from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404 

from api.models import LoanProvider
from api.serializers import ProviderSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LoanProvider.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def get_customer_by_id(self, request, pk=None):
        customer = get_object_or_404(LoanProvider, pk=pk)
        serializer = self.get_serializer(customer)
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
