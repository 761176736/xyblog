from django.urls import path,re_path
from . import views

app_name = 'blog'


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('about/', views.about, name='about'),
    path('message/',views.Messages.as_view(),name='message'),
    path('search/',views.search,name='search'),

    path('log_page/',views.log_page,name='log-page'),
    re_path(r'^(\w+)/article/(\d+)',views.detail,name='detail'),
    re_path(r'comments/(\d+)/',views.comments,name='comments'),
    re_path(r'^category/(\w+)/$',views.category_list,name='category'),
]