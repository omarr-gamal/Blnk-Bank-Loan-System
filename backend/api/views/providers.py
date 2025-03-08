from typing import override

from django.shortcuts import get_object_or_404 

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import LoanProvider
from api.serializers import AddFundsSerializer, ProviderSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    serializer_classes = {
        'add_funds': AddFundsSerializer,
    }
    default_serializer_class = ProviderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @override
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)
    
    def get_queryset(self):
        return LoanProvider.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def get_customer_by_id(self, request, pk=None):
        provider = get_object_or_404(LoanProvider, pk=pk)
        serializer = ProviderSerializer(provider)  # Use the correct serializer
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'])
    def update_current_user(self, request):
        """Allows the logged-in user to update their profile"""
        customer = get_object_or_404(LoanProvider, user=request.user)
        serializer = self.get_serializer(customer, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'])
    def add_funds(self, request):
        """Allows the logged-in provider to add funds for lending"""
        
        serializer = AddFundsSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']

            provider = LoanProvider.objects.get(user=request.user)

            provider.fund_amount += amount
            provider.save()

            return Response({
                "detail": "Funds successfully added.",
                "fund_amount": provider.fund_amount,
                "wallet_amount": provider.wallet_amount
            }, status=200)
        
        return Response(serializer.errors, status=400)
