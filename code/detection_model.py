import glob

import numpy as np
import tensorflow as tf
from keras import applications
from keras.applications.inception_v3 import (decode_predictions,
                                             preprocess_input)
from keras.layers import Dense, Dropout, GlobalAveragePooling2D
from keras.preprocessing import image
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

def modelPrediction(input_img, img_height, img_width, num_classes,class_names, logger):
    model = Sequential([
    layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes)
    ])
   
    try:
        model.load_weights('../models/model.h5')
    except:
        logger.exception("ISSUE WHEN LOADING MODEL")
        return "NA", "NA", "E50063"


    img_path = input_img
    try:
        img = keras.preprocessing.image.load_img(img_path, target_size=(img_height, img_width))
    except:
        logger.exception("IMAGE NOT FOUND")
        return "NA", "NA","E50064"

    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
 
    out_label = class_names[np.argmax(score)]
  
    freshness = out_label.split('_')
    return out_label , freshness , "L20037"
