import os
import random
import time
import json

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.config import config
from utils.store import fetch_credentials, store_credentials, store_emails, select_email_asread
from utils.models import Email
from utils.common import log_error, extract_email, log_info
from dateutil.parser import parser

parser_instance = parser()

MAX_RETRIES = 5
RETRY_BACKOFF_FACTOR = 2

class GmailProvider:
    def __init__(self, email):
        self.email = email
        self.service = self.authenticate()
        self.user_id = 1
        
    def authenticate(self):
        creds = None
        token_path = f"{os.getcwd()}/token/{self.email}.json"
        try:
            user_id, token = fetch_credentials(self.email)
            if token:
                creds = Credentials.from_authorized_user_info(json.loads(token), config.scope['gmail'])
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    self.user_id = user_id
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(token_path, config.scope['gmail'], redirect_uri='http://localhost:9090')
                    creds = flow.run_local_server(port=0)
                    creds_json = creds.to_json()
                    store_credentials(self.email, creds_json)

            service = build('gmail', 'v1', credentials=creds)
            return service
        except Exception as e:
            log_error("Error during Gmail authentication", e)
            raise

    def fetch_email_metadata(self, next_page_token=None):
        try:
            return self.service.users().messages().list(userId='me', labelIds=['INBOX'], pageToken=next_page_token).execute()
        except HttpError as e:
            log_error("HTTP Error occurred while fetching email metadata", e)
            raise
    def fetch_email_details(self, message_id):
        try:
            return self.service.users().messages().get(userId='me', id=message_id).execute()
        except HttpError as e:
            log_error(f"HTTP Error occurred while fetching email details for message ID {message_id}", e)
            raise
    
    def process_email_message(self, msg):
        payload = msg['payload']
        headers = payload['headers']
        subject = sender = receiver = message = received_at = None
        for header in headers:
            if header['name'] == 'From':
                sender = extract_email(header.get('value', ''))
            if header['name'] in ['To', 'Delivered-To']:
                receiver = extract_email(header.get('value', ''))
            if header['name'] == 'Subject':
                subject = header.get('value', '')
            if header['name'] in ['Date', 'date']:
                try:
                    received_at = parser_instance.parse(header['value']).strftime('%Y-%m-%d %H:%M:%S')
                except (TypeError, ValueError) as e:
                    log_error("Error parsing date", e)
                    received_at = None  # Set to None or handle as needed
        if 'snippet' in msg:
            message = msg.get('snippet')
        user_id = self.user_id
        message_id = msg['id']
        history_id = msg['historyId']
        
        email = Email(user_id, sender, receiver, subject, message, received_at, message_id, history_id)
        log_info(f"Processed email: {email.to_dict()}")
        return email
    
    def fetch_store_emails(self):
        next_page_token = None
        retries = 0

        while True:
            try:
                email_data = []
                results = self.fetch_email_metadata(next_page_token)
                messages = results.get('messages', [])
                next_page_token = results.get('nextPageToken', None)

                for message in messages:
                    msg = self.fetch_email_details(message['id'])
                    email = self.process_email_message(msg)
                    email_data.append(email)
            
                if not next_page_token:
                    break

                retries = 0  # Reset retries after a successful fetch

            except HttpError as e:
                if retries < MAX_RETRIES:
                    retries += 1
                    sleep_time = RETRY_BACKOFF_FACTOR ** retries + random.uniform(0, 1)
                    log_error(f"Retrying in {sleep_time} seconds...", e)
                    time.sleep(sleep_time)
                else:
                    log_error("Max retries exceeded", e)
                    raise
            except Exception as e:
                log_error("Unexpected error occurred while fetching emails", e)
                raise
            finally:
                if email_data:
                    # store_emails_threaded(email_data)                    
                    store_emails(email_data)
        return email_data

    def fetch_and_process_email(self, message_id):
        try:
            msg = self.fetch_email_details(message_id)
            email = self.process_email_message(msg)
            return email
        except Exception as e:
            log_error(f"Error fetching email {message_id}", e)
            return None
    
    def mark_email_as_read(self):
        try:
            # Fetch stored email from the database
            for each in select_email_asread():
                message_id = each
                self.service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()
        except Exception as error:
            log_error(f"An error occurred: {error}")
            
        except Exception as error:
            log_error(f"An error occurred: {error}")
    