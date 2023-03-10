import cv2

import pickle

# initilization
space_width, space_height = 105, 48 # width and height of the parking space

try:
    with open('CarParkPos', 'rb') as file:
        posList = pickle.load(file)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    '''
    Left click on the mouse for adding the block and right click for deleting
    Input - events: 

    Output - 
    '''
    block = 12
    
    # add rectangle to parking space
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))

    if events == cv2.EVENT_LBUTTONDBLCLK:
        for i in range(block):
            posList.append((x, y+i*space_height))
        
    # delete rectangle in posList
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 <= x <= x1+space_width and y1 <= y <= y1+space_height:
                posList.pop(i)
    
    with open('CarParkPos', 'wb') as file:
        pickle.dump(posList, file)

while True:
    # import the image every time
    img = cv2.imread('parking_lot.png')

    for pos in posList:
        pos_width = pos[0] + space_width
        pos_length = pos[1] + space_height
        cv2.rectangle(img, pos, (pos_width, pos_length), (255, 0, 255), 2)
    
    cv2.imshow("park image", img)
    cv2.setMouseCallback("park image", mouseClick)
    cv2.waitKey(1)
