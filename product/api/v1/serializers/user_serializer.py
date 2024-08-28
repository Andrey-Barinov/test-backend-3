from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers
from users.models import Subscription, Balance

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""
    subscriptions = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ("password",)


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'
        read_only_fields = ['id', 'user']


class BalanceUpdateSerializer(serializers.Serializer):
    amount_to_add = serializers.IntegerField(min_value=1)


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки. задание 2.3"""
    user = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)
    # TODO

    class Meta:
        model = Subscription
        fields = (
            'course',
            'user',
            'purchase_date '
        )
