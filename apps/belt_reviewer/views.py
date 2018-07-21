from django.shortcuts import render, redirect
from django.db import models
from django.contrib import messages
from .models import Author, Review, User, Book
import bcrypt


# Create your views here.

def login_register(request):
    return render(request, 'belt_login.html')

def register(request):
    # Validation
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    hashword = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

    #Instantiate user
    activeUser = User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=hashword)

    # Check if active User is first user
    request.session['activeUser_id'] = activeUser.id
    return redirect('/books')

def signin(request):
    targetProfile = User.objects.get(email=request.POST['email'])
    print(targetProfile)
    if(bcrypt.checkpw(request.POST['password'].encode(), targetProfile.password.encode())):
        activeUser_id = targetProfile.id
        request.session['activeUser_id'] = activeUser_id
        return redirect('/books')
    else:
        return redirect('/', { 'response': 'Invalid Profile'})

def allBooks(request):
    starRange = range(5)
    activeUser = User.objects.get(id=request.session['activeUser_id'])
    allReviews = Review.objects.all().order_by('-created_at')
    recentReviews = allReviews[:3]

    return render(request, 'beltRev_main.html', { 'activeUser':activeUser, 'reviews':allReviews, 'recentReviews':recentReviews, 'starRange':starRange })

def addBook(request):
    authors = Author.objects.all()
    print(authors.values())
    return render(request, 'add_book.html', { 'authors':authors })

def book(request, book_id):
    book = Book.objects.get(id=book_id)
    activeUser = User.objects.get(id=request.session['activeUser_id'])
    return render(request, 'book_page.html', { 'book':book, 'activeUser':activeUser })

def user(request, user_id):
    user = User.objects.get(id=user_id)
    numReviews = user.user_reviews.all().count()
    return render(request, 'user_page.html', { 'user': user, 'numReviews':numReviews })

def process_add_book(request):
    # Validation
    activeUser = User.objects.get(id=request.session['activeUser_id'])
    errors = Book.objects.basic_validator(request.POST)
    if len(errors):
        for value in errors.items():
            messages.error(request, value)
        return redirect('/books/add')
    author = ''
    print(request.POST)
    if(len(request.POST['create_auth'])>0):
        author = Author.objects.create(name=request.POST['create_auth'])
    else:
        author = request.POST['select_auth']
        author = Author.objects.get(name=author)

    
    #Instantiate Book
    book = Book.objects.create(title=request.POST['book_title'], author=author)

    Review.objects.create(reviewed_by_user=activeUser, star_rating=request.POST['star_rating'], review_of_book=book, content=request.POST['content'])

    # Check if active User is first user
    return redirect('/books')

def logOff(request):
    request.session.flush()
    return redirect('/')



def process_add_review(request, book_id):
    requestingUser = User.objects.get(id=request.session['activeUser_id'])
    book = Book.objects.get(id=int(book_id))
    Review.objects.create(reviewed_by_user=requestingUser, star_rating=request.POST['star_rating'], review_of_book=book, content=request.POST['content'])
    return redirect('/books/' + str(book_id))

def process_rem_review(request, book_id, review_id):
    doomedMessage = Review.objects.get(id=int(review_id))
    doomedMessage.delete()
    return redirect('/books/' + book_id)
