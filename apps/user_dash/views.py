from django.shortcuts import render, redirect
from django.db import models
from django.contrib import messages
from .models import Message, Comment, User
import bcrypt


# Create your views here.

def landing_page(request):
    return render(request, 'landing_page.html')

def register(request):
    return render(request, 'register.html')

def processRegister(request):
    # Validation
    errors = User.objects.basic_validator(request.POST)
    hashword = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')

    #Instantiate user
    activeUser = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashword, user_level=1)

    # Check if active User is first user
    allUsers = User.objects.all()
    print(allUsers)
    print(len(allUsers))
    if(len(allUsers) < 2):
        activeUser.user_level = 9
        activeUser.save()
    request.session['activeUser_id'] = activeUser.id
    return redirect('/dashboard')

def signIn(request):
    return render(request, 'signin.html', { 'response': " " })

def processSignin(request):
    targetProfile = User.objects.filter(email=request.POST['email'])
    if len(targetProfile) == 1:
        if(bcrypt.checkpw(request.POST['password'].encode(), targetProfile.first().password.encode())):
            activeUser_id = targetProfile.first().id
            request.session['activeUser_id'] = activeUser_id
            return redirect('/dashboard')
        if not (bcrypt.checkpw(request.POST['password'].encode(), targetProfile.first().password.encode())):
            errors = {}
            errors['password'] = 'password does not match that of the user on record'
            for tag, value in errors.items():
                messages.error(request, value)
            return redirect('/signin')
    elif(len(targetProfile) == 0):
        errors = {}
        errors['profile'] = 'No such profile'
        for tag, value in errors.items():
            messages.error(request, value)
        return redirect('/signin')
    return redirect('/')

def displayUsers(request):
    activeUser = User.objects.get(id=request.session['activeUser_id'])
    print(activeUser)
    print(activeUser.user_level)
    request.session['activeUser_level'] = activeUser.user_level
    return render(request, 'display_users.html', { 'activeUser':activeUser, 'users':User.objects.all()})

def addUser(request):
    return render(request, 'add_users.html')

def processAddUser(request):
    # Validation
    errors = User.objects.basic_validator(request.POST)
    hashword = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/users/new')

    #Instantiate user
    User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashword, user_level=1)

    # Check if active User is first user
    return redirect('/dashboard')


def editUser(request, user_id):
    user = User.objects.get(id=user_id)
    activeUser = User.objects.get(id=request.session['activeUser_id'])
    return render(request, 'edit_profile.html', { 'user':user, 'activeUser':activeUser })

def processEditUser(request, user_id):
    activeUser = User.objects.get(id=request.session['activeUser_id'])
    user = User.objects.get(id=user_id)
    if(not request.session['activeUser_level'] == 9) and (request.session['activeUser_id'] != int(user_id)):
        return redirect('/dashboard')
    if(request.POST['secret'] == 'upd_info'):
        errors = User.objects.info_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/edit/' + user_id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.user_level = request.POST['user_level']
    elif(request.POST['secret'] == 'upd_pass'):
        errors = User.objects.password_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/edit/' + user_id)
        user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    else:
        print(request.POST['description'])
        print("I'm here!!!!!!!!!!")
        user.description = request.POST['description']
        print(user.description)


    user.save()

    return redirect('/dashboard')

def wall(request, user_id):
    user = User.objects.get(id=user_id)
    print(request.session['activeUser_id'])
    return render(request, 'wall.html', { 'user':user })

def processRemove(request, user_id):
    user = User.objects.get(id=int(user_id))
    user.delete()
    return redirect('/dashboard')

def logOff(request):
    request.session.flush()
    return redirect('/')




def processMessage(request, user_id):
    requestingUser = User.objects.get(id=request.session['activeUser_id'])
    recipient = User.objects.get(id=int(user_id))
    Message.objects.create(created_by=requestingUser, recipient=recipient, content=request.POST['messageContent'])
    return redirect('/users/show/' + str(user_id))

def processComment(request, user_id, message_id):
    requestingUser = User.objects.get(id=request.session['activeUser_id'])
    parentMessage = Message.objects.get(id=int(message_id))
    Comment.objects.create(created_by=requestingUser, content=request.POST['commentContent'], message=parentMessage)
    return redirect('/users/show/' + str(user_id))

def deleteMessage(request, user_id):
    doomedMessage = Message.objects.get(id=int(request.POST['message_id']))
    doomedMessage.delete()
    return redirect('/users/show/' + str(user_id))
