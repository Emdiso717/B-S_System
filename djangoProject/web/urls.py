from django.urls import path
from pkg_resources.extern import names

from .check_price import check_price
from .views import login
from .views import register
from .views import searchJD
from .views import add
from .views import search_car
from .views import car_delete
from .views import searchSN
from .views import searchA
from .views import get_A
from .views import login_A
from .views import get_SN
from .views import login_SN
from .views import get_JD
from .views import login_JD
from .views import get_price
from .views import down
from .views import get_account
from .views import send_email

urlpatterns = [
    path('login/register',register,name='register'),
    path('login',login,name='login'),

    path('searchJD',searchJD,name='searchJD'),
    path('searchSN', searchSN, name='searchSN'),
    path('searchA', searchA, name='searchA'),
    path('add',add,name='add'),

    path('scar',search_car,name='scar'),

    path('delete',car_delete,name='delete'),
    path('get_A',get_A,name='get_A'),
    path('login_A',login_A,name='login_A'),
    path('login_SN',login_SN,name='login_SN'),
    path('get_SN',get_SN,name='get_SN'),
    path('login_JD', login_JD, name='login_JD'),
    path('get_JD', get_JD, name='get_JD'),
    path('new_price',get_price,name='get_price'),
    path('down',down,name='down'),
    path('get_account',get_account,name='get_account'),
    path('send',send_email,name='send_email')
]