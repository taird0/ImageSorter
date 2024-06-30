import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials   
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError

class GoogleDriveAuthenticator:
    def __init__(self, client_secrets_file, token_file='token.json', scopes=['https://www.googleapis.com/auth/drive']):
        self.client_secrets_file = client_secrets_file
        self.token_file = token_file
        self.scopes = scopes
        self.creds = None

    def load_credentials(self):
        if(os.path.exists(self.token_file)):
            self.creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)
            return True
        return False

    def refresh_credentials(self):
        print('Refreshing credentials...')
        if self.creds and self.creds.expired and self.creds.refresh_token:
            try:
                self.creds.refresh(Request())
                self.save_credentials
                print('Credentials Refreshed successfully!')
            except RefreshError as error:
                self.handle_refresh_error(error)
                return False
        return True
    
    def handle_refresh_error(self, error):
        print('Attempting to recreate credentials...')
        self.create_token()

    def save_credentials(self):
        print('Saving Credentials...')
        with open(self.token_file, 'w') as token:
            token.write(self.creds.to_json()) 

    def authenticate(self):
        print('Authenticating...')
        if not self.creds or not self.creds.valid:
            if not self.load_credentials():
                self.create_token()

    def create_token(self):
        print('Creating token...')
        flow = InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, self.scopes
        )
        self.creds = flow.run_local_server(port=0)
        self.save_credentials()