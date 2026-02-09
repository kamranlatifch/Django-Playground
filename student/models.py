from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    roll_no = models.IntegerField(unique=True, max_length=10, auto_created=True)
    email = models.EmailField(unique=True, max_length=100)
    phone = models.CharField(max_length=15)
    roll_no = models.IntegerField(unique=True, max_length=10, auto_created=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
