from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import RegisterForm, SigninForm

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
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)#Login après signup
            return redirect("home")#redirect
    else:
        form = RegisterForm()
    return render(request, "bow/pages/signup.html", {"form": form})

#Logout page
def signout(request):
    logout(request)
    return render(request, 'bow/pages/index.html')

#======= Fight =======#

#Select opponent page
def fight(request):
    return render(request, 'bow/pages/fight.html')

def opponent(request):
    return render(request, 'bow/pages/home.html')
