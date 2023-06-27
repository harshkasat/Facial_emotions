import numpy as np
import cv2
import time
import glob
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers.experimental.preprocessing import Rescaling
from tensorflow.keras.layers import Conv2D, MaxPool2D, Dense, Dropout, Flatten
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.optimizers import Adam


emotions = {
    0: ['Angry', (0, 0, 255), (255, 255, 255)], 
    1: ['Disgust', (0, 102, 0), (255, 255, 255)],
    2: ['Fear', (255, 255, 153), (0, 51, 51)],
    3: ['Happy', (153, 0, 153), (255, 255, 255)],
    4: ['Sad', (255, 0, 0), (255, 255, 255)],
    5: ['Surprise', (0, 255, 0), (255, 255, 255)],
    6: ['Neutral', (160, 160, 160), (255, 255, 255)]
}
num_classes = len(emotions)
input_shape = (48, 48, 1)
weights_1 = 'Z:\\emotion reco and song playback\\song\\app\\emotionsavedmodel\\vggnet_up.h5'
weights_2 = 'Z:\\emotion reco and song playback\\song\\app\\emotionsavedmodel\\vggnet.h5'


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


class VGGNet(Sequential):
    def __init__(self, input_shape, num_classes, checkpoint_path, lr=1e-3):
        super().__init__()
        self.add(Rescaling(1./255, input_shape=input_shape))
        self.add(Conv2D(64, (3, 3), activation='relu',
                 kernel_initializer='he_normal'))
        self.add(BatchNormalization())
        self.add(Conv2D(64, (3, 3), activation='relu',
                 kernel_initializer='he_normal', padding='same'))
        self.add(BatchNormalization())
        self.add(MaxPool2D())
        self.add(Dropout(0.5))

        self.add(Conv2D(128, (3, 3), activation='relu',
                 kernel_initializer='he_normal', padding='same'))
        self.add(BatchNormalization())
        self.add(Conv2D(128, (3, 3), activation='relu',
                 kernel_initializer='he_normal', padding='same'))
        self.add(BatchNormalization())
        self.add(MaxPool2D())
        self.add(Dropout(0.4))

        self.add(Conv2D(256, (3, 3), activation='relu',
                 kernel_initializer='he_normal', padding='same'))
        self.add(BatchNormalization())
        self.add(Conv2D(256, (3, 3), activation='relu',
                 kernel_initializer='he_normal', padding='same'))
        self.add(BatchNormalization())
        self.add(MaxPool2D())
        self.add(Dropout(0.5))

        self.add(Conv2D(512, (3, 3), activation='relu',
                 kernel_initializer='he_normal', padding='same'))
        self.add(BatchNormalization())
        self.add(Conv2D(512, (3, 3), activation='relu',
                 kernel_initializer='he_normal', padding='same'))
        self.add(BatchNormalization())
        self.add(MaxPool2D())
        self.add(Dropout(0.4))

        self.add(Flatten())

        self.add(Dense(1024, activation='relu'))
        self.add(Dropout(0.5))
        self.add(Dense(256, activation='relu'))

        self.add(Dense(num_classes, activation='softmax'))

        self.compile(optimizer=Adam(learning_rate=lr),
                     loss=categorical_crossentropy,
                     metrics=['accuracy'])

        self.checkpoint_path = checkpoint_path


model_1 = VGGNet(input_shape, num_classes, weights_1)
model_1.load_weights(model_1.checkpoint_path)

model_2 = VGGNet(input_shape, num_classes, weights_2)
model_2.load_weights(model_2.checkpoint_path)




def detection_preprocessing(image, h_max=360):
    h, w, _ = image.shape
    if h > h_max:
        ratio = h_max / h
        w_ = int(w * ratio)
        image = cv2.resize(image, (w_, h_max))
    return image


def resize_face(face):
    x = tf.expand_dims(tf.convert_to_tensor(face), axis=2)
    return tf.image.resize(x, (48, 48))


def recognition_preprocessing(faces):
    x = tf.convert_to_tensor([resize_face(f) for f in faces])
    return x


def inference(image):
    if image is None:
        return None, None, None, None

    H, W, _ = image.shape

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    face_images = []
    pos = []
    l= []
    result_emotions = ""
    if len(faces) > 0:
        
        for (x, y, w, h) in faces:
            x1 = max(0, x)
            y1 = max(0, y)
            x2 = min(x + w, W)
            y2 = min(y + h, H)

            face = gray_image[y1:y2, x1:x2]
            face_images.append(face)
            pos.append((x1, y1, x2, y2))

        x = recognition_preprocessing(face_images)

        y_1 = model_1.predict(x)
        y_2 = model_2.predict(x)
        l = np.argmax(y_1 + y_2, axis=1)

        for i in range(len(face_images)):

            result_emotions = emotions[l[i]][0]
            cv2.rectangle(image, (pos[i][0], pos[i][1]), (pos[i][2], pos[i][3]), emotions[l[i]][1], 2, lineType=cv2.LINE_AA)
            cv2.rectangle(image, (pos[i][0], pos[i][1] - 20), (pos[i][2] + 20, pos[i][1]), emotions[l[i]][1], -1, lineType=cv2.LINE_AA)
            cv2.putText(image, f'{result_emotions}', (pos[i][0], pos[i][1] - 5), 0, 0.6, emotions[l[i]][2], 2, lineType=cv2.LINE_AA)

    return image, faces, pos, l, result_emotions