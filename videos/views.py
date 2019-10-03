from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Videos


def home(request):
    return render(request, 'videos/home.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

# def create_video(request):
#     if request.method == 'POST':


class CreateVideos(generic.CreateView):
    model = Videos
    fields = ['title']
    template_name = 'videos/create_videos.html'
    success_url = reverse_lazy('home')
