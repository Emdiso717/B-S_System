from django.urls import path
from .views import login
from .views import register
from .views import search
from .views import add
urlpatterns = [
    path('login/register',register,name='register'),
    path('login',login,name='login'),

    path('search',search,name='search'),

    path('add',add,name='add')
]