from PIL import Image
import argparse
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from GoogleDriveAuthenticator import GoogleDriveAuthenticator as gda


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

    auth = gda(client_secrets_file="credentials.json")

    try:
        auth.authenticate()
    except Exception as error:
        print(f"An error occured during auth: {error}")
        auth.refresh_credentials()

    try:
        service = build("drive", "v3", credentials = auth.creds)

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

def process_image(image_path):
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
        
def main(image_path):
    if image_path.lower().endswith('.jpg'):
        process_image(image_path)
    else:
        for filename in os.listdir(image_path):
            if filename.lower().endswith('.jpg'):
                this_path = os.path.join(image_path, str(filename))
                process_image(this_path)
                print(f'{filename} saved to drive.')




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Save a JPG Image into Google Drive - Color coded")
    parser.add_argument('input_image', help='File/Directory to be sorted.')
    
    args = parser.parse_args()
    main(args.input_image)


