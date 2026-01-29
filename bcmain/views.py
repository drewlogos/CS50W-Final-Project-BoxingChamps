from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
import json, random # For requests in JS fetch (buttons & actions), and to randomize
from decimal import Decimal # To operate/convert decimals
# To handle dates and times
from datetime import datetime, date, timedelta 
from django.utils import timezone
# Import models
from .models import User, Place, Player, AreaAction, CityEvent, NonPlayer

# Main page
def index(request):
    try:
        # If user exists
        if User.objects.get(username=request.user):
            return HttpResponseRedirect(reverse("home"))            
    except:
        # If it doesn't exist go back to welcome page
        return render(request, "welcome.html")

# To log user in
def login_view(request):
    if request.method == "POST":
        username = request.POST["InputUsername"]
        password = request.POST["InputPassword"]
        user = authenticate(request, username=username, password=password)
        # Check for successful authentication
        if user is not None:
            # If user exists
            if User.objects.get(username=username):
                login(request, user)
                return HttpResponseRedirect(reverse("home"))          
        else:
            messages.error(request, 'Invalid Username and/or Password.')
            return render(request, "login.html", {
                "message": messages
            })
    else:
        return render(request, "login.html")
    
# To log user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("welcome"), {
        "message": "You have successfully logged out."
    })

# To register a user
def register(request):
    if request.method == "GET":
        return render(request, "register.html")   
    elif request.method == "POST":
        username = request.POST["InputUser"]
        password = request.POST["InputPassword"]
        confirmation = request.POST["ConfirmPassword"]
        email = request.POST["InputEmail"]
        first_name = request.POST["InputFirstName"]
        last_name = request.POST["InputLastName"]
        # For different passwords
        if password != confirmation:
            messages.error(request, 'Both passwords must match.')
            return render(request, "register.html", {
                "message": messages
            })
        # For blank password    
        elif password == '':
            messages.error(request, 'You must set a password')
            return render(request, "register.html", {
                "message": messages
            })
        else:
            try:
                # Create User
                new_user = User.objects.create_user(username, email, password)
                new_user.save()
                new_user.first_name = first_name
                new_user.last_name = last_name
                new_user.save()
                # Create Player
                new_player = Player(user=new_user)
                new_player.save()
            # If user exists    
            except IntegrityError:
                messages.error(request, "Username already taken.")
                return render(request, "register.html", {
                    "message": messages
                })
            login(request, new_user)
            return HttpResponseRedirect(reverse("welcome"))
                           
# Home page (show player data, rank and statistics)
@csrf_exempt
@login_required
def home(request):
    # Get Player data to populate HTML
    player_data = Player.objects.get(user=request.user)
    # Check if player is not recovering
    if check_recovery(request, player_data) == "Not Recovering":
        return render(request, "home.html", {
            "player": player_data
        })
    else:
        # Redirect to recovery
        return check_recovery(request, player_data)

# City and Places section:
## Main City
@login_required
def city(request):
    # Get Player data to populate HTML
    player_data = Player.objects.get(user=request.user)
    # Check if player is not recovering
    if check_recovery(request, player_data) == "Not Recovering":
        # Get all places to fill the city links
        places = Place.objects.all()
        return render(request, "city.html",{ 
                    "places": places
                    })
    else:
        # Redirect to recovery
        return check_recovery(request, player_data)
    
## Places (sections or districts in the City)
@login_required
def places(request, place):
    # Get Places and Player data
    zone = Place.objects.get(id_name=place)
    player_data = Player.objects.get(user=request.user) 
    area_actions = AreaAction.objects.filter(place=zone)
    # Check if player is not recovering
    if check_recovery(request, player_data) == "Not Recovering":
        return render(request, "place.html", {
            "zone": zone,
            "player": player_data,
            "ar_act": area_actions
        })
    else:
        # Redirect to recovery
        return check_recovery(request, player_data)

