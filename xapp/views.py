from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Wallet, Transaction
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .libs.cmc import get_crypto_data, get_coin_data
from .libs.paystack import initialize_payment, verify_payment
from django.http import HttpResponse




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



def history_view(request):
    return render(request, 'history.html')

def profile(request):
    user = request.user
    wallet = get_object_or_404(Wallet, user=user)
    return render(request, 'profile.html', {'user': user, 'wallet': wallet})


def trade_view(request):
    return render(request, 'trade.html')


def xtrade_view(request, id=id):
    coin = get_coin_data(id)
    return render(request, 'xtrade.html', {"coin": coin})

import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

@csrf_exempt
def fund_wallet(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)     
            amount = data.get('amount')
        except Exception:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=401)

        email = user.email
        payment = initialize_payment(email=email, amount=amount)
        if payment:
            wallet = get_object_or_404(Wallet, user=user)
            Transaction.objects.create(
                wallet=wallet,
                amount=amount,
                type="CREDIT",
                category="DEPOSIT",
                reference=payment['reference'],
                previous_balance=wallet.balance
            )
            return JsonResponse({"url": payment['url']})
        
        return JsonResponse({"error": "Failed to initialize payment"}, status=400)

    return HttpResponse(status=405)  

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Transaction


@csrf_exempt
def verify_service(request, reference):
    ftst = verify_payment(reference=reference)
    trans = get_object_or_404(Transaction, reference=ftst['reference'])

    if ftst['status'] == 'success':
        trans.status = Transaction.Status.COMPLETED
        trans.previous_balance = trans.wallet.balance
        trans.new_balance = trans.wallet.balance + trans.amount
        # update wallet balance
        trans.wallet.balance = trans.new_balance
        trans.wallet.save()
        trans.save()

    elif ftst['status'] == 'failed':
        trans.status = Transaction.Status.FAILED
        trans.save()

    elif ftst['status'] == 'cancelled':
        trans.status = Transaction.Status.CANCELLED
        trans.save()

    else:
        # if for any reason Paystack/processor returns something unexpected
        trans.status = Transaction.Status.PENDING
        trans.save()

    return JsonResponse({
        "reference": trans.reference,
        "status": trans.status,
        "wallet_balance": str(trans.wallet.balance)
    })



def callback_page(request):
    return render(request, 'callback.html')