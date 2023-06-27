import cv2,os,urllib.request
import numpy as np
from django.conf import settings
from app.ml_model import inference, detection_preprocessing
from django.http import HttpResponseServerError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0, cv2.CAP_MSMF)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()
		result_emotions = ""
		if not success :
			return None, None
		emotions = {
			0: ['Angry', (0, 0, 255), (255, 255, 255)], 
			1: ['Disgust', (0, 102, 0), (255, 255, 255)],
			2: ['Fear', (255, 255, 153), (0, 51, 51)],
			3: ['Happy', (153, 0, 153), (255, 255, 255)],
			4: ['Sad', (255, 0, 0), (255, 255, 255)],
			5: ['Surprise', (0, 255, 0), (255, 255, 255)],
			6: ['Neutral', (160, 160, 160), (255, 255, 255)],
		}
		frame, faces, pos, l, result_emotions = inference(image)
		
		# print(result_emotions)

		
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
		# frame_flip = cv2.flip(frame,1)
		new_width = 500
		new_height = 500
		# Resize the image
		resized_image = cv2.resize(frame, (new_width, new_height))
		ret, jpeg = cv2.imencode('.jpg', resized_image)
		return jpeg.tobytes(), result_emotions
	

	def result_emotions(self):
		success, image = self.video.read()
		if image is None:
			return None
		emotions = {
			0: ['Angry', (0, 0, 255), (255, 255, 255)], 
			1: ['Disgust', (0, 102, 0), (255, 255, 255)],
			2: ['Fear', (255, 255, 153), (0, 51, 51)],
			3: ['Happy', (153, 0, 153), (255, 255, 255)],
			4: ['Sad', (255, 0, 0), (255, 255, 255)],
			5: ['Surprise', (0, 255, 0), (255, 255, 255)],
			6: ['Neutral', (160, 160, 160), (255, 255, 255)],
		}
		frame, faces, pos, l, result_emotions = inference(image)


		return result_emotions
