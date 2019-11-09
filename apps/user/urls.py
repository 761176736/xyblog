from django.urls import path,re_path
from . import views

app_name = 'user'

urlpatterns = [
    path('write/',views.Write_article.as_view(),name='write'),
    path('comment/',views.comment,name='comment'),
    path('like/',views.like,name='like'),
    path('upload/',views.upload,name='upload'),
    path('avatar/',views.upload_avatar,name='avatar'),
    path('change_email/',views.change_email,name='change_email'),
    path('change_username/',views.change_username,name='change_username'),
    re_path(r'^(\w+)/person/$',views.Person.as_view(),name='person')
]