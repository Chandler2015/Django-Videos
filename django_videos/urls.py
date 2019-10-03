from django.contrib import admin, auth
from django.urls import path
from videos import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    # auth
    path('signup', views.SignUp.as_view(), name="signup"),
    path('login', auth.views.LoginView.as_view(), name="login"),
    path('logout', auth.views.LogoutView.as_view(), name="logout"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
