from django.db import models
from django.utils import timezone

from djangoapp.utils import get_file_path_folder
from users.models import Profile

# Create your models here.


def get_file_path(instance, filename):
    folder_name = 'posts_images/'
    return get_file_path_folder(instance, folder_name, filename)


class Post(models.Model):
    author = models.ForeignKey(Profile,
                               on_delete=models.CASCADE,
                               related_name='posts')
    content = models.TextField(max_length=280)
    date_posted = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=40, blank=True)
    image = models.ImageField(upload_to=get_file_path, blank=True)
