from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import models
from .models import User
import bcrypt

# Create your views here.

def landingPage(request):
    if('visitState' not in request.session):
        request.session['visitState'] = 'unknown'
    return render(request, 'lgnRegIndex.html', )


def process(request):
    if('register' in request.POST):
        
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.items():
                messages.error(request, error)
            return redirect('/')

        fName = request.POST['first_name']
        lName = request.POST['last_name']
        emailAdd = request.POST['email']
        hashWord = bcrypt.hashpw((request.POST['password']).encode(), bcrypt.gensalt())

        user = User.objects.create(first_name=fName, last_name=lName, email=emailAdd, password=hashWord)
        request.session['first_name'] = fName
        request.session['visitState'] = 'new_user'
        return redirect('/' + str(user.id) + '/success')

    elif('login' in request.POST):
        user = User.objects.filter(email=request.POST['email']).first()
        if(bcrypt.checkpw(request.POST['password'].encode(), user.password.encode())):
            request.session['user_id'] = user.id
            request.session['visitState'] = 'returning_user'
            return redirect('/wall/' + str(user.id))
        else:
            return redirect(request, '/')
            
def success(request, user_id):
    user = User.objects.get(id=user_id)
    arrivalRoute = 'logged in'
    if(request.session['visitState'] == 'new_user'):
        arrivalRoute = 'registered'
    return render(request, 'success.html', { 'arrivalRoute': arrivalRoute, 'userName':user.first_name })