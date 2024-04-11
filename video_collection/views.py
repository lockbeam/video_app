from django.shortcuts import render, redirect
from django.contrib import messages # allows us to display a temp message to user
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower
from .forms import VideoForm, SearchForm
from .models import Video

def home(request):
    app_name = 'Music Videos'
    return render(request, 'video_collection/home.html', {'app_name': app_name})

def add(request):

    if request.method == 'POST': # if user is adding a video
        new_video_form = VideoForm(request.POST)
        if new_video_form.is_valid():
            try:
                new_video_form.save()
                return redirect('video_list') #if successful upload redirect to video_list
                # messages.info(request, 'New video has been saved')
                # TODO show success message
            except ValidationError:
                messages.warning(request, 'Invalid YouTube URL')
            except IntegrityError: # checking to make sure no duplicates
                messages.warning(request, 'Video already exists in database')

    messages.warning(request, 'Please check the data entered.')
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form}) # just show the same page again without saving but still have user inputted data
    
    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

def video_list(request):

    search_from = SearchForm(request.GET) # this builds a form from the data the user has sent to app

    if search_from.is_valid():
        search_term = search_from.cleaned_data('search_term') # user has searched a term, save term - matches forms.py
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name')) # case insensitive, order by name 

    else: # form is not filled in or this is the first time the user sees the page
        search_from = SearchForm()
        videos = Video.objects.order_by(Lower('name'))

    videos = Video.objects.all()
    return render(request, 'video_collection/video_list.html', {'videos': videos, 'search_form': search_from})



