from os import name
from django.urls import path
from .views import *

urlpatterns = [

    path('customer/', CustomerDetailsAPI.as_view(), name='customer'),
    path('fetch-plans/', FetchPlansAPI.as_view(), name='fetch_plan'),
    path('fetch-payments/', FetchPaymentsAPi.as_view(), name='fetch_payments'),
    path('change-default-payment/', ChangeDefaultPayment.as_view(),
         name='change_default_payment'),
    path('create-customer/', create_customer, name='create_customer'),
    path('create-subscription/', CreateSubscriptionAPI.as_view(), name='create_subscription'),
    path('delete-subscription/', UnSubscribeAPI.as_view(), name='create_subscription'),
    path('add-payment/', AddPaymentAPI.as_view(), ),
    path('delete-payment/', DeletePaymentAPI.as_view(), ),
    path('payment-history/',UserPaymentHistoryAPI.as_view(),name='user_payments'),
    path('subscription/webhook/',my_webhook_view,name="webhook"),
    path('ordering-challenge/',ChangeOrderingChallenges.as_view())
]
