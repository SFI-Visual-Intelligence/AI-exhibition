import cv2

font = cv2.FONT_HERSHEY_SIMPLEX
fontsize = 1

def lack_of_face(img, x,y,w,h):
    cv2.putText(img, '.', (x+w,y+(15*fontsize)), font, fontsize, (0,0,0), 2)
    return img

def face_estimations(img, face, x, y, w ,h):
    #cv2.putText(img, 'Age: '+ str(face.age), (x+w,y+(15*fontsize)), font, fontsize, (0,0,0), 2)
    #cv2.putText(img, str(face.gender), (x+w,y+(40*fontsize)), font, fontsize, (0,0,0), 2)
    cv2.putText(img, 'Sad: ' + str(face.emotions['sad']), (x+w,y+(15*fontsize)), font, fontsize, (0,0, 0), 2)
    cv2.putText(img, 'Surprise: ' + str(face.emotions['surprise']), (x+w,y+(45*fontsize)), font, fontsize, (0,0, 0), 2)
    cv2.putText(img, 'Angry: ' + str(face.emotions['angry']), (x+w,y+(65*fontsize)), font, fontsize, (0,0, 0), 2)
    cv2.putText(img, 'Happy: ' + str(face.emotions['happy']), (x+w,y+(95*fontsize)), font, fontsize, (0,0, 0), 2)
    cv2.putText(img, 'Fear: ' + str(face.emotions['fear']), (x+w,y+(125*fontsize)), font, fontsize, (0,0, 0), 2)
    return img

def not_estimated(img, x, y, w, h):
    cv2.putText(img, '.', (x+w,y+(15*fontsize)), font, fontsize, (0,0,0), 2)
    return img

def clear_text(img, x, y, w, h):
    cv2.putText(img, '.', (x+w,y+(15*fontsize)), font, fontsize, (0,0,0), 2)
    cv2.putText(img, '.', (x+w,y+(40*fontsize)), font, fontsize, (0,0,0), 2)
    cv2.putText(img, '.', (x+w,y+(65*fontsize)), font, fontsize, (0,0, 0), 2)
    cv2.putText(img, '.', (x+w,y+(95*fontsize)), font, fontsize, (0,0, 0), 2)
    return img

def missed_face(img):
    cv2.putText(img, 'Missed the face! Try again!', (0, 450), font, 1, (255,0,0), 2)
    return img

def press_space(img):
    cv2.putText(img, 'Press Spacebar to analyse faces', (0, 15), font, 0.5, (0,0,0), 2)
    return img

def countdown(img, x, y, w, h, time):
    cv2.putText(img, f'{time:.1f}', (x+w,y+(15*fontsize)), font, fontsize, (0,0,0), 2)
    return img
