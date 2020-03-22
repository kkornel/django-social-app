import logging

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import default_storage as storage
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from PIL import Image

from djangoapp.utils import get_file_path_folder

from .tokens import account_activation_token
from .utils import send_email

logger = logging.getLogger(__name__)

# Getting rid of annoying logs.
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('PIL').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


def get_file_path(instance, filename):
    folder_name = 'profile_images/'
    return get_file_path_folder(instance, folder_name, filename)


class UserManager(BaseUserManager):
    """Custom User Manager for Custom User"""
    def create_user(self, email, username, password=None):
        logger.debug('UserManager called.')
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        logger.debug('UserManager saved a new user.')
        return user

    def create_superuser(self, email, username, password):
        logger.debug('UserManager of a superuser called.')
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        logger.debug('UserManager saved a new superuser.')
        return user


class User(AbstractBaseUser):
    """Custom User for authenticating users via email, not username."""
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=20, unique=True)
    last_login = models.DateTimeField('last login', blank=True, null=True)
    is_admin = models.BooleanField(
        'admin status',
        default=False,
        help_text=(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        'active',
        default=False,
        help_text=('Designates whether this user should be treated as active. '
                   'Unselect this instead of deleting accounts.'),
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    """
    REQUIRED_FIELDS must contain all required fields on your user model, 
    but should not contain the USERNAME_FIELD or password 
    as these fields will always be prompted for.
    """
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def send_verification_email(self, request):
        current_site = get_current_site(request)
        subject = 'Activate Your Account - Django Social App'
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        token = account_activation_token.make_token(self)
        message = render_to_string(
            'users/mail_verify_email.html', {
                'user': self.pk,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
        to_email = self.email
        send_email(to_email, subject, message)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    bio = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=40, blank=True)
    image = models.ImageField(default='default.jpg', upload_to=get_file_path)
    follows = models.ManyToManyField('self',
                                     through='Follow',
                                     symmetrical=False,
                                     related_name='followers')

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

    def add_follow(self, user):
        follow, created = Follow.objects.get_or_create(from_user=self,
                                                       to_user=user)
        return follow

    def remove_follow(self, user):
        Follow.objects.filter(from_user=self, to_user=user).delete()
        return

    def get_following(self):
        return self.follows.filter(to_users__from_user=self)

    def get_followers(self):
        return self.followers.filter(from_users__to_user=self)

    def is_following(self, user):
        return user in self.get_following()

    def is_followed_by(self, user):
        return user in self.get_followers()

    def __str__(self):
        return f'Profile#{self.id}.{self.user.username}'


class Follow(models.Model):
    from_user = models.ForeignKey(Profile,
                                  on_delete=models.CASCADE,
                                  related_name='from_users')
    to_user = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name='to_users')

    def __str__(self):
        return f'{self.from_user.user.username}->{self.to_user.user.username}'
