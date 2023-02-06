from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    pwd = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class File_Upload(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    file_field = models.FileField(upload_to="")

    def __str__(self):
        return self.title