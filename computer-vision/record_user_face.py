import cv2
import os
import detection

number_of_faces = 90
data_folder = detection.data_dir
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
# For each person, enter a name
face_id = input('\n enter user name end press <return> ==>  ')
print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = 0
while(True):
    ret, img = cam.read()
    #img = cv2.flip(img, 1) # mirror
    faces, gray = detection.get_faces(img, face_detector)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1
        # Save the captured image into the datasets folder
        filename = 'User.' + str(face_id) + '.' + str(count) + '.jpg'
        data_file = os.path.join(data_folder,filename) 
        print("saving file", data_file)
        cv2.imwrite(data_file, gray[y:y+h,x:x+w])
    cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= number_of_faces: # Take as many face samples as needed and stop video
         break
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()