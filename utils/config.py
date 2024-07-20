from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.db_name = os.getenv('DB_NAME')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        self.encryption_key = os.getenv('ENCRYPTION_KEY')
        self.input_max_attempts = int(os.getenv('INPUT_MAX_ATTEMPTS'))
        self.scope = {
            'gmail': ['https://www.googleapis.com/auth/gmail.readonly'
                    ],
            'outlook': ['https://graph.microsoft.com/Mail.Read']
        }

# Usage
config = Config()