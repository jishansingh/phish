from django.urls import path,include,re_path
from . import views
urlpatterns = [
    path('',views.index),
    path('new/',views.new),
    path('view/',views.view_pages),
    path('view/<id>/',views.view_pages),
    re_path(r'(?P<website>.*)/$',views.ViewPage),
    re_path(r'(?P<website>.*)$',views.ViewPage),
]