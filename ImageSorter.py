from PIL import Image, ImageOps
import argparse
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
    
def saveToDrive(image_path, colorCode):
    creds = None
    
    #Access and refresh tokens stored in token.json - check if this already exists first
    

def main(image_path):

    colorCode = {'red': 'folder_path', 'blue': 'folder_path', 'green': 'folder_path'}

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