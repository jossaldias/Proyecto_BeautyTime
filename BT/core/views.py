import os
import requests

from django.shortcuts import render, redirect, get_object_or_404

def home(request):
    print(request.session.session_key)

    return render(request, 'base/home.html', {'home': home})

