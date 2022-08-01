# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3
#     name: python3
# ---

# + [markdown] id="ScitaPqhKtuW"
# ##### Copyright 2019 The TensorFlow Hub Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");

# + id="jvztxQ6VsK2k"
# Copyright 2019 The TensorFlow Hub Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# + [markdown] id="oXlcl8lqBgAD"
# # Fast Style Transfer for Arbitrary Styles
#

# + [markdown] id="MfBg1C5NB3X0"
# <table class="tfo-notebook-buttons" align="left">
#   <td>
#     <a target="_blank" href="https://www.tensorflow.org/hub/tutorials/tf2_arbitrary_image_stylization"><img src="https://www.tensorflow.org/images/tf_logo_32px.png" />View on TensorFlow.org</a>
#   </td>
#   <td>
#     <a target="_blank" href="https://colab.research.google.com/github/tensorflow/hub/blob/master/examples/colab/tf2_arbitrary_image_stylization.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Run in Google Colab</a>
#   </td>
#   <td>
#     <a target="_blank" href="https://github.com/tensorflow/hub/blob/master/examples/colab/tf2_arbitrary_image_stylization.ipynb"><img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" />View on GitHub</a>
#   </td>
#   <td>
#     <a href="https://storage.googleapis.com/tensorflow_docs/hub/examples/colab/tf2_arbitrary_image_stylization.ipynb"><img src="https://www.tensorflow.org/images/download_logo_32px.png" />Download notebook</a>
#   </td>
#   <td>
#     <a href="https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"><img src="https://www.tensorflow.org/images/hub_logo_32px.png" />See TF Hub model</a>
#   </td>
# </table>

# + [markdown] id="YeeuYzbZcJzs"
# Based on the model code in [magenta](https://github.com/tensorflow/magenta/tree/master/magenta/models/arbitrary_image_stylization) and the publication:
#
# [Exploring the structure of a real-time, arbitrary neural artistic stylization
# network](https://arxiv.org/abs/1705.06830).
# *Golnaz Ghiasi, Honglak Lee,
# Manjunath Kudlur, Vincent Dumoulin, Jonathon Shlens*,
# Proceedings of the British Machine Vision Conference (BMVC), 2017.
#

# + [markdown] id="TaM8BVxrCA2E"
# ## Setup

# + [markdown] id="J65jog2ncJzt"
# Let's start with importing TF2 and all relevant dependencies.

# + id="v-KXRY5XBu2u"
import functools
import os

from matplotlib import gridspec
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import cv2

print("TF Version: ", tf.__version__)
print("TF Hub version: ", hub.__version__)
print("Eager mode enabled: ", tf.executing_eagerly())
print("GPU available: ", tf.config.list_physical_devices('GPU'))


# + id="tsoDv_9geoZn"
# @title Define image loading and visualization functions  { display-mode: "form" }

def crop_center(image):
  """Returns a cropped square image."""
  shape = image.shape
  new_shape = min(shape[1], shape[2])
  offset_y = max(shape[1] - shape[2], 0) // 2
  offset_x = max(shape[2] - shape[1], 0) // 2
  image = tf.image.crop_to_bounding_box(
      image, offset_y, offset_x, new_shape, new_shape)
  return image

@functools.lru_cache(maxsize=None)
def load_image(path, image_size=(256, 256), preserve_aspect_ratio=True):
  """Loads and preprocesses images."""
  # Cache image file locally.
  image_path = path  # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
  img = tf.io.decode_image(
      tf.io.read_file(image_path),
      channels=3, dtype=tf.float32)[tf.newaxis, ...]
  img = crop_center(img)
  img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
  return img

def show_n(images, titles=('',)):
  n = len(images)
  image_sizes = [image.shape[1] for image in images]
  w = (image_sizes[0] * 6) // 320
  plt.figure(figsize=(w * n, w))
  gs = gridspec.GridSpec(1, n, width_ratios=image_sizes)
  for i in range(n):
    plt.subplot(gs[i])
    plt.imshow(images[i][0], aspect='equal')
    plt.axis('off')
    plt.title(titles[i] if len(titles) > i else '')
  plt.show()

def getIntegers(string):
  numbers = [int(x) for x in string.split() if x.isnumeric()]
  return numbers[0]


output_image_size = 384  # @param {type:"integer"}

cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 

cap_pic = True

while cap_pic == True: #camerafeed
    ret,frame = cap.read() 
    cv2.imshow('Press spacebar to capture image',frame) #display the video image
    k = cv2.waitKey(33)
    if k == 32: #capture image on pressing spacebar 
        cv2.imwrite('taken_image.jpg',frame)   #save frame
        cap.release()
        cv2.destroyAllWindows()
        cap_pic = False
        break
    else:
        pass

print('Which image would you like to merge with?')
print('1: Bonfire style')
print('2: Abstarct painting style')
print('3: Colorful blue painting style')
print('4: Colorful painting style')
print('5: Grey abstract painting style')
print('6: Grey shadow painting style')
print('7: Scream painting style')
print('8: Starry night painting style')
print('9: Waves art style')
print('10: Lightning style\n')
style_type = input('Enter the number of the style you want: ')


style_number = getIntegers(style_type)
if style_number > 10 or style_number < 1:
  print('Not an option!')
  raise
content_image1 = 'taken_image.jpg'
style_images = ['images_tomerge/bonfire.jpg', 
                'images_tomerge/abstract_art.jpg', 
                'images_tomerge/blue_color_art.jpg', 
                'images_tomerge/colorful_art.jpg', 
                'images_tomerge/grey_abstract_art.jpg', 
                'images_tomerge/grey_shadow.jpg', 
                'images_tomerge/scream.jpg', 
                'images_tomerge/starry_night_art.jpg', 
                'images_tomerge/waves.jpg',
                'images_tomerge/lightning.jpg']
style_image1 = style_images[style_number - 1]
# The content image size can be arbitrary.
content_img_size = (output_image_size, output_image_size)
# The style prediction model was trained with image size 256 and it's the 
# recommended image size for the style image (though, other sizes work as 
# well but will lead to different results).
style_img_size = (256, 256)  # Recommended to keep it at 256.

content_image = load_image(content_image1, content_img_size)
style_image = load_image(style_image1, style_img_size)
style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')
show_n([content_image, style_image], ['Content image', 'Style image'])

# + [markdown] id="yL2Bn5ThR1nY"
# ## Import TF Hub module

# + id="467AVDSuzBPc"
# Load TF Hub module.

hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
hub_module = hub.load(hub_handle)

# + [markdown] id="uAR70_3wLEDB"
# The signature of this hub module for image stylization is:
# ```
# outputs = hub_module(content_image, style_image)
# stylized_image = outputs[0]
# ```
# Where `content_image`, `style_image`, and `stylized_image` are expected to be 4-D Tensors with shapes `[batch_size, image_height, image_width, 3]`.
#
# In the current example we provide only single images and therefore the batch dimension is 1, but one can use the same module to process more images at the same time.
#
# The input and output values of the images should be in the range [0, 1].
#
# The shapes of content and style image don't have to match. Output image shape
# is the same as the content image shape.

# + [markdown] id="qEhYJno1R7rP"
# ## Demonstrate image stylization

# + id="lnAv-F3O9fLV"
# Stylize content image with given style image.
# This is pretty fast within a few milliseconds on a GPU.

outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
stylized_image = outputs[0]


show_n([content_image, style_image, stylized_image], titles=['Original content image', 'Style image', 'Stylized image'])
os.remove('taken_image.jpg')

