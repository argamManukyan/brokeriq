from .models import UserPayments
from rest_framework import serializers


class AddPaymentSerializer(serializers.Serializer):

    number = serializers.CharField()
    exp_month  =serializers.IntegerField()
    exp_year = serializers.IntegerField()
    cvc = serializers.CharField()



class MakePaymentsSerializer(serializers.Serializer):

    tariff_id = serializers.IntegerField()


class ChangeDefaultPaymentSerializer(serializers.Serializer):

    customer_id = serializers.CharField()
    payment_method_id = serializers.CharField()


class CreateSubscriptionSerializer(serializers.Serializer):

    price_id = serializers.CharField()


class UnsubscribeSerializer(serializers.Serializer):

    subscription_id = serializers.CharField()

class ChangeSubscriptionSerializer(serializers.Serializer):

    subscription_id = serializers.CharField()
    price_id = serializers.CharField()


class DeletePaymentSerializer(serializers.Serializer):

    payment_method_id = serializers.CharField()


class UserPaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPayments    
        fields = "__all__"


class OrderingChallengeSerializer(serializers.Serializer):

    ordering = serializers.ListField()