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
    
    @action(detail=True, methods=['get'], description="Retrieve the customer's profile")
    def get_customer_by_id(self, request, pk=None):
        """Returns a specific customer by ID"""
        customer = get_object_or_404(LoanCustomer, pk=pk)
        serializer = self.get_serializer(customer)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'], description="Update the customer's profile")
    def update_current(self, request):
        """Allows the logged-in user to update their profile"""
        customer = get_object_or_404(LoanCustomer, user=request.user)
        serializer = self.get_serializer(customer, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    