from django.urls import path
from .views import home, login_view, signup_view, profile


urlpatterns = [    
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('profile/', profile, name='profile'),
]