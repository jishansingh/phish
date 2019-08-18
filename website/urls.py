from django.urls import path,include,re_path
from . import views
urlpatterns = [
    path('',views.index),
    path('new/',views.new),
    re_path(r'(?P<website>.*)/$',views.ViewPage),
    re_path(r'(?P<website>.*)$',views.ViewPage),
]