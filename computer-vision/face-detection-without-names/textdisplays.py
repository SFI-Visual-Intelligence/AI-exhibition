import cv2

font = cv2.FONT_HERSHEY_SIMPLEX
fontsize = 1

def lack_of_face(img, x,y,w,h):
    cv2.putText(img, 'Age: Not calculated', (x+w,y+(15*fontsize)), font, fontsize, (0,0,0), 2)
    cv2.putText(img, 'Gender: Not calculated', (x+w,y+(40*fontsize)), font, fontsize, (0,0,0), 2)
    cv2.putText(img, 'Emotion: Not calculated', (x+w,y+(65*fontsize)), font, fontsize, (0,0, 0), 2)
    return img

def face_estimations(img, face, x, y, w ,h):
    cv2.putText(img, 'Age: '+ str(face.age), (x+w,y+(15*fontsize)), font, fontsize, (0,0,0), 2)
    cv2.putText(img, 'Gender: '+ str(face.gender), (x+w,y+(40*fontsize)), font, fontsize, (0,0,0), 2)
    cv2.putText(img, 'Emotion: ' + str(face.emotion_certainty) +' ' + str(face.emotion), (x+w,y+(65*fontsize)), font, fontsize, (0,0, 0), 2)
    return img

def not_estimated(img, x, y, w, h):
    cv2.putText(img, 'Age: Not calculated', (x+w,y+(15*fontsize)), font, fontsize, (0,0,0), 2)
    cv2.putText(img, 'Gender: Not calculated', (x+w,y+(40*fontsize)), font, fontsize, (0,0,0), 2)
    cv2.putText(img, 'Emotion: Not calculated', (x+w,y+(65*fontsize)), font, fontsize, (0,0, 0), 2)
    return img

def missed_face(img):
    cv2.putText(img, 'Missed the face! Try again!', (0, 450), font, 1, (255,0,0), 2)
    return img

def press_space(img):
    cv2.putText(img, 'Press Spacebar to analyse faces', (0, 15), font, 0.5, (0,0,0), 2)
    return img