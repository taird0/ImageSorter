from PIL import Image
import argparse
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials   
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError

#TODO Break logic up into more functions (Refresh token etc) / Add better error handling
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
        print('Refreshing credentials')
        if self.creds and self.creds.expired and self.creds.refresh_token:
            try:
                self.creds.refresh(Request())
                self.save_credentials
                print('Credentials Refreshed successfully')
            except RefreshError as error:
                self.handle_refresh_error(error)
                return False
        return True
    
    def handle_refresh_error(self, error):
        print('Attempting to recreate credentials')
        self.create_token()

    def save_credentials(self):
        print('Saving Creds')
        with open(self.token_file, 'w') as token:
            token.write(self.creds.to_json()) 

    def authenticate(self):
        print('Authenticating')
        if not self.creds or not self.creds.valid:
            if not self.load_credentials():
                self.create_token()

    def create_token(self):
        print('Creating token.')
        flow = InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, self.scopes
        )
        self.creds = flow.run_local_server(port=0)
        self.save_credentials()


def checkColor(rgb):
    r, g, b = rgb
    
    #If the difference between rgb values is greater than 20
    #Returns the correct color

    if((r - g) > 20 and (r - b) > 20):
        print("Found color")
        return True, "red"
    elif((g - r) > 20 and (g - b) > 20):
        print("Found color")
        return True, "green"
    elif((b - r) > 20 and (b - g) > 20):
        print("Found color")
        return True, "blue"
    else:
        return False, ""
    


def saveToDrive(image_path, folderID):

    auth = GoogleDriveAuthenticator(client_secrets_file="credentials.json")

    try:
        auth.authenticate()
    except Exception as error:
        print(f"An error occured during auth: {error}")
        auth.refresh_credentials()

    try:
        service = build("drive", "v3", credentials = auth.creds)

        #Upload file to specified folder

        #splits the filepath - tail contains the filename and head rest of path
        head, tail = os.path.split(image_path)

        #Test 
        print(tail)
        
        file_metadata = {
            "name": tail,
            "parents": [folderID]
        }

        media = MediaFileUpload(image_path, mimetype='image/jpeg') 

        file = service.files().create(body=file_metadata,
                                      media_body = media,
                                      fields='id').execute()
    except HttpError as error:
        print(f"Http Error: {error}")

        
def main(image_path):

    #Dictionary containing GD folder ID's
    colorCode = {
        'red': '1qiCQw66znHkb45JGsBk3i7HF9YhkMoPj',
        'blue': '1Z3T7lj1dc6YhmUD0Uf0ZR_Ma_E8dNmv_',
        'green': '1e2loTjljHEk4J78vn_l_uj5FeIzKcBQu'
                }

    with Image.open(image_path) as im:
        width, height = im.size
        foundColor = False

        #Loop through each pixel in image
        for y in range(height):
            for x in range(width):
                #Pass the RGB value to checker function
                rgb_value = im.getpixel((x, y))
                foundColor, color = checkColor(rgb_value)

                if foundColor:
                    break
            if foundColor:
                break
        
        if foundColor:
            print("Color Found")
            saveToDrive(image_path, colorCode[color])
        else:
            print("The program could not identify a color.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Save a JPG Image into Google Drive - Color coded")
    parser.add_argument('input_image', help='Image to be sorted')
    
    args = parser.parse_args()
    main(args.input_image)


