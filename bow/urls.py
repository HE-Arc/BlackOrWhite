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
    #Game
    path('combat', views.fight, name='fight'),
    path('adversaire', views.opponent, name='opponent'),
]
