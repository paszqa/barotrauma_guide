#Count execution time
from datetime import datetime

#Imports
import os
import sys
import urllib
import time
import math
import requests #to get discord/twitch avatars
from PIL import Image, ImageDraw, ImageFont, ImageFilter

### Settings
countFont = ImageFont.truetype('kremlin.ttf',20)
nameFont = ImageFont.truetype('kremlin.ttf',15)

####################################
# Functions
####################################
def resize_image(image_path, max_width, max_height):
    # Open the image
    image = Image.open(image_path)
    
    # Get the original width and height
    width, height = image.size
    
    # Calculate the aspect ratio
    aspect_ratio = width / height
    
    # Determine the new width and height based on the constraints
    new_width = min(width, max_width)
    new_height = min(height, max_height)
    
    # Adjust the width and height based on the aspect ratio
    if new_width / new_height > aspect_ratio:
        new_width = int(new_height * aspect_ratio)
    else:
        new_height = int(new_width / aspect_ratio)
    
    # Resize the image
    resized_image = image.resize((new_width, new_height))
    
    # Save the resized image
    return resized_image
    #print("Image resized successfully.")
    
def get_html_line_with_url(variable):
    # Replace space with "_"
    variable = variable.replace(" ", "_").strip()
    # Generate URL
    url = f"https://barotraumagame.com/wiki/{variable}"
    # Send a GET request to the URL
    response = requests.get(url, allow_redirects=True)
    # Get the HTML source code
    html = response.text
    # Find the line containing '<meta property="og:url"'
    for line in html.split("\n"):
        if '<meta property="og:image"' in line:
            imageUrl = line.strip().split('content="')[1].replace('" />','')
            return imageUrl
    return None

def add_section_to_image(csv_file, startX, startY, img, imgDraw, prodDifference, prodMaxWidth):
    f = open(csv_file, "r")
    startCorner = (120,120)
    lineIndex = 0
    lineHeight = 62
    for line in f:
        print("##################")
        elements = line.split(";")
        elementIndex = 0
        horizontalOffset = 0
        for element in elements:
            print("---")
            if elementIndex == 0 or elementIndex == 2 or elementIndex == 4 or elementIndex == 6:
                if element != "" and element != " ":
                    print("NAME:"+element)
                    variable = element
                    line_with_url = get_html_line_with_url(variable)
                    download_image(line_with_url, "image.png")
                    objectImage = resize_image("image.png", 47, 53)
                    currentCorner = (math.floor(startX + horizontalOffset + (47 - objectImage.width)/2), math.floor(startY + lineHeight * lineIndex + (53 - objectImage.height)/2))
                    print(currentCorner)
                    img.paste(objectImage, currentCorner, objectImage)
                    objectImage.close()
            elif elementIndex == 8:
                print("MACHINE = "+element)
            elif elementIndex == 9:
                print("SPECIAL = "+element)
            elif elementIndex == 11:
                #print("PROD count: "+element)
                if int(element) < 10:
                    prodCountOffsetX = prodMaxWidth - 12
                else:
                    prodCountOffsetX = prodMaxWidth - 30
                prodCountOffsetY = 35
                if element.strip() != "" and element.strip() != " " and element.strip() != "1":
                    #textCorner = (startX + horizontalOffset + 17, startY + 80 * lineIndex + 50)
                    textCorner = (startX + horizontalOffset + prodDifference + prodCountOffsetX, startY + lineHeight * lineIndex + prodCountOffsetY)
                    print(textCorner)
                    imgDraw.text(textCorner, element, font=countFont, fill=(255,255,255))     
                horizontalOffset += 64   
            elif elementIndex == 10:
                print("PROD name: "+element)
                horizontalOffset += 80
                if element != "" and element != " ":
                    variable = element
                    line_with_url = get_html_line_with_url(variable)
                    download_image(line_with_url, "image.png")
                    objectImage = resize_image("image.png", prodMaxWidth, 53)
                    objectImage = objectImage.convert("RGBA")
                    currentCorner = (math.floor(startX + horizontalOffset + prodDifference + (47 - objectImage.width)/2), math.floor(startY + lineHeight * lineIndex + (53 - objectImage.height)/2))
                    print(currentCorner)
                    img.paste(objectImage, currentCorner, objectImage)
                    objectImage.close()
            else:
                countOffsetX = 44
                countOffsetY = 35
                if element != "" and element != " ":
                    print("COUNT:"+element)
                    textCorner = (startX + horizontalOffset + countOffsetX, startY + lineHeight * lineIndex + countOffsetY)
                    print(textCorner)
                    imgDraw.text(textCorner, element, font=countFont, fill=(255,255,255))    
                horizontalOffset += 64        
            elementIndex = elementIndex + 1     
        lineIndex = lineIndex + 1

