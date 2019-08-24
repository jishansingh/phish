from django.urls import path,include,re_path
from . import views
urlpatterns = [
    path('',views.index),
    path('new/',views.new),
    path('view/',views.view_pages),
    path('view/<id>/',views.view_pages),
    path('register/',views.view_pages),
    path('login/',views.user_login),
    path('register/',views.register),
    path('logout/',views.logout),
    re_path(r'(?P<website>.*)/$',views.ViewPage),
    re_path(r'(?P<website>.*)$',views.ViewPage),
]