import os
import requests
from msal import ConfidentialClientApplication
from utils.config import SCOPES
from provider.base import EmailProvider
from utils.store import get_db_connection

class OutlookProvider(EmailProvider):
    def __init__(self):
        self.service = self.authenticate()

    def authenticate(self):
        print("Authenticating with Outlook")

    def process_email_message(self):
        try:
            print(f"Email process")
        except Exception as e:
            print(f"Error fetching emails: {e}")

    def mark_as_read(self, email_id):
        try:
            # Implement marking email as read using Outlook API
            print(f"Email {email_id} marked as read")
        except Exception as e:
            print(f"Error marking as read: {e}")

    def move_message(self, email_id, folder):
        try:
            # Implement moving message using Outlook API
            print(f"Email {email_id} moved to {folder}")
        except Exception as e:
            print(f"Error moving message: {e}")
