from django.urls import path
from .views import home, login_view, signup_view, profile, trade_view, xtrade_view, history_view, fund_wallet, verify_service, callback_page


urlpatterns = [    
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('profile/', profile, name='profile'),
    path("trade/", trade_view, name="trade-view"),
    path('history', history_view, name="history"),
    path('fund-wallet', fund_wallet, name="fund-wallet"),
    path("xtrade/<int:id>", xtrade_view, name="xtrade"),
    path('callback', callback_page, name="callback"),
    path('verify-payment', verify_service, name='verify-payment')
]