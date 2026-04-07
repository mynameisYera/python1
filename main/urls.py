from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hello/', views.hello, name='hello'),
    path('users/', views.users_list, name='users'),
    path('register/', views.register, name='register'),
    path('items/', views.items_collection, name='items'),
    path('items/<int:pk>/', views.items_detail, name='item_detail'),
    path('favicon.ico', views.favicon, name='favicon'),
]
