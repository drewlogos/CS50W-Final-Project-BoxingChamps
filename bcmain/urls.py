from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="welcome"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # Home and recovery pages
    path("home", views.home, name="home"),
    path("recovering/<str:mode>", views.recovering, name="recovering"),
    # City and Navigation
    path("city", views.city, name="city"),
    path("city/<str:place>", views.places, name="places"),
    path("gym", views.gym, name="gym"), # This includes gym actions too (train)
    path("challenges", views.challenges, name="challenges"), # For matches and progression in ranks
    # Action button
    path("paction", views.placeaction, name="paction")
]
