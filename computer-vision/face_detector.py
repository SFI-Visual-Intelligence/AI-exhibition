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
count1 = 1000
face_analyzing_time = 50
people = dict()
for names in person_id2name.values():
    people[names] = ['unknown', 'unknown', 'unknown']
people[undefined_person] = ['unknown', 'unknown', 'unknown']




# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, int(640*3/2)) # set video width
cam.set(4, int(480*3/2)) # set video height
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, img = cam.read()
    img = cv2.flip(img, 1) # mirror
    faces,gray = detection.get_faces(img, face_detector)    #coordinates for box around detected face
   

    count1 +=1
    if count1 > face_analyzing_time:
        state_estimation, ordered_faces = detected_face.face_analyzing(img, faces) #estimating age, gender and emotion and orders after faces found in line 39
        count1 = 0
    
    
    for index, (x,y,w,h) in enumerate(faces):
        
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        person_id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        # Check if confidence is less them 100 ==> "0" is perfect match 
        if ((100 - confidence) > confidence_threshold):
            person_name = person_id2name[str(person_id)]
            confidence = "  {0}%".format(round(100 - confidence))
            if count1 == 0:
                if len(ordered_faces) < 1:  #skips if no faces found by retina
                    pass
                else:   #updates estimates about person
                    people[person_name] = [state_estimation[ordered_faces[index]]['age'], state_estimation[ordered_faces[index]]['gender'],state_estimation[ordered_faces[index]]['dominant_emotion']]
            
        else:
            person_name = undefined_person
            confidence = "  {0}%".format(round(100 - confidence))

        
        #Text display
        cv2.putText(img, 'Age: '+ str(people[person_name][0]), (x+w,y+15), font, 0.5, (0,0,0), 2)
        cv2.putText(img, 'Gender: '+ str(people[person_name][1]), (x+w,y+30), font, 0.5, (0,0,0), 2)
        cv2.putText(img, 'Emotion: '+ str(people[person_name][2]), (x+w,y+45), font, 0.5, (0,0, 0), 2)
        cv2.putText(img, str(person_name), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    cv2.imshow('camera',img)
    k = cv2.waitKey(5) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()