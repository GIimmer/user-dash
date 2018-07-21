from __future__ import unicode_literals
from django.db import models
import re

# Create your models here.

class BlogManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Your first name must be at least 2 characters"
        elif(type(postData['first_name']) is not str):
            errors['first_name'] = "Your first name must not contain numbers"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name must be at least 2 characters"
        elif(type(postData['last_name']) is not str):
            errors['last_name'] = "Your last name must not contain numbers"
        if not re.match(r"[^@]+@[^@]+\.[^@]+", postData['email']):
            errors['email'] = "Your email is not valid"
        if(len(postData['password']) < 4):
            errors['password'] = "Your password must be at least 4 characters"
        if(postData['password'] != postData['confirmPass']):
            errors['confirmPass'] = "Your password confirmation does not match"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    objects = BlogManager()