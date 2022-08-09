import numpy as np
import os
import cv2
import json
import detection

# function to get the images and label data
def getImagesAndLabels(data_dir, face_detector):
    imagePaths = [os.path.join(data_dir,f) for f in os.listdir(data_dir)]     
    faceSamples=[]
    ids = []
    person_name_dic = {}
    id_count = 0
    for imagePath in imagePaths:
        img = cv2.imread(imagePath, 0) # open in grayscale
        img_numpy = np.array(img,'uint8')
        person_name = os.path.split(imagePath)[-1].split(".")[1]
        if person_name in person_name_dic:
            person_id = person_name_dic[person_name]
        else:
            person_id = id_count
            person_name_dic[person_name]= person_id
            id_count +=1
        faces = face_detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(person_id)
    return faceSamples,ids, person_name_dic

if __name__ == '__main__':
    # Create target Directory if it doesn't exist
    #detection.create_dir(detection.data_dir)
    detection.create_dir(detection.trained_model_dir)
    # initializing face recognition methods
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
        
    print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
    faces, ids, person_name_dic = getImagesAndLabels(detection.data_dir, face_detector)
    recognizer.train(faces, np.array(ids))
    # Save the model into trainer/trainer.yml
    recognizer.write(detection.model_file) # recognizer.save() worked on Mac, on Ubuntu, but not on Pi?
    # Print the number of faces trained and end program
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
    # save the name of the persons
    person_id2name = {value : key for (key, value) in person_name_dic.items()}
    detection.save_person_names(person_id2name, detection.person_names_file)
