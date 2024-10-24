from django.urls import path

from . import views

urlpatterns = [
    # INICIO
    path("webpay-plus/create", views.webpay_plus_create, name="create"),
    path("webpay-plus/commit", views.webpay_plus_commit, name="commit"),


]