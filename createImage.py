#Count execution time
from datetime import datetime
print("asd")

#Imports
import os
import sys
import urllib
import time
import requests #to get discord/twitch avatars
from PIL import Image, ImageDraw, ImageFont, ImageFilter

####################################
# Functions
####################################

def get_html_line_with_url(variable):
    # Replace spaces with "_"
    variable = variable.replace(" ", "_").strip()
    
    # Generate URL
    url = f"https://barotraumagame.com/wiki/{variable}"
    print("Built URL: "+url)
    
    # Send a GET request to the URL
    response = requests.get(url, allow_redirects=True)
    
    
    # Get the HTML source code
    html = response.text
    # Find the line containing '<meta property="og:url"'
    for line in html.split("\n"):
        if '<meta property="og:image"' in line:
            print("Found image line: "+line)
            imageUrl = line.strip().split('content="')[1].replace('" />','')
            print("Found image URL: "+imageUrl)
            return imageUrl
    
    return None

def download_image(url, filename):
    print("Getting image from: "+url)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image downloaded successfully as {filename}")
    else:
        print("Failed to download image")
####################################
#   Get image background
####################################
img = Image.open('background1920x1080.png')
img = img.convert("RGB")
imgDraw = ImageDraw.Draw(img,'RGBA')

####################################
# Get URL of image and download it
####################################
variable = "Organic Fiber"
line_with_url = get_html_line_with_url(variable)
download_image(line_with_url, "image.png")


f = open("gear.csv", "r")

startCorner = (120,120)

lineIndex = 0
for line in f:
    print("RAW LINE:"+line)
    elements = line.split(";")
    elementIndex = 0
    for element in elements:
        #print("RAW ELEMENT:"+element)
        currentCorner = (320 + 64 * elementIndex, 320 + 64 * lineIndex)
        if elementIndex == 1 or elementIndex == 3 or elementIndex == 5 or elementIndex == 7:
            print("NAME:"+element)
            if element != "" and element != " ":
                variable = element
                line_with_url = get_html_line_with_url(variable)
                download_image(line_with_url, "image.png")
                objectImage = Image.open("image.png")
                img.paste(objectImage, currentCorner, objectImage)
                objectImage.close()
        elif elementIndex == 8:
            print("MACHINE = "+element)
        elif elementIndex == 9:
            print("SPECIAL = "+element)
        elif elementIndex == 10:
            print("PROD count: "+element)
        elif elementIndex == 11:
            print("PROD name: "+element)
            if element != "" and element != " ":
                variable = element
                line_with_url = get_html_line_with_url(variable)
                download_image(line_with_url, "image.png")
                objectImage = Image.open("image.png")
                img.paste(objectImage, currentCorner, objectImage)
                objectImage.close()
        else:
            print("COUNT:"+element)       
        elementIndex = elementIndex + 1     
    lineIndex = lineIndex + 1
    
img.save("output.png", quality=95)