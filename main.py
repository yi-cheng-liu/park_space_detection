import cv2
import numpy as np
import pickle 
import cvzone

# choose video feed
video = ["carPark.mp4", "carPark2.mp4"]
play_idx = 0
cap = cv2.VideoCapture(video[play_idx])

space_width, space_height = 105, 45 # width and height of the parking space

with open('CarParkPos', 'rb') as file:
    posList = pickle.load(file)


def checkParkingSpace(imgPro):
    spaceCounter = 0
    
    for pos in posList:
        x, y = pos
        pos_width = pos[0] + space_width
        pos_height = pos[1] + space_height
        cv2.rectangle(img, pos, (pos_width, pos_height), (255, 0, 255), 2)
        
        imgCrop = imgPro[y: pos_height, x: pos_width]
        count = cv2.countNonZero(imgCrop)
        
        if count < 800:
            color = (0, 255, 0) # green
            thickness = 4
            spaceCounter += 1
        else:
            color = (0, 0, 255) # red
            thickness = 4
 
        cv2.rectangle(img, pos, (pos_width, pos_height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + space_height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)
 
        cvzone.putTextRect(img, f'Empty: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                           thickness=3, offset=20, colorR=(0,200,0))
        cvzone.putTextRect(img, f'Occcupied: {len(posList)-spaceCounter}/{len(posList)}', (500, 50), scale=3,
                           thickness=3, offset=20, colorR=(0,0,200))


while True:
    # Keep repeating the video, and read the frames
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    
    # Apply grayscale, blur, and find the adaptive threshold with gaussian 
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    
    # Apply median filter, remove some noises
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    
        
    for pos in posList:
        pos_width = pos[0] + space_width
        pos_length = pos[1] + space_height
        cv2.rectangle(img, pos, (pos_width, pos_length), (0, 0, 255), 2)
    
    checkParkingSpace(imgDilate)
    
    cv2.imshow("img", img)
    # cv2.imshow("imgBlur", imgBlur)
    # cv2.imshow("imgThres", imgMedian)
    cv2.waitKey(10)