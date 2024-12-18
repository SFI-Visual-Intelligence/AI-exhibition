"""
TODO: When the deepface algorithm finds a face but the haarcascade does not, 
"""

import cv2
import numpy as np
import os
import sys
import detection
from deepface import DeepFace
from retinaface import RetinaFace
import detected_face

# initializing face recognition methods
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(detection.model_file)
person_id2name = detection.read_person_names(detection.person_names_file)
undefined_person = 'Unknown'
confidence_threshold = 20
face_analyzing_time = 100
frame = face_analyzing_time + 1
people = dict()

for names in person_id2name.values():
    people[names] = ['calculating...', 'calculating...', 'calculating...']
people[undefined_person] = ['unknown', 'unknown', 'unknown']

def get_face_from_index(faces, ind):    #match indexes 
    for face in faces:
        # print(face.haarcascade_id, ind, 'get faces from index')
        if face.haarcascade_id == ind:
            return face

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, int(640*3/2)) # set video width
cam.set(4, int(480*3/2)) # set video height
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, img = cam.read()
    img = cv2.flip(img, 1) # mirror
    faces,gray = detection.get_faces(img, face_detector)    #coordinates for box around detected face
   
    # Only allow the deepface algorithm to run when enough frames have gone due to slow performance of deepface analyze.
    frame += 1
    person_ids = []

    # Iterate over each face found from first model.
    for index, (x,y,w,h) in enumerate(faces):

        # Draw rectangle from haarcascade face detection result.
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        # Predict what person is in what frame
        person_id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # First off we set the detected person as undefined
        person_name = undefined_person

        # Check if confidence is less than 100 ==> "0" is perfect match 
        if ((100 - confidence) < confidence_threshold):
            continue

        # Find name of person given id
        person_name = person_id2name[str(person_id)]
        person_ids.append(person_id)
        confidence_text = "  {0}%".format(round(100 - confidence))

        #text display
        cv2.putText(img, str(person_name), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence_text), (x+5,y+h-5), font, 1, (255,255,0), 2)  
        # If deepface finds more than 0 faces, we match up the indices of deepface´s retinaface and
        # the haarcascade results.
    if frame > face_analyzing_time and len(person_ids) > 0:
        analyzed_faces = detected_face.face_analyzing(img, faces, person_ids) #estimating age, gender and emotion and orders after faces found in line 39
        frame = 0 
    for face_ind, face_id in enumerate(person_ids):
        person_name = person_id2name[str(face_id)] 
        if len(analyzed_faces) > 0  and len(person_ids) > 0 and frame == 0:

            # Match deepface and haarcascade results together to set the correct attributes to the
            # correct name.
            current_face = get_face_from_index(analyzed_faces, face_id)
                
            if current_face is None:    #skip if face isn't found
                pass
            else:
                print('Matched face '+str(face_id), 'to '+ person_name)
                print('Found '+ person_name, '- Updating their info...')
                people[person_name] = [current_face.age, current_face.gender, current_face.emotion] #update estimation information

        (x,y,w,h) = faces[face_ind]
        #Text display
        cv2.putText(img, 'Age: '+ str(people[person_name][0]), (x+w,y+15), font, 0.5, (0,0,0), 2)
        cv2.putText(img, 'Gender: '+ str(people[person_name][1]), (x+w,y+30), font, 0.5, (0,0,0), 2)
        cv2.putText(img, 'Emotion: '+ str(people[person_name][2]), (x+w,y+45), font, 0.5, (0,0, 0), 2)
    cv2.imshow('camera',img)
    k = cv2.waitKey(5) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()