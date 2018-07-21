from __future__ import unicode_literals
from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 3:
            errors['first_name'] = "Your first name must be at least 3 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name must be at least 3 characters"
        if not re.match(r"[^@]+@[^@]+\.[^@]+", postData['email']):
            errors['email'] = "Your email is not valid"
        if len(postData['password']) < 6:
            errors['password'] = "Your password is of insufficient Length"
        if postData['password'] != postData['pass_conf']:
            errors['password'] = "Your passwords do not match"
        return errors

    def info_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Your first name must contain at least 2 characters"
        elif(type(postData['first_name']) is not str):
            errors['first_name'] = "Your first name must not contain numbers"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name must be at least 2 characters"
        elif(type(postData['last_name']) is not str):
            errors['last_name'] = "Your last name must not contain numbers"
        if not re.match(r"[^@]+@[^@]+\.[^@]+", postData['email']):
            errors['email'] = "Your email is not valid"
        return errors

    def password_validator(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors['password'] = "Your password is of insufficient Length"
        if postData['password'] != postData['pass_conf']:
            errors['password'] = "Your passwords do not match"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    description = models.TextField(default="")
    user_level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Message(models.Model):
    created_by = models.ForeignKey(User, related_name='sentMessages')
    content = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(User, related_name='recievedMessages')

class Comment(models.Model):
    content = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='userComments')
    message = models.ForeignKey(Message, related_name='messageComments')


