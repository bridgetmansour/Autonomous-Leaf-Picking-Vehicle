#imports libraries
from camera import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import cv2
import serial
import math
import time


#connects arduino
ser = serial.Serial('/dev/ttyACM0', 19200, timeout=1)


def start():
    

    #retakes picture when restart is set to 1
    if restart == 1:
        camera.capture('/home/pi/Desktop/currentPic' + '.jpg')    


    #reads image
    filePath = '/home/pi/Desktop/currentPic.jpg'
    image = img.imread(filePath,format = 'RGB')
    plt.imshow(image)


    #blurs image
    blurImage = cv2.GaussianBlur(image, (25,25),0)
    plt.imshow(blurImage)


    #converts image from RGB to HSV
    imageInHSV = cv2.cvtColor(blurImage,cv2.COLOR_RGB2HSV)


    #creates a green color range mask
    lowerLimit = (40, 27, 19)
    upperLimit = (108, 255, 180)
    greenMask = cv2.inRange(imageInHSV, lowerLimit, upperLimit)

    isGreen = greenMask > 0
    greenOnly = np.zeros_like(blurImage, np.uint8)
    greenOnly[isGreen] = blurImage[isGreen]
    plt.imshow(greenOnly)


    #identifies if there is a potential leaf
    blackImage = np.zeros_like(isGreen)
    percentGreen = math.sqrt(np.mean(blackImage != isGreen))
    print(percentGreen)

    #finds potential leaf's coordinates within picture
    sumRows = np.sum(isGreen, axis=1)
    sumColumns = np.sum(isGreen.T, axis=1)

    index = 0
    longestRow = 0
    longestIndexRow = 0
    for row in sumRows:
        if row > longestRow:
            longestRow = row
            longestIndexRow = index
        index = index + 1
        
    index = 0
    longestColumn = 0
    longestIndexColumn = 0
    for column in sumColumns:

        if column > longestColumn:
            longestColumn = column
            longestIndexColumn = index
        index = index + 1

    print(f'Pixel coordinates for the center of the potential leaf: ({longestIndexRow}, {longestIndexColumn})')


    #finds the direction that the arm needs to move to grab leaf
    pixelToDegree = 65/1024
    centerColumn = 1024/2
    direction = np.abs(longestIndexColumn - centerColumn) * pixelToDegree

    inchesToLeaf = 0.5
    #finds the distance that the car needs to move to face leaf
    if  longestIndexRow >= 350:
        inchesToLeaf = 0.5
    elif longestIndexRow < 350 and longestIndexRow >= 300:
        inchesToLeaf = 0.7
    elif longestIndexRow < 300 and longestIndexRow >= 200:
        inchesToLeaf = 1.2
    elif longestIndexRow < 200 and longestIndexRow > 100:
        inchesToLeaf = 2.7
    elif longestIndexRow < 100 and longestIndexRow > 0:
        inchesToLeaf = 6

    if percentGreen > 0.1:
        

        #isLeaf shape check
        #...
        #isLeaf = True/False
        isLeaf = True
        if isLeaf == True:

            if centerColumn > longestIndexColumn:
                direction = direction + 32.5
                print(f'Turn {round(direction, 2)} degrees to the left to grab the leaf')
            else:
                print(f'Turn {round(direction, 2)} degrees to the right to grab the leaf')

            print(f'The leaf is {round(inchesToLeaf, 2)} inches away')
            
    else:
        isLeaf = False
        inchesToLeaf = 0
        print('There is no leaf within range')

    return(isLeaf, direction, inchesToLeaf)


try:
    restart = 0
    K = False
    while K == False:
        restart = 1
        K,D,I = start()

        if K == True:
            if I > 0.6:
                time.sleep(1)
                data = b'%10.4f' %I
                ser.write(data)
                time.sleep(1)
                print(data)
            else:
                time.sleep(1) 
                ser.write(b'0.5')
                time.sleep(1)       
        else:
            time.sleep(1) 
            ser.write(b'0')
            time.sleep(1)


finally:
    print('done')