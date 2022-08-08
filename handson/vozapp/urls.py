from django.urls import path,include
from . import views

urlpatterns = [
    path('voz/', views.content_list,name='content_list'),
    path('pagi/', views.content_list1,name='content_list1'),
]