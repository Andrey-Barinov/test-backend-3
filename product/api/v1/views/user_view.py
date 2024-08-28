from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from api.v1.serializers.user_serializer import (
    CustomUserSerializer,
    BalanceSerializer,
    BalanceUpdateSerializer
)
from users.models import Balance

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "head", "options"]
    permission_classes = (permissions.IsAdminUser,)


class BalanceViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        return Balance.objects.all()

    def get_serializer_class(self):
        if self.action == 'increase_balance':
            return BalanceUpdateSerializer
        return BalanceSerializer

    def get_object(self):
        # Получаем объект по pk баланса
        queryset = self.get_queryset()
        balance_id = self.kwargs.get('pk')
        obj = get_object_or_404(queryset, pk=balance_id)
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, methods=['patch'])
    def increase_balance(self, request, pk=None):
        balance = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            amount_to_add = serializer.validated_data['amount_to_add']
            balance.amount += amount_to_add
            balance.save()
            return Response(
                {'status': 'balance updated', 'new_balance': balance.amount}
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
