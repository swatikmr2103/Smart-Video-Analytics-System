'''
 Vehicle Number Plate Recognition using OpenCV, Python and Tesseract OCR

 Created on Wed Mar 25 15:15:58 2020
 
 @author: Vishal Singh

'''

import numpy as np
import cv2
import imutils
import pytesseract
import os
import InputImages

'''
For windows try to run Pytesseract using below command:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

'''

def detectNumberPlate():

    # Read the image file
    try:
        
        #Reading number plate from input image
        image = cv2.imread(InputImages.plateImage)
        
    except Exception as err:
        
        print('could not read images {0}'.format(err))

    # Resize the image - change width to 500
    image = imutils.resize(image, width=500)

    # Display the original image
    cv2.imshow("Original Image", image)
    cv2.waitKey(0)

    # RGB to Gray scale conversion
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("1 - Grayscaled image", gray)
    cv2.waitKey(0)

    # Noise removal with iterative bilateral filter(removes noise while preserving edges)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    cv2.imshow("2 - Bilateral Filtered image", gray)
    cv2.waitKey(0)

    # Find Edges of the grayscale image
    edged = cv2.Canny(gray, 170, 200)
    cv2.imshow("3 - Canny Edges", edged)
    cv2.waitKey(0)

    # Find contours based on Edges

    #try:

    (_,contours, new)  = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    #except Exception as err:
        #print("Couldn't find cantours{0}".format(err))

    # Create copy of original image to draw all contours
    img1 = image.copy()
    cv2.drawContours(img1, contours, -1, (0,255,0), 3)
    cv2.imshow("4- Showing All Contours", img1)
    cv2.waitKey(0)

    #sort contours based on their area keeping minimum required area as '30' (anything smaller than this will not be considered)
    contours=sorted(contours, key = cv2.contourArea, reverse = True)[:30]
    NumberPlateCnt = None #we currently have no Number plate contour

    # Top 30 Contours
    img2 = image.copy()
    cv2.drawContours(img2, contours, -1, (0,255,0), 3)
    cv2.imshow("5- Showing Top 30 Contours", img2)
    cv2.waitKey(0)

    # loop over our contours to find the best possible approximate contour of number plate
    count = 0
    idx =1
    for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # print ("approx = ",approx)
            if len(approx) == 4:  # Select the contour with 4 corners
                NumberPlateCnt = approx #This is our approx Number Plate Contour

                # Crop those contours and store it in Cropped Images folder
                x, y, w, h = cv2.boundingRect(c) #This will find out co-ord for plate
                new_img = gray[y:y + h, x:x + w] #Create new image
                try:
                    cv2.imwrite("SVAS" + str(idx) + '.png', new_img) #Store new image
                except:
                    print('cant write the image')
                idx+=1

                break


    # Drawing the selected contour on the original image
    #print(NumberPlateCnt)
    cv2.drawContours(image, [NumberPlateCnt], -1, (0,255,0), 3)
    cv2.imshow("Final Image With Number Plate Detected", image)
    cv2.waitKey(0)

    try:

        Cropped_img_loc = ("SVAS1.png")
        cv2.imshow("Cropped Image ", cv2.imread(Cropped_img_loc))

    except:
        print("we are gerring this erros: " )


    # Use tesseract to covert image into string
    
    text = pytesseract.image_to_string(Cropped_img_loc, lang='eng')

    #print("Vehicle Number Detected :", text)
    #cv2.waitKey(0) #Wait for user input before closing the images displayed

    
    message = "E-Challan has been genrated successfully."

    return text, message


