# Create your views here.
from django.shortcuts import render, redirect
from django.http.response import StreamingHttpResponse
from django.core.paginator import Paginator
from . models import Song
from app.camera import VideoCamera
from django.http import JsonResponse
from django.http.response import HttpResponse
import asyncio
import json
import time
import threading



def index(request):
    All_song = Song.objects.all()
    paginator= Paginator(Song.objects.all(),1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.method == 'POST':
        new_song =Song(
            title = request.POST['title'],
            artist = request.POST['artist'],
            audio_file=request.FILES['new_audio_file'],
            )
        new_song.save()
        return redirect('/')
    return render(request,"index.html",{"page_obj":page_obj,
                                        "all_song":All_song,
					                    })


latest_frame = None
latest_result_emotions = None


def gen(camera,cond = None):
    
    video_camera = VideoCamera() 
    global latest_frame, latest_result_emotions # Create an instance of the VideoCamera class
    while True:
        frame, result_emotions = video_camera.get_frame()
        if frame is None or result_emotions is None:
            continue
        
        latest_frame = frame
        latest_result_emotions = result_emotions
        if cond:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
                b'Emotion: ' + result_emotions.encode() + b'\r\n\r\n')
        else :
            # result_emotions = JsonResponse({"result_emotions":result_emotions})
            return JsonResponse({"result_emotions":result_emotions})
             


def video_feed(request):
    cond = True  # Set the value of cond based on your requirement
    if cond:
        return StreamingHttpResponse(gen(VideoCamera(), cond=cond),
                                     content_type='multipart/x-mixed-replace; boundary=frame')
    else:
        # Obtain the JSON response from gen function and return it as HttpResponse
        # json_response = next(gen(VideoCamera(), cond=cond))
        return JsonResponse({"result_emotions":""})



def get_emotions(request):
    global latest_result_emotions
    if latest_result_emotions is None:
        return JsonResponse({"result_emotions": ""})
    else:
        return JsonResponse({"result_emotions": latest_result_emotions})