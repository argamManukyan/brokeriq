from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [

    path('clients/<int:pk>/',ClientDetailViewAPI.as_view()),
    path('clients/',ClientsListAPI.as_view(),name='clients')
] 