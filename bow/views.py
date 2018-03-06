from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import RegisterForm, SigninForm
from .models import Characters, UserProfile, Camp

#Maybe TODO Or use decorator https://stackoverflow.com/questions/7367509/login-in-django-testing-framework
#Fist page
def index(request):
    #Retouner le template (page) correspondant
    if(request.user.is_authenticated):
        return redirect('fight')
    else:
        return render(request, 'bow/pages/index.html', {'request': request})

#Home page
def home(request):
    # Assign choosed camp_id to character
    user_character = Characters.objects.get(id=request.user.profile.character.id)

    if(request.POST.get('black', None) is not None):
        user_character.camp_id = Camp.objects.filter(name="Black").first().id
        user_character.save(update_fields=['camp_id'])

    elif(request.POST.get('white', None) is not None):
        user_character.camp_id = Camp.objects.filter(name="White").first().id
        user_character.save(update_fields=['camp_id'])

    if(user_character.camp_id is -1):   # If the user didn't choose camp yet
        return render(request, 'bow/pages/home.html')
    else:
        return redirect('index');

#=======    Authentification    =======#

#Login page
def signin(request):
    if request.method == "POST":
        form = SigninForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("home")#redirect
    else:
        form = SigninForm()
    return render(request, "bow/pages/login.html", {"form": form})

#Register page
def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        #Validité du formulaire
        if form.is_valid():
            user = form.save(commit=False) # Sauvegarde(sans commit)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()

            # Create associated player's profile and character 1:1
            character = Characters.objects.create(name=user.username, strength=5, defense=5, speed=5, agility=5, victories=0, fight_count=0, experience=0, gold=0, camp_id=-1, level_id=1)
            UserProfile.objects.create(user=user, character=character)

            # Authentication
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)    #Login après signup
            return redirect("home")     #redirect
    else:
        form = RegisterForm()
    return render(request, "bow/pages/signup.html", {"form": form})

#Logout page
def signout(request):
    logout(request)
    return render(request, 'bow/pages/index.html')

#======= Fight =======#

#Select opponent page <=> relative to name of the menu "Fight"/"Combat"
def fight(request):

    # White player <=> Black opponent, vice versa
    camp_name = Camp.objects.filter(id=request.user.profile.character.camp.id).first().name
    camp_opponent = ""

    if(camp_name == "White"):
        camp_opponent = "Black"
    else:
        camp_opponent = "White"

    # https://stackoverflow.com/questions/1981524/django-filtering-on-foreign-key-properties
    opponents_query_set = Characters.objects.filter(camp__name__contains=camp_opponent)

    return render(request, 'bow/pages/fight.html', {'opponents': opponents_query_set})

#Details about opponent
def opponent(request):
    return render(request, 'bow/pages/opponent.html')

#====Afficher les statistiques d'un joueur
def profile(request):
    return render(request, 'bow/pages/profile.html')
