from django.urls import path
from . import views

urlpatterns = [
    #Page d'accueil
    path('', views.index, name='index'),
    #Access app
    path('connexion', views.signin, name='login'),
    path('deconnexion', views.signout, name='logout'),
    path('inscription', views.signup_step_1, name='signup_step_1'),
    path('inscription/<int:camp_id>', views.signup_step_2, name='signup_step_2'),
    #user profile
    path('profil', views.profile, name='profile'),
    path('profil/improve/<int:attrib>', views.improve, name='improve'),
    #Game
    path('adversaires', views.opponents, name='opponents'),
    path('combat/<int:opponent_id>', views.fight, name='fight'),
    path('combat/resultat/<int:opponent_id>', views.fight_opponent, name='fight_opponent'),
    #Store
    path('boutique', views.store, name='store'),
    path('achat/<int:id>', views.buy, name='buy'),
]
