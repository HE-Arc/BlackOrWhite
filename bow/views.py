from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import F
from .forms import RegisterForm, SigninForm
from .models import Characters, UserProfile, Camp, InventoryCategory, Item, CharactersItem

from math import gcd
from random import randint

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

@login_required
def fight(request, opponent_id):
    opponent = Characters.objects.filter(id=opponent_id).first()
    #print(opponent.name)
    return render(request, 'bow/pages/fight.html', {'opponent': opponent})

@login_required
def fight_opponent(request, opponent_id):
    response = None

    # Get back characters
    pv_player1 = 100
    player1 = request.user.profile.character

    pv_player2 = 100
    player2 = Characters.objects.filter(id=opponent_id).first()

    # Calcul player tick in f(speed)
    ppmc = player1.speed * player2.speed / gcd(player1.speed, player2.speed) # Calcul least common multiple

    tick_player1 = int(ppmc / player1.speed) # Exemple   10/5 = 2  => so every 2 tick
    tick_player2 = int(ppmc / player2.speed) #           10/10 = 1 => so every tick

    # To logs fight actions
    log_fight = []

    # ---Process the fight----
    #TODO add weapons and shields, and externalize in func in a controller
    counter = 0
    while pv_player1 > 0 and pv_player2 > 0:
        if counter % tick_player1 is 0:
            dodge_rate = ((player2.agility/player1.agility) * 100) / 2 % 101        # Exemple   10/100 * 100 / 2 % 101 = 10% AND 100/10 * 100 / 2 % 101 = 100%
            rnd_dodge = randint(1, 100)

            print("1", dodge_rate, rnd_dodge)

            text = player1.name+" a attaqué "+player2.name
            if dodge_rate > rnd_dodge:  # dodge effective
                text += " mais il a esquivé"
            else:
                damages_player2 = player1.strength * 2 / player2.defense
                pv_player2 -= damages_player2
                text += " et a enlevé "+str(damages_player2)+" PV. Il lui reste: "+str(pv_player2)

            log_fight.append(text)
        if counter % tick_player2 is 0:
            dodge_rate = ((player1.agility / player2.agility) * 100) / 2 % 101
            rnd_dodge = randint(1, 100)

            print("2", dodge_rate, rnd_dodge)

            text = player2.name+" a attaqué "+player1.name
            if dodge_rate > rnd_dodge:
                text += " mais il a esquivé"
            else:
                damages_player1 = player2.strength * 2 / player1.defense
                pv_player1 -= damages_player1
                text += " et a enlevé " + str(damages_player1) + " PV. Il lui reste: " + str(pv_player1)

            log_fight.append(text)

        counter += 1

    # ---End fight---

    # Update DB with result
    db_chararacter = Characters.objects.filter(id=player1.id)
    db_chararacter.update(fight_count=F('fight_count') + 1)

    # Create return values
    if pv_player1 > 0:
        db_chararacter.update(gold=F('gold') + 100, experience=F('experience') + 100, victories=F('victories') + 1)
        log_fight.append(player2.name+" est K.O.")
        response = "Vous avez gagné !"
    elif pv_player2 > 0:
        db_chararacter.update(gold=F('gold') + 10, experience=F('experience') + 10, victories=F('defeat') + 1)
        log_fight.append(player1.name+" est K.O.")
        response = "Vous avez perdu !"
    else:
        log_fight.append("Les deux combattans sont K.O.")
        response = "Égalité !"

    response += '<br><br>' + '<br>'.join(log_fight)

    # Return final response, may be JsonRepsonse
    return HttpResponse(response)

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
