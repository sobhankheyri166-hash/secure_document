from django.db import models
from django.templatetags.static import static
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    @property
    def profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return static('images/logos/default_user_profilepic.png')


    def __str__(self):
        return self.get_full_name() or self.username


class Request(models.Model):
    class FileTypeChoice(models.TextChoices):
        Image = 'IMAGE', 'Image'
        Document = 'DOCUMENT', 'Document'
        Other_Types = 'OTHER_TYPES', 'Other Types'
    class StatusChoices(models.TextChoices):
        Answered = 'ANSWERED', 'Answered'
        Sent = 'SENT', 'Sent'
        Not_Sent = 'NOT_SENT', 'Not Sent'
        Seen = 'SEEN', 'Seen'
    name = models.CharField(max_length=80)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    response_status = models.CharField(
        max_length=12,
        choices=StatusChoices,
        default=StatusChoices.Not_Sent)
    file_type = models.CharField(
        max_length=12,
        choices=FileTypeChoice, 
        default=FileTypeChoice.Other_Types)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='file_request')


class File(models.Model):
    file = models.FileField(upload_to='docs/', validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','pdf','zip'])])
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
