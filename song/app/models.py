from django.db import models

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    audio_file = models.FileField(blank=True,null=True)
    paginate_by = 2
    def __str__(self) -> str:
        return self.title

