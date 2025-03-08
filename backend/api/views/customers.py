from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404 

from api.models import LoanCustomer
from api.serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LoanCustomer.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def get_customer_by_id(self, request, pk=None):
        """Returns a specific customer by ID"""
        customer = get_object_or_404(LoanCustomer, pk=pk)
        serializer = self.get_serializer(customer)
        return Response(serializer.data)
    