def add_section_to_minerals(csv_file, startX, startY, img, imgDraw, prodDifference, prodMaxWidth, prodMaxHeight):
    f = open(csv_file, "r")
    startCorner = (120,120)
    lineIndex = 0
    lineHeight = 86
    for line in f:
        print("##################")
        elements = line.split(";")
        elementIndex = 0
        horizontalOffset = 0
        currentProdName = ""
        for element in elements:
            print("---")
            if elementIndex == 1 or elementIndex == 3 or elementIndex == 5:
                if element != "" and element != " ":
                    print("res NAME:"+element)
                    variable = element
                    line_with_url = get_html_line_with_url(variable)
                    download_image(line_with_url, "image.png")
                    objectImage = resize_image("image.png", 47, 53)
                    currentCorner = (math.floor(startX + horizontalOffset + (47 - objectImage.width)/2), math.floor(startY + lineHeight * lineIndex + (53 - objectImage.height)/2))
                    print(currentCorner)
                    img.paste(objectImage, currentCorner, objectImage)
                    objectImage.close()
            elif elementIndex == 0:
                currentProdName = element
                print("PROD name: "+currentProdName)
                horizontalOffset += 80
                if element != "" and element != " ":
                    variable = element
                    line_with_url = get_html_line_with_url(variable)
                    download_image(line_with_url, "image.png")
                    objectImage = resize_image("image.png", prodMaxWidth, prodMaxHeight)
                    objectImage = objectImage.convert("RGBA")
                    currentCorner = (math.floor(startX + horizontalOffset + (47 - objectImage.width)/2), math.floor(startY + lineHeight * lineIndex + (prodMaxHeight - objectImage.height)/2) - 10)
                    print(currentCorner)
                    img.paste(objectImage, currentCorner, objectImage)
                    objectImage.close()
                    #Paste text below mineral
                    prodNameOffsetX = math.floor(len(currentProdName)/2 * 7)
                    textCorner = (startX + horizontalOffset - prodNameOffsetX, startY + lineHeight * lineIndex + 50)
                    imgDraw.text(textCorner, currentProdName.upper(), font=nameFont, fill=(255,255,255))   
                    horizontalOffset += 100
            elif elementIndex > 6:
                    percents = element.split(",")
                    for chance in percents:
                        currentCornerX = (startX + horizontalOffset)
                        currentCornerY = (startY + lineHeight * lineIndex)
                        #Draw dark background
                        shape = [(currentCornerX, currentCornerY), (currentCornerX + 15, currentCornerY + 60)]
                        imgDraw.rectangle(shape, fill ="#333", outline ="black")
                        #Draw percent
                        chanceNormalized = (125 - float(chance)) / 125
                        chanceStartY = (chanceNormalized * 60)
                        shape = [(currentCornerX, currentCornerY + chanceStartY), (currentCornerX + 15, currentCornerY + 60)]
                        rectangleColor = (math.floor(chanceNormalized * 2.5 * 255), math.floor((1 - (chanceNormalized * 1)) * 255), 0)
                        imgDraw.rectangle(shape, fill = rectangleColor, outline ="black")
                        #Move to next
                        horizontalOffset += 15
                    horizontalOffset += 5
            else:
                countOffsetX = 44
                countOffsetY = 36
                if element != "" and element != " ":
                    print("COUNT:"+element)
                    textCorner = (startX + horizontalOffset + countOffsetX, startY + lineHeight * lineIndex + countOffsetY)
                    print(textCorner)
                    imgDraw.text(textCorner, element, font=countFont, fill=(255,255,255))    
                horizontalOffset += 64        
            elementIndex = elementIndex + 1     
        lineIndex = lineIndex + 1


def download_image(url, filename):
    #print("Getting image from: "+url)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        #print(f"Image downloaded successfully as {filename}")
    else:
        print("Failed to download image from url: "+url)
####################################
#   Get image background
####################################
img = Image.open('background1920x1200empty.png')
img = img.convert("RGBA")
imgDraw = ImageDraw.Draw(img,'RGBA')

####################################
# Get URL of image and download it
####################################
#variable = "Organic Fiber"
#line_with_url = get_html_line_with_url(variable)
#download_image(line_with_url, "image.png")

#Output GEAR
#add_section_to_image("ingredients.csv", 20, 40, img, imgDraw, 0, 47)
#add_section_to_image("fuel.csv", 20, 540, img, imgDraw, 0, 47)
#add_section_to_image("gear.csv", 500, 40, img, imgDraw, 0, 47)
#add_section_to_image("depth.csv", 500, 740, img, imgDraw, 0, 47)
#add_section_to_image("other.csv", 970, 40, img, imgDraw, 0, 47)

#Output WEAPONS
#add_section_to_image("ammobox.csv", 20, 40, img, imgDraw, 0, 47)
#add_section_to_image("explo.csv", 530, 40, img, imgDraw, -64, 47)
#add_section_to_image("weapons.csv", 1000, 40, img, imgDraw, 0, 63)
#add_section_to_image("ammo.csv", 1490, 40, img, imgDraw, -64, 47)

#Output BOOSTERS
#add_section_to_image("boosters.csv", 20, 40, img, imgDraw, -64, 47)

#Output MINERALS
add_section_to_minerals("minerals.csv", 40, 50, img, imgDraw, -64, 64, 64)
add_section_to_minerals("minerals2.csv", 660, 50, img, imgDraw, -64, 64, 64)
add_section_to_minerals("minerals3.csv", 1280, 50, img, imgDraw, -64, 64, 64)

img.save("minerals.png", quality=95)