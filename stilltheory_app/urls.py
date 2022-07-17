from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('login', views.login, name='login')
    path('username', views.username_testpage, name='username'),
    path('dashboard/<str:username>/<int:usr_id>', views.dashboard, name='dashboard'),
    path('get_token', views.get_token, name='get_token'),
    re_path(r'^login/(?P<code>\w)/(?P<state>\w)$', views.login, name='login'),
    path('finish_login/<str:token>', views.finish_login, name='finish_login'),
    # pieces:
]