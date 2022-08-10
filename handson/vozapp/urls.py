from django.urls import path,include
from . import views

urlpatterns = [
    path('abc/', views.content_list,name='content_list'),
    path('pagi/', views.content_list1,name='content_list1'),
    path('colsearch/', views.column_search,name='column_search'),

]