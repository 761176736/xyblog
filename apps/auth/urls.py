from django.urls import path
from . import views

app_name = 'auth'

#
urlpatterns = [
    path('log_page/register/',views.register,name='register'),
    path('log_page/login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout')
]