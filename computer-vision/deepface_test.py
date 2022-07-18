from deepface import DeepFace
import cv2

font = cv2.FONT_HERSHEY_SIMPLEX

result = DeepFace.analyze(img_path="dataset/img1.jpg", actions = ["age", "gender", "race", "emotion"])

img = cv2.imread("dataset/img1.jpg")

print(result)

x, y, w, h = map(int, result["region"].values())

cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.putText(img, f"Alder = {result['age']}", (x+w+30, y), font, 1, (0, 255, 0), 2)
cv2.putText(img, f"Kjønn : {result['gender']}", (x+w+30, y+40), font, 1, (0, 255, 0), 2)
cv2.putText(img, f"Etnisitet : {result['dominant_race']}", (x+w+30, y+80), font, 1, (0, 255, 0), 2)
cv2.putText(img, f"Ansiktsuttrykk : {result['dominant_emotion']}", (x+w+30, y+120), font, 1, (0, 255, 0), 2)
cv2.imshow("testimg", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
