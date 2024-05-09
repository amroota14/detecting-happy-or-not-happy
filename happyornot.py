# -*- coding: utf-8 -*-
"""happyORnot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MHk2tQlHRnx95nstmayA8xtXuNLv-8Xy
"""

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.preprocessing import image

# Define the paths for training, validation, and testing datasets
train_dir = "/content/drive/MyDrive/detection_dataset/base_data/training"
validation_dir = "/content/drive/MyDrive/detection_dataset/base_data/validation"
test_dir = "/content/drive/MyDrive/detection_dataset/base_data/testing"

# Data preprocessing and augmentation for training and validation datasets
train_datagen = ImageDataGenerator(rescale=1.0/255)
validation_datagen = ImageDataGenerator(rescale=1.0/255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(200, 200),
    batch_size=3,
    class_mode='binary'
)

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(200, 200),
    batch_size=3,
    class_mode='binary'
)

# Define the CNN model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(200, 200, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001),
              metrics=['accuracy'])

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=3,
    epochs=30,
    validation_data=validation_generator
)

# Save the trained model to disk
model.save('/content/drive/MyDrive/trained_model.h5')

model = tf.keras.models.load_model('/content/drive/MyDrive/trained_model.h5')  # Replace with your model file path

img_path = '/content/drive/MyDrive/detection_dataset/base_data/testing/13.jpg'  # Replace with your test image path

def predict_image(model, img_path):
    print(f"Processing image: {img_path}")

    # Load and preprocess the image
    img = image.load_img(img_path, target_size=(200, 200))  # Adjust target_size as needed
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Expand dimensions to create batch size of 1 .0
     # Normalize pixel values (assuming model expects inputs in [0, 1] range)
    img_array = img_array / 255
    # Perform prediction
    predictions = model.predict(img_array)

    # Assuming model predicts class probabilities, get the predicted class
    predicted_class_idx = np.argmax(predictions)
    class_labels = ['happy', 'not happy']  # Example class labels

# Display the image with prediction
    plt.imshow(img)
    plt.axis('off')
    predicted_class_label = class_labels[predicted_class_idx]
    plt.title(f"Predicted: {predicted_class_label}", fontsize=14, weight='bold', color='green')
    plt.show()

# Example usage:
# Replace 'model_path' with the path to your trained model file (.h5 or .hdf5)
model_path = '/content/drive/MyDrive/trained_model.h5'
# Load your trained model
model = tf.keras.models.load_model(model_path)

# Directory containing test images
test_image_dir = "/content/drive/MyDrive/detection_dataset/base_data/testing"

if not os.path.exists(test_image_dir):
    print(f"Directory '{test_image_dir}' does not exist.")
    exit()

# Iterate over each file in the directory
for filename in os.listdir(test_image_dir):
    img_path = os.path.join(test_image_dir, filename)

    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Perform prediction and display the image with prediction
        predict_image(model, img_path)
    else:
        print(f"Skipping non-image file: {img_path}")

print("Prediction process completed.")

