"""
TODO: When the deepface algorithm finds a face but the haarcascade does not, 
"""

from cgitb import text
import cv2
from cv2 import fastNlMeansDenoising
import numpy as np
import os
import sys
import detection
from deepface import DeepFace
from retinaface import RetinaFace
import detected_face
import buttons
import textdisplays

# initializing face recognition methods
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

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



check_val = 0
display_retry = False

while True:
    ret, img = cam.read()
    img = cv2.flip(img, 1) # mirror
    img=cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE) # portrait

    faces,gray = detection.get_faces(img, face_detector)    #coordinates for box around detected face
        
    if buttons.analyzation() == True:
        if len(faces) < 1:
            display_retry_val = 0
            display_retry = True
        else:
            analyzed_faces = detected_face.face_analyzing(img, faces) #estimating age, gender and emotion and orders after faces found in line 39
            frame = 0 
            check_val = 1
    if check_val == 1:
        face_analyed_pos = [face.rect for face in analyzed_faces]
        matching_faces = detected_face.rectangle_comparison(faces, face_analyed_pos)
        for index, match in enumerate(matching_faces):
            analyzed_faces[match].x, analyzed_faces[match].y, analyzed_faces[match].w, analyzed_faces[match].h = faces[index]
    img = textdisplays.press_space(img)
    if display_retry == True:
        
        img = textdisplays.missed_face(img)
        display_retry_val += 1
        if display_retry_val == 50:
            display_retry = False

    # Iterate over each face found from first model.
    for index, (x,y,w,h) in enumerate(faces):

        # Draw rectangle from haarcascade face detection result.
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        # cv2.putText(img, 'Face '+str(index), (x, y-25), font, 0.5, (0,0,0), 2)
        if check_val == 1 and len(matching_faces) > index:
            face_ = analyzed_faces[matching_faces[index]]
        if check_val == 1 and len(matching_faces) < index + 1:
            img = textdisplays.lack_of_face(img, x,y,w,h)
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