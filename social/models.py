from django.db import models
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from djangoapp.utils import get_file_path_folder
from users.models import Profile


def get_file_path(instance, filename):
    folder_name = 'posts_images/'
    return get_file_path_folder(instance, folder_name, filename)


class Post(models.Model):
    # It is 'one to many' relation, because 1 user can have multiple posts.
    # It is done by ForeginKey.
    # on_delete means what happens when user is deleted, CASCADE means delete all his posts.
    author = models.ForeignKey(Profile,
                               on_delete=models.CASCADE,
                               related_name='posts')
    content = models.TextField(max_length=280)
    date_posted = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=40, blank=True)
    image = models.ImageField(upload_to=get_file_path, blank=True)
    likes = models.ManyToManyField(Profile,
                                   blank=True,
                                   through='Like',
                                   related_name='likes')

    def save(self, *args, **kwargs):
        """
        Resizing images on local storage.
        Hardcoded output_size.
        """
        super().save(*args, **kwargs)

        if not self.image:
            return

        img = Image.open(self.image.path)

        if img.height > 510 or img.width > 515:
            # TODO split in 2 mote ifs?
            output_size = (510, 515)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return f'Post#{self.id} by {self.author.user.username}#{self.author.user.id} -> {self.content[:10]}... '

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(Profile,
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(max_length=280)
    date_commented = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment#{self.id} for Post#{self.post.id} by {self.author.user.username}#{self.author.user.id}  -> Content {self.text[:10]}... '


class Like(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_liked = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Like#{self.id} for Post#{self.post.id} by {self.author.user.username}#{self.author.user.id}  -> Content {self.post.content[:10]}... '