## Gym section (Train)
@csrf_exempt #TODO Change the 'exempt' workaround for better security!
@login_required
def gym(request):
    if request.method == "GET":
        player_data = Player.objects.get(user=request.user) 
        # Check if player is not recovering
        if check_recovery(request, player_data) == "Not Recovering":
            return render(request, "gym.html", {
                    "player": player_data
            })
        else:
            # Redirect to recovery
            return check_recovery(request, player_data)
            
    # To process the actions from buttons at Gym page (JS function "gymtrain")
    elif request.method == "POST":
        # Check if player is not recovering, need player data to check and modify later
        player_data = Player.objects.get(user=request.user)
        if check_recovery(request, player_data) == "Not Recovering":
            # Get Player data, User data and passed data from JS
            user = User.objects.get(username=request.user)
            player = Player.objects.get(user=request.user)
            data = json.loads(request.body) 
            # Data already validated in js, to receive/store input training data
            train = data['training']
            # Increase stats considering the gym level: Formula >>>  (energy * (1.5 * gymlevel))
            player.str = player.str + Decimal(((train['str'] * (1.5 * player.gym_level))))
            player.dex = player.dex + Decimal(((train['dex'] * (1.5 * player.gym_level))))
            player.spd = player.spd + Decimal(((train['spd'] * (1.5 * player.gym_level))))
            player.sta = player.sta + Decimal(((train['sta'] * (1.5 * player.gym_level))))
            player.acc = player.acc + Decimal(((train['acc'] * (1.5 * player.gym_level))))
            player.defn = player.defn + Decimal(((train['defn'] * (1.5 * player.gym_level))))
            # Reduce energy accordingly
            user.energy = user.energy - train['str'] - train['dex'] - train['spd'] - train['sta'] - train['acc'] - train['defn']
            # Update database accordingly
            player.save()
            user.save()
            # Prepare JsonResponse to return player data
            player_data = { 
                'pstr': player.str,
                'pdex': player.dex,
                'pspd': player.spd,
                'psta': player.sta,
                'pacc': player.acc,
                'pdefn': player.defn,
                'penergy': user.energy
            } 
            return JsonResponse(player_data)
        else:
            # Redirect to recovery
            return check_recovery(request, player_data)

# Recovery section
@csrf_exempt #TODO Change the 'exempt' workaround for better security!
@login_required
def recovering(request, mode):
    if request.method == "GET":
        # Load Images Carousel accordingly
        carousel = recovery_carousel(mode)
        # Get player data
        player = Player.objects.get(user=request.user)
        # Calculate time to recover for showing in template
        timer = player.awake_time - timezone.make_aware(datetime.now())
        timer = str(timer).split(".")[0]
        # Render template
        return render(request, "recovering.html", {
            "recovery_carousel": carousel,
            "timer": timer,
            "mode": mode
        })
        
    elif request.method == "POST":
        data = json.loads(request.body)
        # Check if "full" recovery or "KO" recovery
        if data['id'] == 'full':
            # Get player data
            player = Player.objects.get(user=request.user)
            # Calculate awake time
            player.sleep_time = timezone.make_aware(datetime.now())
            player.awake_time = player.sleep_time + timedelta(hours=8)
            player.recovery_mode = data['id']
            player.save()
            # Fill energy bar
            user = User.objects.get(username=request.user)
            user.energy = 100
            user.save()
            # Send Redirect to recovery
            return JsonResponse({"redirect": reverse('recovering', kwargs={'mode':'full'})})

        elif data['id'] == 'KO':
            player = Player.objects.get(user=request.user)
            # Calculate awake time
            player.sleep_time = timezone.make_aware(datetime.now())
            player.awake_time = player.sleep_time + timedelta(hours=2)
            player.recovery_mode = data['id']
            player.save()
            return JsonResponse({"redirect": reverse('recovering', kwargs={'mode':'KO'})})


