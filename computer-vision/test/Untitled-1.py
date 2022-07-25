from retinaface import RetinaFace
from deepface import DeepFace
import numpy as np
import cv2

img = cv2.imread('img.jpg')

find_face = RetinaFace.detect_faces(img)

x, y, w, h = map(int, find_face['face_1']['facial_area'])
analyzed_face = DeepFace.analyze(img[x:x+w, y:y+h], actions = ['age', 'gender', 'emotion'], enforce_detection=False)

print(analyzed_face)
cv2.imshow("Result", img)
cv2.waitKey(0)
