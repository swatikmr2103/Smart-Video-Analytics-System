'''
 Seat Belt Detection using opencv and Python

 Created on Wed Mar 25 15:15:58 2020
 
 @author: Vishal Singh

'''

import cv2
import numpy as np
import imutils
import database_test
import numberPlateCap
from datetime import datetime
from datetime import date
import InputImages




#Slope of line
def Slope(a,b,c,d):
    try:

        return (d - b)/(c - a)

    except ZeroDivisionError:
        print("")
    

#inpImage = "/home/swati/SVAS/SeatBeltimages/noSeatBelt1.jpg"


# Reading Belt Image from given Input Image
beltCap = cv2.imread(InputImages.beltImage)

# Resizing The Image
beltCap = imutils.resize(beltCap, height=500)

#Converting To GrayScale
beltgray = cv2.cvtColor(beltCap, cv2.COLOR_BGR2GRAY)

# No Belt Detected Yet
belt = False

# Bluring The Image For Smoothness
blur = cv2.blur(beltgray, (1, 1))


# Converting Image To Edges
if (InputImages.beltImage == "/home/swati/SVAS/SeatBeltimages/noSeatBelt1.jpg" ):
    edges = cv2.Canny(blur, 20, 850)
elif (InputImages.beltImage == "/home/swati/SVAS/SeatBeltimages/seatBelt2.jpg" ):
    edges = cv2.Canny(blur, 30, 728)
    
elif (InputImages.beltImage == "/home/swati/SVAS/SeatBeltimages/seatBelt3.jpg" ):
       edges = cv2.Canny(blur, 30, 728) 
elif (InputImages.beltImage == "/home/swati/SVAS/SeatBeltimages/seatBelt4.jpg" ):
    edges = cv2.Canny(blur, 30, 728)
else:    
    edges = cv2.Canny(blur, 30, 728)



# Previous Line Slope
ps = 0

# Previous Line Co-ordinates
px1, py1, px2, py2 = 0, 0, 0, 0

# Extracting Lines
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap = 10, minLineLength = 70)

# If "lines" Is Not Empty
if lines is not None:

    # Loop line by line
    for line in lines:

        # Co-ordinates Of Current Line
        x1, y1, x2, y2 = line[0]

        # Slope Of Current Line
        
        s = Slope(x1,y1,x2,y2)
       
        # If Current Line's Slope Is Greater Than 0.7 And Less Than 2
        if ((abs(s) > 0.7) and (abs (s) < 2)):

            # And Previous Line's Slope Is Within 0.7 To 2
            if((abs(ps) > 0.7) and (abs(ps) < 2)):

                # And Both The Lines Are Not Too Far From Each Other
                if(((abs(x1 - px1) > 5) and (abs(x2 - px2) > 5)) or ((abs(y1 - py1) > 5) and (abs(y2 - py2) > 5))):

                    # Plot The Lines On "beltCap"
                    cv2.line(beltCap, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.line(beltCap, (px1, py1), (px2, py2), (0, 0, 255), 3)

                    # Belt Is Detected
                    belt = True

        # Otherwise Current Slope Becomes Previous Slope (ps) And Current Line Becomes Previous Line (px1, py1, px2, py2)            
        ps = s
        px1, py1, px2, py2 = line[0]
        
                   
if belt == False:

    cv2.imshow("Seat Belt", beltCap)
    cv2.waitKey(0)

    print("No Seatbelt detected")

    
    # To capture current date
    d1 = date.today()
    # dd-Month-YY 
    date = d1.strftime("%d-%B-%Y")
    print("Today's date:", date)
    

    # current time 
    now = datetime.now()
    time = now.strftime("%I:%M:%p")
    print("Current time is:", time)


    numberPlate, numberPlateStatus = numberPlateCap.detectNumberPlate()
    print("Vehicle Number Detected :",numberPlate)
    print(numberPlateStatus)
    
    database_test.connect_databse()
    database_test.create_database()
    database_test.init_db()
    #print(initilize_db)
    database_test.addChallan(date, time, numberPlate)
    database_test.updateChallans(date, time, numberPlate, "")

    

else:
    print ("Belt Detected\nYou are good to go.")

    # Show The "beltCap"
    
    cv2.imshow("Seat Belt ", beltCap)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



