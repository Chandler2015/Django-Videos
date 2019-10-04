from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Videos, Video
from django.contrib.auth import authenticate, login
from .forms import VideoForm, SearchForm
from django.forms import formset_factory
from django.http import Http404, JsonResponse
import urllib
from django.forms.utils import ErrorList
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


YOUTUBE_API_KEY = 'AIzaSyCcVtIzaEIRwklrtyAmwDWKvEgNAFXOQXc'


def home(request):
    recent_videos = Videos.objects.all().order_by("-id")[:3]
    popular_videos = [Videos.objects.get(
        pk=1), Videos.objects.get(pk=2), Videos.objects.get(pk=3)]
    return render(request, 'videos/home.html', {'recent_videos': recent_videos, "popular_videos": popular_videos})


@login_required
def dashboard(request):
    videos = Videos.objects.filter(user=request.user)
    return render(request, 'videos/dashboard.html', {'videos': videos})


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get(
            'username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


class CreateVideos(LoginRequiredMixin, generic.CreateView):
    model = Videos
    fields = ['title']
    template_name = 'videos/create_videos.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateVideos, self).form_valid(form)
        return redirect('dashboard')


class DetailVideos(generic.DetailView):
    model = Videos
    template_name = 'videos/detail_videos.html'


class UpdateVideos(LoginRequiredMixin, generic.UpdateView):
    model = Videos
    template_name = 'videos/update_videos.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        videos = super(UpdateVideos, self).get_object()
        if not videos.user == self.request.user:
            raise Http404
        return videos


class DeleteVideos(LoginRequiredMixin, generic.DeleteView):
    model = Videos
    template_name = 'videos/delete_videos.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        videos = super(DeleteVideos, self).get_object()
        if not videos.user == self.request.user:
            raise Http404
        return videos


@login_required
def add_video(request, pk):
    form = VideoForm()
    search_form = SearchForm()
    videos = Videos.objects.get(pk=pk)
    if videos.user != request.user:
        raise Http404
    if request.method == 'POST':

        form = VideoForm(request.POST)
        if form.is_valid():
            video = Video()
            video.videos = videos
            video.url = form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            if video_id:
                video.youtube_id = video_id[0]
                response = requests.get(
                    f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={YOUTUBE_API_KEY}')

                json = response.json()
                title = json['items'][0]['snippet']['title']
                video.title = title
                video.save()
                return redirect('detail_videos', pk)
            else:
                errors = form._errors.setdefault('url', ErrorList())
                errors.append('Needs to be a YouTube URL')
    return render(request, 'videos/add_video.html', {'form': form, 'search_form': search_form, 'videos': videos})


@login_required
def video_search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(
            search_form.cleaned_data['search_term'])
        response = requests.get(
            f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={encoded_search_term}&key={YOUTUBE_API_KEY}')
        # https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q=eggs&key={YOUR_API_KEY}
        return JsonResponse(response.json())
    return JsonResponse({'Error': "Not able to validate form"})


class DeleteVideo(LoginRequiredMixin, generic.DeleteView):
    model = Video
    template_name = 'videos/delete_video.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super(DeleteVideo, self).get_object()
        if not video.videos.user == self.request.user:
            raise Http404
        return video
