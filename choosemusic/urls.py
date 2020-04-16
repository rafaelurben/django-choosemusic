from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

############

try:
    from django.contrib.auth.models import Group, Permission
    choosemusic_admin, created = Group.objects.get_or_create(name='choosemusic_admin')
    choosemusic_admin.permissions.add(Permission.objects.get(codename="add_einreichung"))
    choosemusic_admin.permissions.add(Permission.objects.get(codename="view_einreichung"))
    choosemusic_admin.permissions.add(Permission.objects.get(codename="change_einreichung"))
    choosemusic_admin.permissions.add(Permission.objects.get(codename="delete_einreichung"))
except:
    pass

############


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
