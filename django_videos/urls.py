from django.contrib import admin, auth
from django.urls import path
from videos import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('dashboard', views.dashboard, name="dashboard"),
    # auth
    path('signup', views.SignUp.as_view(), name="signup"),
    path('login', auth_views.LoginView.as_view(), name="login"),
    path('logout', auth_views.LogoutView.as_view(), name="logout"),
    # videos
    path('videos/create', views.CreateVideos.as_view(), name='create_videos'),
    path('videos/<int:pk>', views.DetailVideos.as_view(), name='detail_videos'),
    path('videos/<int:pk>/update',
         views.UpdateVideos.as_view(), name='update_videos'),
    path('videos/<int:pk>/delete',
         views.DeleteVideos.as_view(), name='delete_videos'),
    # video
    path('videos/<int:pk>/addvideo', views.add_video, name="add_video"),
    path('video/search', views.video_search, name="video_search"),
    path('video/<int:pk>/delete',
         views.DeleteVideo.as_view(), name='delete_video'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
