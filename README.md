# AI Exhibition Summer Internship Instructions

Welcome to the AI Exhibition project repo. You will find here a description of the project. The machine learning demos prepared for the exhibition are inside the folders. The name of each folder gives you an idea of the content. Each demo has its own description and open source code. Most of them uses Python and additional Python modules, specified in the `requirements.txt` file.

A list of demos planned for the exibition is written on [DemoDescription.md].

## Background
Artificial intelligence (AI) and machine learning (ML) methods are becoming increasingly important in many aspects of society. This technology is already used daily in many consumer products, such as  mobile phones, self-driving cars, cameras. Also it is increasingly explored for industrial applications, for instance in the health-care, energy and maritime domains. 

The UiT Machine Learning Group has over many years built a unique team of top competent researchers within artificial intelligence (AI) and deep learning for image analysis. The group was recently acknowledged national status as Center for Research-based Innovation (SFI) Visual Intelligence, by the Research Council of Norway. The research activity is focused within basic machine learning and computer vision method development, as well as towards applications within the health-care, energy and maritime industry. 

Outreach is an important key-activity for the research group, as it is important to educate and create awareness among the public about the research activity and frontier of technology. Together with the Science Center of Northern Norway (Vitensenteret), the UiT Machine Learning Group, and SFI Visual Intelligence aim to develop a permanent AI exhibition, where guests can interact with, and learn about, machine learning and artificial intelligence. The exhibition will consist of multiple interactive machine learning applications, demonstrations and games that leverage computer vision as a key component.

## Aim of the internships
Construct software demonstrations suitable for the AI exhibition at the Science Center. If the project succeeds, and we are granted the appropriate funding, the software will be implemented in the planned AI exhibition at the Science Center in Tromsø. It will be on public display, and used daily by the visitors of the exhibition. The names of the software creators will be displayed in the exhibition.

## Target audience
Primary:
- Children below 10 years of age

Secondary:
- Children above 10 years of age, and adults

## Concept and hardware
The AI exhibition will consist of four interactive stations positioned back-to-back, in the shape of a square. Each interactive station is equipped with a large 65” touch screen (140cm heigh, 80cm wide), and identical input sensors (web-camera, microphone, keyboard etc). Each screen will be connected to one computer, preferably a standard “of-the-shelf” desktop computer (Linux/Windows/Mac). One of the tasks of the internship is to set up a more specific hardware requirement for the developed software.

## Software 
The content on the four interactive stations should be app-based, where the user can select demonstrations from a given topic. Each consolle should be dedicated to one of the following four topics: Computer vision, Art/drawing, Music and Games, as described in detail below. However, the content of each consolle should also be flexible, with the possibility to be changed, depending on the user demands, or usage. 

The following list presents suggestions to hands-on demonstrations that can be displayed on each of the four interactive consoles. These apps are published under open source license, meaning that it is allowed to use them for commercial use in the Science Center. 

### Computer Vision
- Face recognition from camera with classification of age, gender and mood: https://github.com/SFI-Visual-Intelligence/MLdemos_with_webcam
- Avatarify:  
https://github.com/alievk/avatarify-desktop
- GAN celebrity interpolation: 
https://youtu.be/djsEKYuiRFE
- Explore what a neural network sees: https://experiments.withgoogle.com/what-neural-nets-see

### Art/drawing
- Turn picture into artline:
https://github.com/vijishmadhavan/ArtLine
- Demos in colab: (style transfer and Nemo voice Swap)
https://colab.research.google.com/?utm_source=scs-index#scrollTo=P-H6Lw1vyNNd The idea for us is to do style transfer where one of the pictures is a photo taken from a webcam. A sort of "AI photo booth"
- Quickdraw: 
https://quickdraw.withgoogle.com/
- Draw together with a neural network:
https://magenta.tensorflow.org/assets/sketch_rnn_demo/index.html and https://github.com/magenta/magenta-js/tree/master/sketch
- Dale 1 / 2.
https://openai.com/dall-e-2/
- exchange face with a celebrity (needs GPUs, probably too much GPU power for us)
https://github.com/iperov/DeepFaceLive

### Music
- Music generation
https://openai.com/blog/jukebox/
- Freddiemeter:
https://freddiemeter.withyoutube.com/
- AI duett (possibly use an with an external piano-keyboard)
https://experiments.withgoogle.com/ai/ai-duet/view/

### Games
- Emoji-hunt (Possibly limited to emojis representing faces and body positions?)
https://emojiscavengerhunt.withgoogle.com/
- Play Pacman with your camera https://storage.googleapis.com/tfjs-examples/webcam-transfer-learning/dist/index.html
- Text generation:
https://app.inferkit.com/demo

## Tasks to be solved

### Primary tasks
In order of priority.
1. Construct four AI demonstrations, preferably one within each of the four topics:
- Computer vision (Face recognition and age/mood classification is ~mandatory)
- Art/drawing
- Music
- Games

Each to be run on one of the four interactive touch-screen-based workstations. Use the list above for inspiration, but feel free to search for other demonstrations online as well. The code shall be in Python, preferably using PyTorch or Tensorflow packages.

2. Backup the code to the public Github repository of the project. The code shall be easy to follow, well commented, so that any person with basic programming knowledge can understand the code.  
3. Write a documentation/readme file to the code, that describes the functionality, the useage, limitations, and examples of use. Include a specific hardware requirement for the developed software (Platform, processor, RAM, graphic card, disc space)
4. Design a poster of the underlying theoretical method (ML/DL theory). The poster will be displayed next to the touch screen. It shall give a background understanding to the neural networks and mathematical methods that the current demonstration is build upon.

### Secondary tasks
When the above tasks (1-4) have been completed for four demonstrations, the following tasks may be solved.

5. Continue the implementation of additional demonstrations within each topic, following steps 1-4 above.
6. Design a simple “app”-based touch-screen-friendly graphical user interface (GUI), where the users can choose a specific demonstration on the touch screen. This is useful if we would like to allow users to run several demonstrations on each workstation. The GUI should “lock” the computer, so that background apps are not accessible to the users (visitors at the Science Center), only to the computer admin.  

