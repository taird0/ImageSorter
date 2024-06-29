from PIL import Image
import argparse
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials   
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def checkColor(rgb):
    r, g, b = rgb

    if((r - g) > 20 and (r - b) > 20):
        return "red"
    elif((g - r) > 20 and (g - b) > 20):
        return "green"
    elif((b - r) > 20 and (b - g) > 20):
        return "blue"
    else:
        return False
    
def saveToDrive(image_path, folderID):
    creds = None
    
    #Access and refresh tokens stored in token.json - check if this already exists first
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scope='https://www.googleapis.com/auth/drive')
    if not creds or not creds.valid:
        #If user credentials are valid but expired refresh access token
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", scopes="https://www.googleapis.com/auth/drive"
            )
            creds = flow.run_local_server(port=0)
        #Save credentials to json file
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials = creds)

        #Upload file to specified folder

        #splits the filepath - tail contains the filename and head rest of path
        head, tail = os.path.split(image_path)
        
        file_metadata = {
            "name": tail,
            "parents": [folderID]
        }

        media = MediaFileUpload(image_path, mimetype='image/jpeg') 

        file = service.files().create(body=file_metadata,
                                      media_body = media,
                                      fields='id').execute()

def main(image_path):

    colorCode = {
        'red': '1qiCQw66znHkb45JGsBk3i7HF9YhkMoPj',
        'blue': '1Z3T7lj1dc6YhmUD0Uf0ZR_Ma_E8dNmv_',
        'green': '1e2loTjljHEk4J78vn_l_uj5FeIzKcBQu'
                }

    with Image.open(image_path) as im:
        
        pixels = im.load()

        width, height = im.size

        foundColor = False

        while(foundColor):
            for y in range(height):
                for x in range(width):
                    rgb_value = im.getpixel((x, y))

                    foundColor = checkColor(rgb_value)
        
        saveToDrive(image_path, colorCode[foundColor])
        



                

    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Save a JPG Image into Google Drive - Color coded")
    parser.add_argument('input_image', help='Image to be sorted')

    args = parser.parse_args()
    main(args.input_image)