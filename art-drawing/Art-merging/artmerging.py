
import functools
import os

from matplotlib import gridspec
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import buttons

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
options_list = ['Bonfire style', 'Abstarct painting style', 'Colorful blue painting style', 'Colorful painting style', 'Grey abstract painting style', 'Grey shadow painting style', 'Scream painting style', 'Starry night painting style', 'Waves art style', 'Lightning style\n']
for number, option in enumerate(options_list):
  print(number+1, ': ', option)


# print('1: Bonfire style')
# print('2: Abstarct painting style')
# print('3: Colorful blue painting style')
# print('4: Colorful painting style')
# print('5: Grey abstract painting style')
# print('6: Grey shadow painting style')
# print('7: Scream painting style')
# print('8: Starry night painting style')
# print('9: Waves art style')
# print('10: Lightning style\n')
style_number = buttons.chosen_option()


# style_number = getIntegers(style_type)
if style_number > len(options_list) + 1 or style_number < 1:
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

