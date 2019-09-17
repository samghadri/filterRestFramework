from django.db import models

# Create your models here.

class Person(models.Model):

    name = models.CharField(max_length=100)

    job_title = models.CharField(max_length=100)

    telephone = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return self.name


