import cv2

def test_webcam(mirror=False, width=600, height=600):
    """ Basic webcam display function, to test the webcam
    """
    cam = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not cam.isOpened():
        raise IOError("Cannot open webcam")
    print("[INFO] Press esc to quit")
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
        ## display image
        try:
            cv2.imshow('my webcam', img)
            cv2.namedWindow('my webcam',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('my webcam', width, height)
            if cv2.waitKey(1) == 27: 
                break  # esc to quit
        except:
            cam.release()
            cv2.destroyAllWindows()
            raise ValueError('Problem displaying the video.')
    cam.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    # Display the camera on the screen
    test_webcam()