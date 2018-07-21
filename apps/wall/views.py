from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import models
from .models import Message, Comment
from apps.lgn_register.models import User

# Create your views here.
def displayWall(request, user_id):
    # print(request.session['user_id'])
    # print(User.objects.all())
    # print(request.session['messageContent'])
    user = User.objects.get(id=request.session[user_id])
    print(messages)
    return render(request, 'wallMain.html', { 'user':user })

def processMessage(request, user_id):
    requestingUser = User.objects.get(id=user_id)
    print(requestingUser.first_name)
    print(requestingUser)
    print(request.POST['messageContent'])
    Message.objects.create(user=requestingUser, content=request.POST['messageContent'])
    return redirect('/wall/' + str(user_id))

def processComment(request, user_id):
    user = User.objects.get(id=user_id)
    print(request.POST['parentMessage'])
    print(request.POST['parentMessage'])
    usrMessage = Message.objects.get(id=int(request.POST['parentMessage']))
    Comment.objects.create(user=user, content=request.POST['commentContent'], message=usrMessage)
    return redirect('/wall/' + str(user_id))

def deleteMessage(request, user_id):
    doomedMessage = Message.objects.get(id=int(request.POST['message_id']))
    doomedMessage.delete()
    return redirect('/wall/' + str(request.session['user_id']))

def logOff(request, user_id):
    request.session.flush()
    return redirect('/')