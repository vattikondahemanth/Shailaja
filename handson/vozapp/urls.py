from django.urls import path,include
from . import views

urlpatterns = [
    path('elid1/', views.content_list,name='content_list'),
    path('pagi/', views.content_list1,name='content_list1'),
    path('colsearch/', views.column_search,name='column_search'),
    path('ajax_infinite/', views.ajax_infinite,name='ajax_infinite'),
    path('get_all_dd_data/', views.get_all_drop_downs_data,name='get_all_dd_data'),
    path('get_hot_data/', views.get_hands_on_table_data,name='get_hot_data'),
    # path('elid/', views.elid,name='elid'),
    path('home/', views.home,name='elid'),



]