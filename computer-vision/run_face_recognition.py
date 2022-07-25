import cv2
import record_user_face
import train_face_recognition
import face_detector

font = cv2.FONT_HERSHEY_SIMPLEX
background = cv2.resize('background.jpg', (int(640*3/2),int(480*3/2)))

record_user_face
add_person = True
while add_person == True:
    cv2.putText(background, 'Press space to add a peron', (int(640*3/2)-40,int(480*3/2)-40), font, 1, (255,255,255), 2)
    cv2.putText(background, 'Press enter to start training', (int(480*3/2),int(480*3/2)), font, 1, (255,255,255), 2)