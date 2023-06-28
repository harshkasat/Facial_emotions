from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.index, name="index"),
    path('video_feed/', views.video_feed, name='video_feed'),
#    path('gen/', views.gen, name='gen'),
    path('get_emotions/', views.get_emotions, name='get_emotions'),

]