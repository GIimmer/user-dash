from __future__ import unicode_literals
from django.db import models
import datetime
import re

# Create your models here.

class TripManager(models.Manager):
    def basic_validator(self, postData):
        now = datetime.datetime.now()
        errors = {}
        problem = False
        try:
            date_from = datetime.datetime.strptime(postData['date_from'], "%Y-%m-%d")
        except:
            errors['date_from'] = 'Start Date must not be empty'
            problem = True
        try:
            date_to = datetime.datetime.strptime(postData['date_to'], "%Y-%m-%d")
        except:
            errors['Date to'] = 'End Date must not be empty'
            problem = True
        
        if len(postData['destination']) < 3:
            errors['destination'] = "Your destination field must be at least 3 characters"
        if len(postData['description']) < 3:
            errors['description'] = "Your description of this event must be at least 3 characters"
        if(not problem):
            if (date_from < now):
                errors['date_from'] = "Your start date must begin later than today; silly goose"
            if (date_to < date_from):
                errors['date_to'] = "Your end data must be after the start date, super silly goose"
        return errors



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

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    startTime = models.DateField()
    endTime = models.DateField()
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TripManager()

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    trips_going_on = models.ManyToManyField(Trip, related_name='users_on_trip')
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
