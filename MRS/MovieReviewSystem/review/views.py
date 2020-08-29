from django.shortcuts import render
from .forms import LoginForm,MovieForm
import logging
from django.contrib.auth import authenticate, login
logger = logging.getLogger(__name__)
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from review.models import Movie
from django.contrib.auth import logout
import boto3

# Create your views here.
def signin(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/review/')
        else:    
            form = LoginForm()
            return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':
        # sending the request object to the the form
        form = LoginForm(request.POST)
        # check the form object is valid
        logger.debug("inside post method")
        if form.is_valid():
            # derive the data from the form object
            logger.debug("inside form valid")
            Username = form.cleaned_data['Username']
            pwsd = form.cleaned_data['password']
            if User.objects.filter(username=Username).exists():
                user = authenticate(username=Username, password=pwsd)
                if user is not None:
                    logger.debug("authenticated")
                    login(request, user)
                    logger.debug("login is done")
                    # redirect to ota upload link
                    return HttpResponseRedirect('/review/')
                else:
                    return render(request, 'login.html', {'form': form, 'error': 'Invalid password'})
            else:
                logger.debug("login failed")
                return render(request, 'login.html', {'form': form, 'error': 'Invalid Email'})
        else:
            logger.debug("login failed")
            logger.debug(form.errors)
            return render(request, 'login.html', {'form': form, 'error': 'Enter a valid email address.'})

@login_required
def dashboard(request):
    is_admin=False
    if request.method == 'GET':
        if request.user.is_staff:
            is_admin=True
        form = MovieForm()
        movies=Movie.objects.all()
        return render(request,'home.html',{'form': form,'movies':movies,'is_admin':is_admin})
    else:
        if request.user.is_staff:
            is_admin=True
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movietitle=form.cleaned_data['movietitle']
            synopsis=form.cleaned_data['synopsis']
            poster=request.FILES['poster']
            filename=poster.name
            s3 = boto3.resource('s3').Bucket("testbucketjaszz")
            s3.put_object(Key=poster.name, Body=poster)
            Movie_1 = Movie(movie_title=movietitle,synopsis=synopsis,poster_link=poster)
            Movie_1.save()
            movies=Movie.objects.all()
            return render(request,'home.html',{'form': form,'movies':movies,'is_admin':is_admin})
        else:
            logger.debug("Invalid form")
            movies=Movie.objects.all()
            return render(request,'home.html',{'form': form,'movies':movies,'is_admin':is_admin})           

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')