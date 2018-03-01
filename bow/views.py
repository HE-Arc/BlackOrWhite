from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import RegisterForm, SigninForm
from .models import Characters

#Maybe TODO Or use decorator https://stackoverflow.com/questions/7367509/login-in-django-testing-framework
#Fist page
def index(request):
    #Retouner le template (page) correspondant
    if(request.user.is_authenticated):
        return fight(request)
    else:
        return render(request, 'bow/pages/index.html', {'request': request})

#Home page
def home(request):
    return render(request, 'bow/pages/home.html')

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
            user = form.save(commit=False)#Sauvegarde(sans commit)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()

            #TODO create associated player's character 1:1

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
    # https://stackoverflow.com/questions/1981524/django-filtering-on-foreign-key-properties
    #TODO filter from user opponents => white player <=> black opponent, vice versa
    opponents_query_set = Characters.objects.filter(camp__name__contains="Black")
    print(opponents_query_set)
    return render(request, 'bow/pages/fight.html', {'opponents': opponents_query_set})

#Details about opponent
def opponent(request):
    return render(request, 'bow/pages/home.html')   #TODO template and replace