# Function to process the actions from buttons in Place template (JS function "placeaction").
@csrf_exempt #TODO Change the 'exempt' workaround for better security!
@login_required
def placeaction(request):
    # Get player data
    player = Player.objects.get(user=request.user)
    player_user = User.objects.get(username=request.user)
    # Get passed data
    data = json.loads(request.body)
    # For updates on Database
    if request.method == "POST":
        # Check what button was clicked
        ## Gym buttons
        if data["action"] == "Join":
            # Identify where's the gym and check player funds to cover the fee:
                # For Fighter's District
            if data["zone"] == "Fighter's District" and player.gym_level != 3:
                if player_user.jabucks < 8000:
                    # Not enough funds
                    response_data = {
                    'message': 'join_fee', 
                    'fee': 8000
                    }
                else:
                    # Successful join. Assign the gym level accordingly, and update player funds
                    player_user.jabucks -= 8000
                    player_user.save()
                    player.gym_level = 3
                    player.joined_gym = True 
                    player.gym_name = "The Forge"
                    player.save()  
                    # Prepare JsonResponse. Pass the gym name to JS
                    response_data = {
                        'message': 'join_success', 
                        'gym': player.gym_name,
                        'jabucks_upd': player_user.jabucks
                    }
                return JsonResponse(response_data)
                
                #For Shadow Alley
            elif data["zone"] == "Shadow Alley" and player.gym_level != 2:
                if player_user.jabucks < 3000:
                    # Not enough funds
                    response_data = {
                    'message': 'join_fee', 
                    'fee': 3000
                    }
                else:
                    # Successful join. Assign the gym level accordingly, and update player funds
                    player_user.jabucks -= 3000
                    player_user.save()
                    player.gym_level = 2
                    player.joined_gym = True 
                    player.gym_name = "Chains & Fury"
                    player.save()  
                    # Prepare JsonResponse. Pass the gym name to JS
                    response_data = {
                        'message': 'join_success', 
                        'gym': player.gym_name,
                        'jabucks_upd': player_user.jabucks
                    }
                return JsonResponse(response_data)
            
            # If player is joining the same gym twice 
            elif (data["zone"] == "Fighter's District" and player.gym_level == 3) or (data["zone"] == "Shadow Alley" and player.gym_level == 2):
                # Failed join (already in this gym)
                return JsonResponse({'message': 'join_fail'},safe=False)                
            
        elif data["action"] == "Quit":
            # Cannot quit a gym from a different zone
            if (data["zone"] == "Fighter's District" and player.gym_level == 2) or (data["zone"] == "Shadow Alley" and player.gym_level == 3):
                # Determine the zone where player gym is located
                if player.gym_level == 2:
                    zone = "Shadow Alley"
                elif player.gym_level == 3:   
                    zone = "Fighter's District"
                # Prepare JsonResponse. Pass the gym name and zone to JS
                response_data = {
                    'message': 'quit_cannot', 
                    'gym': player.gym_name,
                    'zone': zone
                }
                return JsonResponse(response_data)
            
            # Successful quit (not in this gym or any other anymore)
            elif (data["zone"] == "Fighter's District" and player.gym_level == 3) or (data["zone"] == "Shadow Alley" and player.gym_level == 2):
                # Prepare JsonResponse. Pass the gym name to JS
                response_data = {
                    'message': 'quit_success', 
                    'gym': player.gym_name
                }
                # Update player model
                player.gym_level = 1
                player.joined_gym = False
                player.gym_name = "None"
                player.save()    
                return JsonResponse(response_data)
 
            else:
                # No gym joined
                return JsonResponse({'message': 'quit_fail'},safe=False)
            
        elif data["action"] == "Train":
            # Identify gym and player gym level to train accordingly
            if (data["zone"] == "Fighter's District" and player.gym_level == 3) or (data["zone"] == "Shadow Alley" and player.gym_level == 2) or data["zone"] == "Victory Plaza":
                return JsonResponse({"message": "train_success"},safe=False) 
            else:
                return JsonResponse({"message": "train_fail"},safe=False)
            
        ## Bar buttons 
        elif data["action"] == "Gossip":
            # Query the events model for all gossip-type events
            total = CityEvent.objects.filter(event_action=data["action"])
            # Randomize a number between 1 and the amount of events of this type 
            number = random.randint(1,len(total))
            # Get the random story/dialog from models using the number as ID
            event = CityEvent.objects.get(id=number)
            return JsonResponse({"message": "gossip", "text": event.event_text, "title": event.event_title}, safe=False)
        
        elif data["action"] == "Drink":
            # Spend 100 jabucks to fill out 60 energy. Only once per day
                # Check available funds and Check if player hasn't drink today
            if check_funds(player_user, 100) and check_refill(player_user):
                # Substract funds
                player_user.jabucks -= 100                
                # Add energy
                player_user.energy += 60
                # Save data and return to JS
                player_user.energy_drink = date.today()
                player_user.save()
                return JsonResponse({"message": "drink", "jabucks_upd": player_user.jabucks, "energy_upd": player_user.energy})   
                # If already refilled 
            elif not check_refill(player_user):
                return JsonResponse({"message": "no refill"})    
            else:
                # If no funds
                return JsonResponse({"message": "no funds"})
        
        # Titan Arena buttons
        elif data["action"] == "Challenges":
            return JsonResponse({"message": "redirect"})
            
        # If button is not an action, then is an area. Get area info to pass into template for its description.
        else:
            # Get correct area using the "place.full_name" attribute from foreignkey.
            area = AreaAction.objects.get(area=data["action"].capitalize(), place__full_name=data["zone"])
            # Return only intro message for area
            return JsonResponse({'message': area.area_intro}, safe=False)
        
    else:
        pass
    return HttpResponse({"message": "View process completed"},safe=False)         

