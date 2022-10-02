import fastai 
from fastai.vision import * 
from fastai.utils.mem import * 
from fastai.vision import open_image, load_learner, image, torch 
import numpy as np 
import urllib.request 
import PIL.Image 
from io import BytesIO 
import torchvision.transforms as T 
from PIL import Image 
import requests 
from io import BytesIO 

import cv2
import matplotlib.pyplot as plt
import os

path = '.'

# Download the neural net weights if they are not already downloaded
colorNNweightsfile = os.path.join(path, 'Toon-Me_820.pkl')
if not os.path.isfile(colorNNweightsfile):
    print('Downloading weights for color neural network...')
    url = 'https://www.dropbox.com/s/6k4bdq5lessc53e/Toon-Me_820.pkl?dl=1'
    r = requests.get(url, allow_redirects=True)
    open(colorNNweightsfile, 'wb').write(r.content)

greyNNweightsfile = os.path.join(path, 'ArtLine_920.pkl')
if not os.path.isfile(greyNNweightsfile):
    print('Downloading weights for greyscale neural network...')
    url = 'https://www.dropbox.com/s/04suaimdpru76h3/ArtLine_920.pkl?dl=1'
    r = requests.get(url, allow_redirects=True)
    open(greyNNweightsfile, 'wb').write(r.content)

cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 

cap_pic = True

while cap_pic == True: #camerafeed
    ret,frame = cap.read() 
    cv2.imshow('Press spacebar to capture image',frame) #display the video image
    k = cv2.waitKey(33)
    if k == 32: #capture image on pressing spacebar 
        cv2.imwrite('original_img.jpg',frame)   #save frame
        cap.release()
        cv2.destroyAllWindows()
        cap_pic = False
        break
    else:
        pass




 

class FeatureLoss(nn.Module): 
    """
    Class is made by creator of ToonMe and has been not edited by us
    """

    def __init__(self, m_feat, layer_ids, layer_wgts): 

        super().__init__() 

        self.m_feat = m_feat 

        self.loss_features = [self.m_feat[i] for i in layer_ids] 

        self.hooks = hook_outputs(self.loss_features, detach=False) 

        self.wgts = layer_wgts 

        self.metric_names = ['pixel', ] + [f'feat_{i}' for i in range(len(layer_ids)) 

                                           ] + [f'gram_{i}' for i in range(len(layer_ids))] 

    def make_features(self, x, clone=False): 

        self.m_feat(x) 

        return [(o.clone() if clone else o) for o in self.hooks.stored] 

    def forward(self, input, target): 

        out_feat = self.make_features(target, clone=True) 

        in_feat = self.make_features(input) 

        self.feat_losses = [base_loss(input, target)] 

        self.feat_losses += [base_loss(f_in, f_out)*w 

                             for f_in, f_out, w in zip(in_feat, out_feat, self.wgts)] 

        self.feat_losses += [base_loss(gram_matrix(f_in), gram_matrix(f_out))*w**2 * 5e3 

                             for f_in, f_out, w in zip(in_feat, out_feat, self.wgts)] 

        self.metrics = dict(zip(self.metric_names, self.feat_losses)) 

        return sum(self.feat_losses) 

    def __del__(self): self.hooks.remove() 

 

def add_margin(pil_img, top, right, bottom, left, color): 

    width, height = pil_img.size 

    new_width = width + right + left 

    new_height = height + top + bottom 

    result = Image.new(pil_img.mode, (new_width, new_height), color) 

    result.paste(pil_img, (left, top)) 

    return result 


path = '.'

img = PIL.Image.open('original_img.jpg').convert("RGB") #get captured image

im_new = add_margin(img, 150, 150, 150, 150, (255, 255, 255)) #add margin to image

im_new.save("test.jpg", quality=95)     #save version with margin

img = open_image("test.jpg") 



def comicstyle_blackwhite(img):
    """Function generates comic style image
    Input:
        Image captured or loaded
    returns:
        comic style black and white image 
    """
    learn = load_learner(path, 'ArtLine_920.pkl')    #load learner from comicstyle model

    p, img_hr, b = learn.predict(img)   #create comicstyle image
    x = np.minimum(np.maximum(image2np(img_hr.data*255), 0), 255).astype(np.uint8) 

    PIL.Image.fromarray(x).save("comic_style_blackwhite.jpg", quality=95) #save image
    

def comicstyle_color(img_taken):
    """Function generates comic style colored image
    Input:
        Image captured or loaded
    returns:
        comic style colored image 
    """
    comicstyle_blackwhite(img_taken)    #generate grey comicstyle image
    blackwhite_img = open_image('comic_style_blackwhite.jpg') 
    
    learn_c = load_learner(path, 'Toon-Me_820.pkl') #load color model
    p, img_hr, b = learn_c.predict(blackwhite_img)   #adds color to comicstyle image
    
    x = np.minimum(np.maximum(image2np(img_hr.data*255), 0), 255).astype(np.uint8) 
    PIL.Image.fromarray(np.asarray(x)).save("comic_style_color.jpg", quality=95) #save image

def run_style(image_taken, color=False):
    """Function runs the algorithm and displays image
    Input: 
        Image captured or loaded
    Returns:
        Nothing
    """
    if color == False:
        comicstyle_blackwhite(image_taken)
        display_img = cv2.imread('comic_style_blackwhite.jpg')

    if color == True:
        comicstyle_color(image_taken)
        display_img = cv2.imread('comic_style_color.jpg')

    while True:
        cv2.imshow('Cartoonstyle image | press esc to exit | press s to save image', display_img)   #show image
        k = cv2.waitKey(5) & 0xff # Press 'ESC' for exiting video
        if k == ord('s'):   #save image by pressing s
            cv2.imwrite('Comicstyle_image.jpg', display_img)
        if k == 27:
            if color == False:  #remove images
                os.remove('comic_style_blackwhite.jpg')
            if color == True:
                os.remove('comic_style_color.jpg')
            break


print('Do you want colored image?')
awnser = input('Enter \'color\' for colored or \'grey\' for black and white: ')
if awnser == 'color':
    print('Please wait a moment while the image is being made')
    run_style(img, color=True) 
    os.remove('original_img.jpg')
    os.remove('test.jpg') #removes images used in between generating comicstyle images

if awnser == 'grey':
    print('Please wait a moment while the image is being made')
    run_style(img) 
    os.remove('original_img.jpg')
    os.remove('test.jpg') #removes images used in between generating comicstyle images

if awnser != 'color' and awnser != 'grey':
    print('You did not enter a correct option!')



