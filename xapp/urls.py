from django.urls import path
from .views import home, login_view, signup_view, profile, trade_view, xtrade_view


urlpatterns = [    
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('profile/', profile, name='profile'),
    path("trade/", trade_view, name="trade-view"),
    path("xtrade/<int:id>", xtrade_view, name="xtrade")
]