from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    energy=models.SmallIntegerField(default=100) # To track Player's energy. Shows at top nav bar (passed to Layout)
    jabucks=models.PositiveIntegerField(default=1000, null=True, blank=True) # For Player's cash. In-game currency is called Jabucks. Show at top nav bar (passed to Layout)
    energy_drink=models.DateField(null=True, blank=True, default=None) # When player drinks at bar (refill energy), set a date and store it. Can only refill once a day
    
    # Create a Player registry when a superuser is created in the terminal (e.g., via createsuperuser)
    def save(self, *args, **kwargs):  
        # When a new user is being created perform the default save              
        creating = self.pk is None                       
        super().save(*args, **kwargs)
        # Only for superusers, not regular users. Import inside method to avoid circular import and create a Player if not already existing                  
        if creating and self.is_superuser:               
            from .models import Player 
            Player.objects.get_or_create(user=self)

    # Format decimal to currency style
    def formatted_jabucks(self):
        # Format with commas and two decimal places
        return f"{self.jabucks:,}"
    
# Model for player (stats -up to 9,999,999.99-, reputation, fight history, etc). Linked to User.
class Player(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    rank_hof=models.PositiveIntegerField(null=True, blank=True, default=None) # Rank in Hall of Fame
    reputation=models.CharField(max_length=30, blank=True, default="Mr. Nobody")
    str=models.DecimalField(default=100, max_digits=8, decimal_places=1)    #Strength
    dex=models.DecimalField(default=100, max_digits=8, decimal_places=1)    #Dexterity
    spd=models.DecimalField(default=100, max_digits=8, decimal_places=1)    #Speed
    sta=models.DecimalField(default=100, max_digits=8, decimal_places=1)    #Stamina
    acc=models.DecimalField(default=100, max_digits=8, decimal_places=1)    #Accuracy
    defn=models.DecimalField(default=100, max_digits=8, decimal_places=1)   #Defense
    joined_gym=models.BooleanField(default=False)   #Check if player is in gym
    gym_name=models.CharField(max_length=50, default="None")
    gym_level=models.PositiveSmallIntegerField(default=1) #Gym level that player has joined. Influence the stats gain (multiplier)    
    sleep_time=models.DateTimeField(null=True, blank=True, default=timezone.make_aware(datetime.now())) # To track when clicking recovery button
    awake_time=models.DateTimeField(null=True, blank=True, default=timezone.make_aware(datetime.now())) # To track when the player ends recovery time. Formula: sleep + 8h (fills when clicking recovery button)
    recovery_mode=models.CharField(max_length=10, blank=True, default="") #Type of recovery (KO or rest)

    # Standard return
    def __str__(self):
        return f"User: {self.user.username}, Rank: {self.rank_hof}, Reputation: {self.reputation}, Strength:{self.str}, Dexterity: {self.dex}, Speed: {self.spd}, Stamina: {self.sta}, Accuracy: {self.acc}, Defense: {self.defn}, Joined a Gym?: {self.joined_gym}"
            
    # Formatted return. Player stats with commas (for showing in templates)
    def formatted_stats(self):
        return {
            "str": f"{self.str:,}", #Strength
            "dex": f"{self.dex:,}", #Dexterity
            "spd": f"{self.spd:,}", #Speed
            "sta": f"{self.sta:,}", #Stamina
            "acc": f"{self.acc:,}", #Accuracy
            "defn": f"{self.defn:,}" #Defense
        }
        
# Model for Rivals similar to Player with stats
class NonPlayer(models.Model):
    name=models.CharField(max_length=25, blank=False, null=False)
    nickname=models.CharField(max_length=20, null=True, blank=True)
    rank_hof=models.PositiveIntegerField(default=0) # Rank in Hall of Fame
    reputation=models.CharField(max_length=350)
    str=models.DecimalField(default=100, max_digits=8, decimal_places=1)    #Strength
    dex=models.DecimalField(default=100, max_digits=8, decimal_places=1)    #Dexterity
    spd=models.DecimalField(default=100, max_digits=8, decimal_places=1)    #Speed
    sta=models.DecimalField(default=100, max_digits=8, decimal_places=1)    #Stamina
    acc=models.DecimalField(default=100, max_digits=8, decimal_places=1)    #Accuracy
    defn=models.DecimalField(default=100, max_digits=8, decimal_places=1)   #Defense
    prize=models.PositiveIntegerField(default='0') # Prize after victory

    # Standard return
    def __str__(self):
        return f"Name: {self.name}, Rank: {self.rank_hof}, Reputation: {self.reputation}, Nickname: {self.nickname}, Prize: {self.prize}, Strength:{self.str}, Dexterity: {self.dex}, Speed: {self.spd}, Stamina: {self.sta}, Accuracy: {self.acc}, Defense: {self.defn}"
            
    # Formatted return. Player stats with commas (for showing in templates)
    def formatted_stats(self):
        return {
            "str": f"{self.str:,}", #Strength
            "dex": f"{self.dex:,}", #Dexterity
            "spd": f"{self.spd:,}", #Speed
            "sta": f"{self.sta:,}", #Stamina
            "acc": f"{self.acc:,}", #Accuracy
            "defn": f"{self.defn:,}" #Defense
        }
       
# For City and Places:
    # A record for each Place (district) in the City
class Place(models.Model):
    full_name=models.CharField(max_length=40, blank=True) # Full name of the place.
    id_name=models.CharField(max_length=15, blank=True)   # ID or short name of the place. Used in template id="" tag
    image=models.CharField(max_length=100, blank=True) # Image name at "static" path for evey place. Used in template <img src=""> tag
    description=models.CharField(max_length=1000, blank=True) # Description of the place. Used in Place template to describe the location.
 
    def __str__(self):
        return f"{self.full_name}, Id: {self.id_name}, Description: {self.description}, Image: {self.image}"
    
# Each Place has different Areas and each Area has different Actions. This model is used for navigation, to auto generate the buttons for each area and action in "Place" HTML template
class AreaAction(models.Model):
    place=models.ForeignKey(Place, on_delete=models.CASCADE) # To identify the Place where the areas and actions are executed.
    area_intro=models.CharField(max_length=1200, blank=True) # Intro text for the area the player is in.
    # Each Place has different Areas (variable "area" as Key), each Area have different Actions (variable "actions" as an Array of Values). EX >>>  area: Bar || actions: Drink, Socialize.
    area=models.CharField(max_length=20, blank=True) # To populate left section of "Place" (passed to HTML template). Also used as Area Title (Heading for area_intro text in the "Place" template)
    actions=models.JSONField(null=True) # To populate right section of "Place" (passed to HTML template) An array of strings (actions) that will be passed to populate the button names.
    
    def __str__(self):
        return f"Zone: {self.place.full_name}, Area: {self.area}, Text: {self.area_intro}, Actions: {self.actions}"

# For text events occurring at some areas/places in the City. Linked to the action button (in template) and the variable from model AreaAction.
class CityEvent(models.Model):
    area=models.ForeignKey(AreaAction, on_delete=models.CASCADE)
    event_action=models.CharField(max_length=50, blank=True) #Action that triggers the event 
    event_title=models.CharField(max_length=50, blank=True) #Event Title
    event_text=models.CharField(max_length=1200, blank=True) # Event dialog/text
    
    def __str__(self):
        return f"{self.area}, Action: {self.event_action}, Title: {self.event_title}, Text: {self.event_text}"
    

    
    
    
    

    