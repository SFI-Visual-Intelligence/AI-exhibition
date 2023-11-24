import cv2

def test_webcam(mirror=False, width=1080, height=1920):
    """ Basic webcam display function, to test the webcam
    """
    cam = cv2.VideoCapture(1)
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(width, height)

    # change the size
    cam.set(3, width) # set video width
    cam.set(4, height) # set video height


    # Check if the webcam is opened correctly
    if not cam.isOpened():
        raise IOError("Cannot open webcam")
    print("[INFO] Press esc to quit")
    while True:
        ret_val, img = cam.read()
        #if mirror: 
        #    img = cv2.flip(img, 1)
        ## display image
        try:
            # img = cv2.resize(img,(int(1080),int(1920)))
            img=cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE) # portrait
            img = cv2.resize(img, (img.shape[1] * 2, img.shape[0] * 2))
            #img = cv2.flip(img, 1)
            cv2.imshow('my webcam', img)
            #img = textdisplays.press_space(img)
            #cv2.resizeWindow('my webcam', int(width), height)
            #cv2.namedWindow('my webcam', cv2.WND_PROP_FULLSCREEN)
            #cv2.setWindowProperty(1, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            if cv2.waitKey(1) == 27: 
                break  # esc to quit
        except Exception as e:
            cam.release()
            cv2.destroyAllWindows()
            print(e)
            raise e
    cam.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    # Display the camera on the screen
    test_webcam()