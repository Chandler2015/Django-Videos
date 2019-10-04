from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Videos, Video
from django.contrib.auth import authenticate, login
from .forms import VideoForm, SearchForm


def home(request):
    return render(request, 'videos/home.html')


def dashboard(request):
    return render(request, 'videos/dashboard.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get(
            'username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


class CreateVideos(generic.CreateView):
    model = Videos
    fields = ['title']
    template_name = 'videos/create_videos.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateVideos, self).form_valid(form)
        return redirect('home')


class DetailVideos(generic.DetailView):
    model = Videos
    template_name = 'videos/detail_videos.html'


class UpdateVideos(generic.UpdateView):
    model = Videos
    template_name = 'videos/update_videos.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')


class DeleteVideos(generic.DeleteView):
    model = Videos
    template_name = 'videos/delete_videos.html'
    success_url = reverse_lazy('dashboard')


def add_video(request, pk):
    form = VideoForm()
    search_form = SearchForm()
    if request.method == 'POST':
        filled_form = VideoForm(request.POST)
        if filled_form.is_valid():
            video = Video()
            video.url = filled_form.cleaned_data['url']
            video.title = filled_form.cleaned_data['title']
            video.youtube_id = filled_form.cleaned_data['youtube_id']
            video.videos = Videos.objects.get(pk=pk)
            video.save()
    return render(request, 'videos/add_video.html', {"form": form, 'search_form': search_form})
