import logging

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.storage import default_storage as storage
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)

# Getting rid of annoying logs.
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('PIL').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

# Create your models here.


def get_file_path(instance, filename):
    folder_name = 'profile_images/'
    return get_file_path_folder(instance, folder_name, filename)


class UserManager(BaseUserManager):
    """
    Custom User Manager for Custom User
    """
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
    """
    Custom User for authenticating users via email, not username.
    """
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
        default=True,
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


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to=get_file_path)

    def save(self, *args, **kwargs):
        """Resizing images on local storage.
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
        return f'Profile#{self.id} of {self.user.username}#{self.user.id}'

    # def save(self, *args, **kwargs):

    #     """ Resizing images on S3.
    #     Hardcoded output_size.
    #     """
    #     super().save(*args, **kwargs)

    #     if not self.image:
    #         return

    #     img_read = storage.open(self.image.name, 'r')
    #     img = Image.open(img_read)

    #     if img.height > 300 or img.width > 300:
    #         extension = os.path.splitext(self.image.name)[1].lower()

    #         if extension in ['.jpeg', '.jpg']:
    #             format = 'JPEG'
    #         if extension in ['.png']:
    #             format = 'PNG'

    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         in_mem_file = io.BytesIO()
    #         img.save(in_mem_file, format=format)
    #         img_write = storage.open(self.image.name, 'w+')
    #         img_write.write(in_mem_file.getvalue())
    #         img_write.close()

    #     img_read.close()