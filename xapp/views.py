from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .libs.cmc import get_crypto_data, get_coin_data




def home(request):
    coins = get_crypto_data()[:5]
    print(coins)
    return render(request, 'index.html', {"coins": coins})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
    return render(request, 'login.html')


def signup_view(request):
    return render(request, 'signup.html')




def profile(request):
    return render(request, 'profile.html')


def trade_view(request):
    return render(request, 'trade.html')


def xtrade_view(request, id=id):
    coin = get_coin_data(id)
    return render(request, 'xtrade.html', {"coin": coin})