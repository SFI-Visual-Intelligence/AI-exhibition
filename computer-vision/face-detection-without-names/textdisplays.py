from re import error
import cv2

font = cv2.FONT_HERSHEY_SIMPLEX
fontsize = 1


def lack_of_face(img, x,y,w,h):
    cv2.putText(img, '.', (x+w,y+(15*fontsize)), font, fontsize, (0,0,0), 2)
    return img


def face_estimations(img, face, x, y, w ,h):



    bar_length = 100
    txt_col = (255, 0, 255)
    bar_col = (255, 0, 255)

    max_txt_x = 0
    max_txt_y = 0
    for key in face.emotions.keys():
        size, _ = cv2.getTextSize(f'{key}: ', font, fontsize, 2)
        x_size, y_size = size

        if x_size > max_txt_x:
            max_txt_x = x_size

        elif y_size > max_txt_y:
            max_txt_y = y_size

    y_spacing = int(1.5 * max_txt_y)
    bar_xshift = int(max_txt_x * 1)

    for i, (emotion, val) in enumerate(face.emotions.items()):
        y_shift = (i+1) * y_spacing * fontsize
        scale_val = val / 100
        bar_xstretch = int(scale_val * bar_length)
        cv2.putText(img, f'{emotion}: ', (x + w, y+y_shift), font, fontsize, bar_col, 2)
        cv2.rectangle(img, (x+w+bar_xshift, y+y_shift-max_txt_y), (x+w+bar_xshift+bar_xstretch, y+y_shift), color=bar_col, thickness=-1)
        cv2.rectangle(img, (x+w+bar_xshift, y+y_shift-max_txt_y), (x+w+bar_xshift+bar_length, y+y_shift), color=(0,0, 0), thickness=4)

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


if __name__ == "__main__":
    pass