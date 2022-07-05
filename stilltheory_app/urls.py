from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('login', views.login, name='login')
    path('username', views.username_testpage, name='username'),
    path('dashboard/<str:username>/<int:usr_id>', views.dashboard, name='dashboard'),
    path('get_token', views.get_token, name='get_token'),
    path('login/<str:code_verifier>/<str:code_challenge>/<str:token>', views.login, name='login'),
    path('finish_login/<str:token>', views.finish_login, name='finish_login')   
]