from django.contrib import admin
from .models import User, Place, Player, AreaAction, CityEvent, NonPlayer

# Register your models here.
admin.site.register(User)
admin.site.register(Player)
admin.site.register(NonPlayer)
admin.site.register(Place)
admin.site.register(AreaAction)
admin.site.register(CityEvent)
