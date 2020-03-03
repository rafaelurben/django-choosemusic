from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

app_name = 'choosemusic'
urlpatterns = [
    path('', views.home, name="home"),
    path('suggestions', views.SuggestionsView.as_view(), name="suggestions"),
    path('suggest', views.suggest, name="suggest"),
    path('playlist', views.PlaylistView.as_view(), name="playlist"),
    path('play', views.play, name="play"),
    path('login', auth_views.LoginView.as_view(template_name = 'choosemusic/login.html'), name="login"),
    path('logout', auth_views.LogoutView.as_view(next_page="/choosemusic"), name="logout"),
]
