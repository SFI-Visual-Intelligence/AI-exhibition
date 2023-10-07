from cgitb import text
import cv2
from cv2 import fastNlMeansDenoising
import os
import sys
import detection
#from deepface import DeepFace
#from retinaface import RetinaFace
import detected_face
import buttons
import textdisplays
import time
##
# TODO: 
# - test other face detection methods
# - record the number of faces analyzed each day in a file or each hour
##
reset_time = 4.0 # reset text display time in seconds
trigger_time = 2.0 # time between 2 analyzes

# initializing face recognition methods
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#recognizer = cv2.face.LBPHFaceRecognizer_create()

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)# (0) or ("/dev/video0"), usb webcam cam have a higher number
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
print('Press "esc" key to exit')
print('Press space bar to compute the values')
print(f'Camera resolution {width} x {height}')
zoom = 2

# change the size
cam.set(3, int(width * zoom)) # set video width
cam.set(4, int(height * zoom)) # set video height

# initialize timer
previous = time.time()
delta = 0

analyzed = 0
display_val = False

while True:
    ret, img = cam.read()
    img = cv2.flip(img, 1) # mirror
    #img=cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE) # portrait
    #img = textdisplays.press_space(img)

    current = time.time()
    delta += current - previous
    previous = current

    faces,gray = detection.get_faces(img, face_detector)    #coordinates for box around detected face
    

    if len(faces) >=1 and (delta > trigger_time and analyzed == 0):
        print(f'{trigger_time} seconds have passed, running analysis...')
        display_val = True
        delta = 0
        analyzed_faces = detected_face.face_analyzing(img, faces) #estimating age, gender and emotion
        face_analyzed_pos = [face.rect for face in analyzed_faces]
        analyzed = 1
    
    if analyzed == 1:        
        matching_faces = detected_face.rectangle_comparison(faces, face_analyzed_pos)
        for index, match in enumerate(matching_faces):
            analyzed_faces[match].x, analyzed_faces[match].y, analyzed_faces[match].w, analyzed_faces[match].h = faces[index]

    # Iterate over each face found from first model.
    for index, (x,y,w,h) in enumerate(faces):
        # Draw rectangle from haarcascade face detection result.
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        if analyzed == 0:
            img = textdisplays.countdown(img, x, y, w, h, trigger_time - delta)
        if analyzed == 1 and len(matching_faces) > index:
            face_ = analyzed_faces[matching_faces[index]]
        if analyzed == 1 and len(matching_faces) < index + 1:
            img = textdisplays.lack_of_face(img, x,y,w,h)

        if delta > reset_time and analyzed == 1:
            print(f'{reset_time} seconds have passed, removing text')
            #img = textdisplays.clear_text(img, x, y, w, h)
            display_val = False
            analyzed = 0
            delta = 0
        if display_val == True:
            try:
                img = textdisplays.face_estimations(img, face_, x, y, w, h)
            except:
                img = textdisplays.not_estimated(img, x, y, w, h)


    #imgS = cv2.resize(img, (width*2, height*2))                # Resize image
    imgS = img
    cv2.imshow('Camera',imgS)
    
    if buttons.endtest() == True:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()