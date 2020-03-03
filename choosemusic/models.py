from django.db import models
from django.contrib.auth.models import Group, Permission
from django.utils import timezone
from django.conf import settings
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import os, requests, asyncio, time, datetime

# Create your models here.

choosemusic_admin, created = Group.objects.get_or_create(name='choosemusic_admin')
choosemusic_admin.permissions.add(Permission.objects.get(codename="add_einreichung"))
choosemusic_admin.permissions.add(Permission.objects.get(codename="view_einreichung"))
choosemusic_admin.permissions.add(Permission.objects.get(codename="change_einreichung"))
choosemusic_admin.permissions.add(Permission.objects.get(codename="delete_einreichung"))


class Einreichung(models.Model):
    STATUS = [
        ('playlist', 'In der Playlist'),
        ('play', 'Spielt gerade'),
        ('wait', 'Auf Überprüfung warten...'),
        ('passed', 'Schon vorbei'),
        ('forbidden', 'Wurde nicht zugelassen')
    ]
    benutzer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    titel = models.CharField('Titel', max_length=200)
    kuenstler = models.CharField('Künstler', max_length=200)
    dauer = models.IntegerField('Dauer', default=0)
    link = models.CharField('Link', max_length=200, validators=(URLValidator(schemes=["https","http"]),))
    thumbnail = models.CharField('Thumbnail', max_length=100)
    status = models.CharField('Status', max_length=20, choices=STATUS, default="wait")
    timestamp = models.DateTimeField('Hinzugefügt am', auto_now_add=True)
    starttimestamp = models.DateTimeField('Gestartet um', auto_now_add=True)
    endtimestamp = models.DateTimeField('Endet um', auto_now_add=True)

    def getFromAPI(self):
        try:
            from mysite.settings import Youtube_Data_API_v3

            if "&" in self.link:
                self.link = self.link.split("&")[0]

            if "youtu.be" in self.link:
                id = self.link.split("youtu.be/")[1]
                self.link = "https://youtube.com/watch?v="+str(id)
            else:
                id = self.link.split("v=")[1]

            requestlink = ("https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id="+str(id)+"&key="+str(Youtube_Data_API_v3))
            requestlink2 = ("https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id="+str(id)+"&key="+str(Youtube_Data_API_v3))

            r = requests.get(requestlink)
            r2 = requests.get(requestlink2)

            vid = dict(r.json())['items'][0]['snippet']
            vid2 = dict(r2.json())['items'][0]['contentDetails']

            if "M" in vid2["duration"] and "S" in vid2["duration"]:
                dauer = [vid2['duration'][2::].split("M")[0],vid2['duration'][2::].split("M")[1].split("S")[0]]
            elif "M" in vid2["duration"]:
                dauer = [vid2["duration"][2::].split("M")[0],0]
            elif "S" in vid2["duration"]:
                dauer = [0,vid2["duration"][2::].split("S")[0]]

            self.dauer = int(dauer[0])*60+int(dauer[1])+1
            # self.beschreibung = vid['description']
            self.thumbnail = vid['thumbnails']['default']['url']
            self.titel = vid['title']
            self.kuenstler = vid['channelTitle']
        except IndexError:
            self.titel = "Ungültiger Link!"

    def checkAPIwasSuccessful(self):
        if self.titel == "Ungültiger Link!":
            self.delete()

    def play(self):
        if self.status == "playlist":
            self.status = "play"
            self.starttimestamp = datetime.datetime.now()
            self.endtimestamp = datetime.datetime.now()+datetime.timedelta(seconds=self.dauer-1)
            self.save()
            print("Spielt nun: "+self.titel)

    def has_ended(self):
        if self.status == "play" and (datetime.datetime.now().replace(tzinfo=None) - self.endtimestamp.replace(tzinfo=None)).seconds > 0:
            self.status = "passed"
            self.save()
            print("Fertig gespielt: "+self.titel)
            return True
        else:
            return False

    def __str__(self):
        return self.titel

    __str__.short_description = 'Einreichung'

    class Meta:
        verbose_name = "Einreichung"
        verbose_name_plural = "Einreichungen"


def pre_model_created_or_updated(sender, **kwargs):
    instance = kwargs['instance']
    instance.getFromAPI()

def post_model_created_or_updated(sender, **kwargs):
    instance = kwargs['instance']
    instance.checkAPIwasSuccessful()

models.signals.pre_save.connect(pre_model_created_or_updated, sender=Einreichung)
models.signals.post_save.connect(post_model_created_or_updated, sender=Einreichung)
