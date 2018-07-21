from django.shortcuts import render, redirect
from django.db import models
from django.contrib import messages
from .models import User, Trip
import bcrypt


# Create your views here.

def login(request):
    return render(request, 'login.html')

def processRegister(request):
    # Validation
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    hashword = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    #Instantiate user
    activeUser = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashword)
    request.session['activeUser_id'] = activeUser.id
    return redirect('/travels')

def processSignin(request):
    targetProfile = User.objects.filter(email=request.POST['email'])
    if len(targetProfile) == 1:
        if(bcrypt.checkpw(request.POST['password'].encode(), targetProfile.first().password.encode())):
            activeUser_id = targetProfile.first().id
            request.session['activeUser_id'] = activeUser_id
            return redirect('/travels')
        if not (bcrypt.checkpw(request.POST['password'].encode(), targetProfile.first().password.encode())):
            errors = {}
            errors['password'] = 'password does not match that of the user on record'
            for tag, value in errors.items():
                messages.error(request, value)
            return redirect('/')
    elif(len(targetProfile) == 0):
        errors = {}
        errors['profile'] = 'No such profile'
        for tag, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    return redirect('/')

def travels(request):
    activeUser = User.objects.get(id=request.session['activeUser_id'])
    trip = Trip.objects.all()
    trips_going_on = []
    unjoined_trips = []
    if len(trip) > 0:
        trips_going_on = Trip.objects.filter(users_on_trip=activeUser)
        unjoined_trips = trip.exclude(users_on_trip=activeUser)
    return render(request, 'python_main.html', { 'activeUser':activeUser, 'trips_going_on':trips_going_on, 'unjoined_trips':unjoined_trips })

def addTrip(request):
    return render(request, 'addTrip.html')

def processAddTrip(request):
    # Validation
    activeUser = User.objects.get(id=request.session['activeUser_id'])
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors):
        for tag, value in errors.items():
            messages.error(request, value)
        return redirect('/addtrip')
    name = activeUser.first_name
    trip = Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], startTime=request.POST['date_from'], endTime=request.POST['date_to'], created_by=name)
    trip.users_on_trip.add(activeUser)
    trip.save()
    # Check if active User is first user
    return redirect('/travels')

def viewTrip(request, trip_id):
    activeUser = User.objects.get(id=int(request.session['activeUser_id']))
    trip = Trip.objects.get(id=int(trip_id))
    usersOnTrip = trip.users_on_trip.exclude(first_name=trip.created_by)
    return render(request, 'trippage.html', { 'trip':trip, 'usersOnTrip':usersOnTrip, 'activeUser':activeUser })

def leaveTrip(request, trip_id):
    user = User.objects.get(id=int(request.session['activeUser_id']))
    trip = Trip.objects.get(id=int(trip_id))
    user.trips_going_on.remove(trip)
    return redirect('/travels')

def joinTrip(request, trip_id):
    user = User.objects.get(id=int(request.session['activeUser_id']))
    trip = Trip.objects.get(id=int(trip_id))
    trip.users_on_trip.add(user)
    return redirect('/travels')

def deleteTrip(request, trip_id):
    trip = Trip.objects.get(id=int(trip_id))
    activeUser = User.objects.get(id=int(request.session['activeUser_id']))
    if trip.created_by == activeUser.first_name:
        trip.delete()
    return redirect('/travels')

def logOff(request):
    request.session.flush()
    return redirect('/')

