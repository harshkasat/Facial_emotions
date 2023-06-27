# Create your views here.
from django.shortcuts import render, redirect
from django.http.response import StreamingHttpResponse
from django.core.paginator import Paginator
from . models import Song
from app.camera import VideoCamera
from django.http import JsonResponse
from django.http.response import HttpResponse



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

def gen(camera):
    while True:
        frame, result_emotions = camera.get_frame()
        if frame is None or result_emotions is None:
            continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
               b'Emotion: ' + result_emotions.encode() + b'\r\n\r\n')


def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def get_emotions(request):
	# for results in emotions.
        camera = VideoCamera()
        result_emotions = camera.result_emotions()
        if result_emotions is None:
             return HttpResponse(status =204)
        return JsonResponse({"result_emotions":result_emotions})