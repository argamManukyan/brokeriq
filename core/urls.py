from django.urls import path
from rest_framework.generics import DestroyAPIView

from .views import *




urlpatterns = [

    # Solutions CRUD
    path('solutions/',ListAndCreateSolution.as_view(),name='solutions'),
    path('solutions/<int:pk>/',ReadAndChangeSolutionAPI.as_view(),name='solutions_read'),
   
    # Solutions CRUD
    
    path('challenges/',ListAndCreateChallengeAPI.as_view(),name='challenges_list'),
    path('challenges/<int:pk>/',ReadAndChangeChallengeAPI.as_view(),name='challenges_read'),

      # Bank CRUD
    path('banks/', ListAndCreateBankAPI.as_view(),name='banks'),
    path('banks/<int:pk>/',ReadAbdChangeBankAPI.as_view(),name='banks_read'),
    # Bank CRUD
    
    #Bank Combinations
    # path('bank-combinations/',BankCoefficientListAPI.as_view(),name='bank_coefficient'),
    path('bank-combinations/create/',BankCoefficientCreateAPI.as_view(),name='bank_coefficient_create'),
    path('bank-combinations/update/',BankCoefficientUpdateAPI.as_view(),name='bank_coefficient_update'),
    path('bank-combinations/delete/',BankCoefficientDestroyAPIView.as_view(),name='bank_coefficient_destroy'),
    path('bank-combinations/remove/',BankCombinationRemove.as_view(),name='bank_coefficient_remove'),
    path('bank-image/<pk>/',BankImageAPI.as_view()),
    #Bank Combinations


] 
