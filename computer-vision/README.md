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
    
## How it works - Short description
Harrcascade a method to create a facial recognition algorithm. The haarcascade algorithm is trained on many positive and negative images, where positive images are images containing a face, whereas negative does not contain faces. The process starts with applying kernels accross the traning images and calculating a lot of features. However this results in and extreme amount of features. Which means that the next step is looking the the significant features for facial recognition, this is done by applying the features to the images and selecting the ones with the least error rate. After a few intermidiate steps the amount of features can be significantly reduced but still have good accuracy. To increase the efficiency of the facial recognition the algorithm uses a *cascade of classifiers*. Instead of applying all features on a window, they are grouped in to stages and applied one-by-one. If the window fails, meaning it does not find a face, it skips it and does not repeat on that window.
The estimation of age, gender and currenct emotion is done through a deepface algorithm. Deepface is a hybrid face recognition model, using *VGG-Face*, *Google FaceNet*, *OpenFace*, *Facebook DeepFace*, *DeepID*, *ArcFace*, *Dlib* and *SFace*. The facial recognition networks are convolutional neural networks which represent faces as vectors. The age is usually around +-4.65 and the gender accuracy is 97.44%. The estimated attributes comes from neural networks trained on the spesific attributes. For example the age estimation is a network with 101 output values, meaning it can estimate age between 0 and 100 years old.

Here is a more detailed explanation for haarcascade:
https://docs.opencv.org/3.4/d2/d99/tutorial_js_face_detection.html

Here is a more detailed explanation for deepface:
https://github.com/serengil/deepface
https://sefiks.com/2019/02/13/apparent-age-and-gender-prediction-in-keras/


**Hardware requirements**
<p>The program was put together an run on a laptop.<br>
The program can be run on a computer with the minimum spesifications:<br>
Processor: Intel Core i3-5005U CPU<br>
Ram: 8.00GB<br>
Platform: Windows x64<br>
Graphic card: None<br>
Disc space: 800 MB<p>
