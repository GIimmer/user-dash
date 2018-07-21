from __future__ import unicode_literals
from django.db import models
import re

# Create your models here.
class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['book_title']) < 2:
            errors['title'] = "The title must be at least 2 characters"
        elif(type(postData['book_title']) is not str):
            errors['title'] = "The title must not contain numbers"
        if len(postData['content']) < 2:
            errors['content'] = "Your review is of insufficient length"
        if((len(postData['create_auth']) < 1) and (len(postData['select_auth']) < 1)):
            errors['author'] = "You need an author"
        return errors

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Your first name must be at least 2 characters"
        elif(type(postData['name']) is not str):
            errors['name'] = "Your first name must not contain numbers"
        if len(postData['alias']) < 2:
            errors['alias'] = "Your last name must be at least 2 characters"
        elif(type(postData['alias']) is not str):
            errors['alias'] = "Your last name must not contain numbers"
        if not re.match(r"[^@]+@[^@]+\.[^@]+", postData['email']):
            errors['email'] = "Your email is not valid"
        if len(postData['password']) < 6:
            errors['password'] = "Your password is of insufficient Length"
        if postData['password'] != postData['pass_conf']:
            errors['password'] = "Your passwords do not match"
        return errors

    def info_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Your first name must be at least 2 characters"
        elif(type(postData['name']) is not str):
            errors['name'] = "Your first name must not contain numbers"
        if len(postData['alias']) < 2:
            errors['alias'] = "Your last name must be at least 2 characters"
        elif(type(postData['alias']) is not str):
            errors['alias'] = "Your last name must not contain numbers"
        if not re.match(r"[^@]+@[^@]+\.[^@]+", postData['email']):
            errors['email'] = "Your email is not valid"
        return errors

    def password_validator(self, postData):
        errors = {}
        if len(postData['password']) < 6:
            errors['password'] = "Your password is of insufficient Length"
        if postData['password'] != postData['pass_conf']:
            errors['password'] = "Your passwords do not match"
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Book(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, related_name='authored_book')

    objects = BookManager()


class Review(models.Model):
    content = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    star_rating = models.IntegerField()
    reviewed_by_user = models.ForeignKey(User, related_name='user_reviews')
    review_of_book = models.ForeignKey(Book, related_name='book_reviews')