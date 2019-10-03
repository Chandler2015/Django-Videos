from django.contrib import admin, auth
from django.urls import path
from videos import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    # auth
    path('signup', views.SignUp.as_view(), name="signup"),
    path('login', auth_views.LoginView.as_view(), name="login"),
    path('logout', auth_views.LogoutView.as_view(), name="logout"),
    # videos
    path('videos/create', views.CreateVideos.as_view(), name='create_videos'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
