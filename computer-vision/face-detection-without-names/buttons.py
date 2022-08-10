import cv2

def analyzation():
    k = cv2.waitKey(33)
    if k == 32: #run face analyse on pressing spacebar 
        return True

def endtest():
    k = cv2.waitKey(5) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        return True

