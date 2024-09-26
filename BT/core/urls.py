from django.urls import path

from . import views


urlpatterns = [
    # INICIO
    path("", views.home, name="home"),

]