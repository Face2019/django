from django.db import models
from django.utils import timezone
from picklefield.fields import PickledObjectField
#from db_helpers.example_models import ExampleFaceElements

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Photos(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    input_photo = models.TextField()
    photo_in_rgb = PickledObjectField(blank=True,
                                      null=True)
    number_of_detected_faces = models.IntegerField()
    face_landmarks = models.TextField(default=None,
                                      blank=True,
                                      null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    PHOTOS_STR_FORMAT = "{id} | {date}"

    def __str__(self):
        return self.PHOTOS_STR_FORMAT.format(id=self.id, date=self.timestamp.strftime("%d-%m-%Y %H:%M:%S"))



class ExampleLips(models.Model):
    model_id = models.AutoField(primary_key=True, unique=True)
    image_name = models.CharField(max_length=100)
    image_in_base_64 = models.TextField()
    rgb_numpy = PickledObjectField()
    face_landmarks = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    PHOTOS_STR_FORMAT = "{name} | {date}"

    def __str__(self):
        return self.PHOTOS_STR_FORMAT.format(name=self.image_name, date=self.timestamp.strftime("%d-%m-%Y %H:%M:%S"))

class ExampleNoses(models.Model):
    model_id = models.AutoField(primary_key=True, unique=True)
    image_name = models.CharField(max_length=100)
    image_in_base_64 = models.TextField()
    rgb_numpy = PickledObjectField()
    face_landmarks = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    PHOTOS_STR_FORMAT = "{name} | {date}"

    def __str__(self):
        return self.PHOTOS_STR_FORMAT.format(name=self.image_name, date=self.timestamp.strftime("%d-%m-%Y %H:%M:%S"))
