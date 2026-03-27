from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
    pass
    def __str__(self):
        return self.get_full_name() or self.username


class Request(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class File(models.Model):
    file = models.FileField(upload_to='docs/',validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','pdf','zip'])])
    request = models.ForeignKey(Request,on_delete=models.CASCADE)
