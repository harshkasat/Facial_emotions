# Generated by Django 4.2.2 on 2023-06-24 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='file',
        ),
        migrations.AddField(
            model_name='song',
            name='audio_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='song',
            name='audio_link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]