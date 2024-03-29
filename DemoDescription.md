
# Demos for the first exhibition

List of demos planned for the first exhibition, in priority order.

## Demo 1
Face detection
https://github.com/SFI-Visual-Intelligence/AI-exhibition/tree/main/computer-vision/face-detection-without-names
This is a stand alone python script. It uses the webcam and open a window showing the webcam stream with the detected faces inside bounding boxes.
Run on a computer with a webcam and a screen.
Pressing the space bar run the AI analysis: the computation of "gender", "age" and "emotion". It needs a few seconds to update. 
It could run continuously but the image would freeze each time the AI computation run.
- [ ] Maybe displaying a small timer in a corner to show that the computer is processing the values would help the user understand why the emotion does not change immediately when he/she change his/her face.

## Demo 2
Drawing
https://github.com/SFI-Visual-Intelligence/AI-exhibition/tree/main/art-drawing/sketch-rnn-js
This is a javascript code that needs a server and is viewed in a browser.
The user uses the mouse to start drawing and the machine will finish the drawing.
The best would be to run it on a tablet and use the touch screen to draw.
Before drawing, the user has to choose an animal to draw from the (small) list, so that the computer know how to finish it.
- [ ] A button is needed to change the animal and another to erase the screen.

## Demo 3
Style transfer
art-drawing/Art-merging
https://github.com/SFI-Visual-Intelligence/AI-exhibition/tree/main/art-drawing/Art-merging
The user push a button to take a picture from the webcam. The program then ask to choose a style among several ones. After choosing a style, the photo and style image are merged together and displayed.

## Demo 4
Medical images
https://github.com/SFI-Visual-Intelligence/AI-exhibition/tree/main/medical
It consists on displaying the different slices of an MRI scan and other scans like PET.
Initially, the idea was a game to "find the tumor" but we can simplify it to just display the scans, as a start.
- [ ] We need some code to display the data on a screen.
- [ ] We need buttons to scroll across the different slices, vertically and optionally other directions.

## Demo 5
Object-hunt
This is not implemented yet
The computer asks the user to show a particular object to the webcam. The program detects the objects it sees on the webcam and speaks to tell what is the object it recognizes, until the asked object is shown. This will be inspired by Emoji-hunt [https://emojiscavengerhunt.withgoogle.com/](https://emojiscavengerhunt.withgoogle.com/)

## Demo 6 (Optional, instead of Demo 3)
Toon-me
https://github.com/SFI-Visual-Intelligence/AI-exhibition/tree/main/art-drawing/Toon-Me
This is a standalone python script. The script take a picture from the webcam, modify the image to make it cartoon-like and display it on a screen.
A button is needed to start the process (3 step process: taking a picture - computing - displaying the result).
It works on a computer with a webcam.

