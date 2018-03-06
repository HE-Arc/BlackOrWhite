from django.urls import path
from . import views

urlpatterns = [
    #Page d'accueil
    path('', views.index, name='index'),
    path('accueil', views.home, name='home'),
    #Access app
    path('connexion', views.signin, name='login'),
    path('deconnexion', views.signout, name='logout'),
    path('inscription', views.signup, name='register'),
    #user profile
    path('profil', views.profile, name='profile'),
    path('personnage', views.character, name='character'),
    path('attributs', views.attributes, name='attributes'),
    path('inventaire', views.inventory, name='inventory'),
    #Game
    path('adversaire', views.opponent, name='opponent'),
]
