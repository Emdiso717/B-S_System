from django.urls import path
from .views import login
from .views import register
from .views import searchJD
from .views import add
from .views import search_car
from .views import car_delete
from .views import searchSN
from .views import searchA
urlpatterns = [
    path('login/register',register,name='register'),
    path('login',login,name='login'),

    path('searchJD',searchJD,name='searchJD'),
    path('searchSN', searchSN, name='searchSN'),
    path('searchA', searchA, name='searchA'),
    path('add',add,name='add'),

    path('scar',search_car,name='scar'),

    path('delete',car_delete,name='delete')
]