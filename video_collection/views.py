from django.shortcuts import render
from django.contrib import messages # allows us to display a temp message to user
from .forms import VideoForm

def home(request):
    app_name = 'Music Videos'
    return render(request, 'video_collection/home.html', {'app_name': app_name})

def add(request):

    if request.method == 'POST': # if user is adding a video
        new_video_form = VideoForm(request.POST)
        if new_video_form.is_valid():
            new_video_form.save()
            messages.info(request, 'New video has been saved')
            # TODO show success message
        else:
            messages.warning(request, 'Please check the data entered.')
            return render(request, 'video_collection/add.html', {'new_video_form': new_video_form}) # just show the same page again without saving but still have user inputted data
    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})



