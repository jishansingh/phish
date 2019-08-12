from django.urls import path,include,re_path
from . import views
urlpatterns = [
    path('',views.index),
    re_path(r'(?P<website>.*)/$',views.ViewPage),
]