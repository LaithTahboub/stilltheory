from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('login', views.login, name='login')
    path('username', views.username_testpage, name='username'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login, name='login'),


    
    
]
