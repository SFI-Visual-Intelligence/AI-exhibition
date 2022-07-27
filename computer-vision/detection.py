# functions for the detection
import cv2
import os
import json

path = os.getcwd()
data_dir = os.path.join(path,"dataset")
trained_model_dir = os.path.join(path,"trained_models")


model_file = os.path.join(trained_model_dir,'trainer.yml')
person_names_file = os.path.join(trained_model_dir,"persons.json")


def create_dir(dirName):
    # Create target Directory if it doesn't exist
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")

def get_faces(img, face_detector):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #gray = cv2.equalizeHist(gray)
    W, H = gray.shape
    minW, minH = int(0.1* W), int(0.1* H) # 10% of image size
    faces = face_detector.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (minW, minH),
       )
    return faces,gray

def save_person_names(person_id2name, person_names_file):
    with open(person_names_file, 'w') as fp:
        json.dump(person_id2name, fp,  indent=4)

    
def read_person_names(person_names_file):
    with open(person_names_file, 'r') as fp:
        person_id2name = json.load(fp)
    return person_id2name

if __name__ == '__main__':
    pass