# Computer Vision 
### using opencv´s haarcascade face recognizer in conjunction with deepface´s analyzing features.

---
## What is this?

This program uses two different premade machine learning algorithms to first detect a face and display the name of the person, then another algorithm will analyze each face it sees and display a predicted *age*, *gender* and *emotion* to this face.

## Setup

There are a few libraries needed to run the programme, we recommend using a `python venv` with the command `python -m venv venv`. Installing requirements using the following command in the directory:

```bash
$ pip install -r requirements.txt
```

## Usage

1. **Recording a face.**
    First off, the face recognition model will need to take some images of each person and quickly train its weights for each registered person. This can be done from the command line using the command:
    ```bash
    $ python record_user_face.py
    ```

    This will display a video feed from the built-in camera, and once a face is detected the script will capture 90 images of any face in the frame. **It is important there is only one person infront of the camera each time the script has been executed.** To record multiple users, execute the script again.
2. **Training the model.**
    Whenever a new user is recorded, for the algorithm to be able to detect them and correctly classify their names, the algorithm needs to be trained again. It is possible to record multiple users faces before training the model. Use command

    ```bash
    $ python train_face_recognition.py
    ```

    This will take a few seconds.

3. **Testing the full programme**
    All that is now left is to execute
    
    ```bash
    $ python face_detector.py
    ```

    A videofeed will be displayed and the model will try to recognize all faces in the frame. At this point the face analysis algorithm will also come into play, and once every few seconds the camera will freeze for a few seconds analyzing all detected faces in the videofeed.

**Hardware requirements**
<p>The program was put together an run on a laptop.<br>
The program can be run on a computer with the minimum spesifications:<br>
Processor: Intel Core i3-5005U CPU<br>
Ram: 8.00GB<br>
Platform: Windows x64<br>
Graphic card: None<br>
Disc space: 800 MB<p>