# Function to process the challenges or fights.
@csrf_exempt #TODO Change the 'exempt' workaround for better security!
@login_required
def challenges(request):
    # Get Player data and convert his rank to an integer
    player_data = Player.objects.get(user=request.user)
    if request.method == 'GET':
        # Get all rivals (NPC) data to populate rankings table
        nonplayer_data = NonPlayer.objects.all().order_by('rank_hof')
        # Lock rivals too high from player rank. Cannot challenge over one place above (starting at 10th)
        if player_data.rank_hof != None:
            rivals_locked = player_data.rank_hof - 2
        else:
            rivals_locked = 9
        return render(request, "challenges.html", {
            "player": player_data,
            "nonplayer": nonplayer_data,
            "rivals_locked": rivals_locked
        })
        
    elif request.method == 'POST':
        # Process post data from template
        data = json.loads(request.body)
        # If match confirmation button
        if data['id'] == "confirmation":
            # Get selected rival data and calculate stats difference
            nonplayer_data = NonPlayer.objects.get(rank_hof=data['npc_rank'])
            statsdiff = {
                        'str': '',
                        'dex': '',
                        'sta': '',
                        'spd': '',
                        'acc': '',
                        'defn': '',
                    }   
                # Calculate
            statsdiff['str'] = round(player_data.str - nonplayer_data.str)
            statsdiff['dex'] = round(player_data.dex - nonplayer_data.dex)
            statsdiff['sta'] = round(player_data.sta - nonplayer_data.sta)
            statsdiff['spd'] = round(player_data.spd - nonplayer_data.spd)
            statsdiff['acc'] = round(player_data.acc - nonplayer_data.acc)
            statsdiff['defn'] = round(player_data.defn - nonplayer_data.defn)
            return JsonResponse({"npcname": nonplayer_data.name, "npcnickname":nonplayer_data.nickname, "prize": nonplayer_data.prize, "stat_diff": statsdiff}, safe=False)
        # If fight button
        elif data['id'] == "challengewin":
            # Process new rank, reputation and add prize to player's funds
            player_data.rank_hof = data['rank']
            if player_data.rank_hof == 1:
                player_data.reputation = 'Hall of Fame Legend'
            elif player_data.rank_hof == 3:
                player_data.reputation = 'World Champion'
            elif player_data.rank_hof == 5:
                player_data.reputation = 'Title Holder'
            elif player_data.rank_hof == 7:
                player_data.reputation = 'Professional Contender'
            elif  player_data.rank_hof == 10:
                player_data.reputation = 'Amateur Prospect'
            user_data = User.objects.get(username=request.user)
            user_data.jabucks = int(user_data.jabucks)
            user_data.jabucks += data['prize']
            user_data.save()
            player_data.save()
            # To Store Stats difference (for JS operations)
            return JsonResponse({"rank": data['rank'], "prize": data['prize']}, safe=False)

# Function to check available funds before any transaction
def check_funds(user, cost):
    if user.jabucks >= cost:
        return True
    else:
        return False
    
# Function to check if energy was refilled today    
def check_refill(user):
    if (user.energy_drink == None) or (date.today() - user.energy_drink != timedelta(days=0)):
        return True
    else:
        return False
    
# Function to set carousel of images 
def recovery_carousel(mode):
    if mode == 'full' :
        # Array of image names to pass to carousel. 
        carousel_images = ['Dream2.jpg','Dream3.jpg','Dream4.jpg','Dream5.jpg','Dream6.jpg','Dream7.jpg','Dream8.jpg']
    if mode == 'KO':
        carousel_images = ['KO2.jpg','KO3.jpg','KO4.jpeg','KO5.jpg']
    # Randomize images
    random.shuffle(carousel_images)
    return (carousel_images)

# Function to check if Player is still recovering
def check_recovery(request, player_data):
    if timezone.make_aware(datetime.now()) <= player_data.awake_time:
        # Redirect to recovery
        carousel = recovery_carousel(player_data.recovery_mode)
        timer = player_data.awake_time - timezone.make_aware(datetime.now())
        timer = str(timer).split(".")[0]
        return render(request, "recovering.html", {
            "recovery_carousel": carousel,
            "timer": timer,
            "mode": player_data.recovery_mode
        })
    else: 
        return "Not Recovering"