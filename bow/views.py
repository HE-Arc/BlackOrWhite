from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import F
from .forms import RegisterForm, SigninForm
from .models import Characters, UserProfile, Camp, InventoryCategory, Item, CharactersItem

#Fist page
def index(request):
    return render(request, 'bow/pages/index.html', {'request': request})

#Home page
def signup_step_1(request):
    #Retrieve camp dynamically
    camps = Camp.objects.all();
    return render(request, 'bow/pages/signup_step_1.html', {'camps': camps})

#Register page
def signup_step_2(request, camp_id):

    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        #Validité du formulaire
        if form.is_valid():
            user = form.save(commit=False) # Sauvegarde(sans commit)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            #Create character
            character = Characters.objects.create(name=user.username, camp_id = camp_id)
            #Create user pofile
            UserProfile.objects.create(user=user, character=character)
            #Assign default weapon and shield
            CharactersItem.objects.create(is_active=1, character_id=character.id, item_id=1)
            CharactersItem.objects.create(is_active=1, character_id=character.id, item_id=2)
            # Authentication
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)    #Login après signup
            return redirect("profile")     #redirect
    else:
        form = RegisterForm()
    return render(request, "bow/pages/signup_step_2.html", {"form": form})

#Login page
def signin(request):
    if request.method == "POST":
        form = SigninForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("profile")#redirect
    else:
        form = SigninForm()
    return render(request, "bow/pages/login.html", {"form": form})

#Logout page
def signout(request):
    logout(request)
    return render(request, 'bow/pages/index.html')

#======= Fight =======#

#Opponents
@login_required
def opponents(request):
    # White player <=> Black opponent, vice versa
    camp_name = Camp.objects.filter(id=request.user.profile.character.camp.id).first().name
    camp_opponent = ""
    if(camp_name == "White"):
        camp_opponent = "Black"
    else:
        camp_opponent = "White"
    opponents_query_set = Characters.objects.filter(camp__name__contains=camp_opponent)
    return render(request, 'bow/pages/opponents.html', {'opponents': opponents_query_set})

#Choose opponent
'''def opponent(request):
    return render(request, 'bow/pages/opponents.html')'''

#====Display user profile
@login_required
def profile(request):
    #current user
    current_user = request.user
    #get user and character datas
    user_profile = UserProfile.objects.select_related('user','character').get(user_id=current_user.id)
    #Return inventory Categories
    inv_cat = InventoryCategory.objects.all();
    #All player Items
    items = CharactersItem.objects.select_related('item').filter(character_id=Characters.objects.filter(name=current_user).first().id)#Juste pour test
    return render(request, 'bow/pages/profile.html', {'profile': user_profile, 'cats': inv_cat, 'items': items})

#====Improve player: Pas terrible (05:10)
@login_required
def improve(request, attrib):
    if request.method =='POST':
        if request.is_ajax:
            #Get current user id
            current_user = request.user
            #Update strength
            if attrib == 1:
                Characters.objects.filter(name=current_user).update(strength=F('strength') +10, experience=F('experience') - 10)
                response = Characters.objects.filter(name=current_user).first().strength
                return HttpResponse(response)
            #Update defense
            elif attrib == 2:
                Characters.objects.filter(name=current_user).update(defense=F('defense') +10, experience=F('experience') - 10)
                response = Characters.objects.filter(name=current_user).first().defense
                return HttpResponse(response)
            #Update speed
            elif attrib == 3:
                Characters.objects.filter(name=current_user).update(speed=F('speed') +10, experience=F('experience') - 10)
                response = Characters.objects.filter(name=current_user).first().speed
                return HttpResponse(response)
            #Update agility
            elif attrib == 4:
                Characters.objects.filter(name=current_user).update(agility=F('agility') +10, experience=F('experience') - 10)
                response = Characters.objects.filter(name=current_user).first().agility
                return HttpResponse(response)
    return render(request)
#====Store
@login_required
def store(request):
    #current_user
    current_user = request.user
    character = Characters.objects.filter(name=current_user).first()
    #Return alls Items
    items = Item.objects.all()
    return render(request, 'bow/pages/store.html', {'items': items, 'character': character})

#====Achat équiement
@login_required
def buy(request, id):
    if request.method =='POST':
        if request.is_ajax:
            character_id = Characters.objects.filter(name=request.user).first().id
            #Test if (character_id, item_id) exists
            exist = CharactersItem.objects.filter(character_id=character_id, item_id=id).count();
            if exist == 0:
                item = CharactersItem.objects.create(character_id=character_id, item_id=id)
                return HttpResponse(item)
            else:
                return HttpResponse("interdit")
    return render(request)
