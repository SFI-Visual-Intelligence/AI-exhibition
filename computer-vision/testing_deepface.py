from deepface import DeepFace as df
from retinaface import RetinaFace as rf
import cv2
import os
import multiprocessing

models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace",
          "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']

path = os.path.dirname(__file__)
db_path = os.path.join(path, "database")

def find_faces(img, q):
    print("started new core")
    faces = rf.detect_faces(img)
    q.put(faces)


def start_new_process(img, q):
    process = multiprocessing.Process(target=find_faces, args=(img, q))
    return process

def main():
    my_variable = "not done"
    current_process = None
    cam = cv2.VideoCapture(0)
    cam.set(3, int(640*3/2))  # set video widht
    cam.set(4, int(480*3/2))  # set video height
    font = cv2.FONT_HERSHEY_SIMPLEX
    frame = 0
    q = multiprocessing.Queue()

    while True:
        ret, img = cam.read()
        img = cv2.flip(img, 1)
        frame += 1

        print(my_variable)

        if frame > 100:
            if current_process is None:
                current_process = start_new_process(img, q)
                current_process.start()
            else:
                if not current_process.is_alive():
                    current_process.terminate()
                    current_process = None

            frame = 0
        
        print(q.get())

        cv2.imshow("camera", img)
        k = cv2.waitKey(5) & 0xff
        if k == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
