from rest_framework import viewsets, serializers, permissions
from rest_framework.response import Response
from rest_framework import status

from api.models import Loan, LoanCustomer, BankConfig
from api.serializers import LoanSerializer
from api.services import LoanFundAllocator


class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Loan.objects.filter(customer__user=self.request.user)

    def perform_create(self, serializer):
        """Create a new loan and allocate funds from providers."""
        customer = LoanCustomer.objects.get(user=self.request.user)
        amount = serializer.validated_data['amount']
        
        if amount < customer.min_loan_amount or amount > customer.max_loan_amount:
            raise serializers.ValidationError(f"Loan amount not within allowed range. Min: {customer.min_loan_amount}, Max: {customer.max_loan_amount}")
        
        serializer.validated_data['customer'] = customer
        loan = serializer.save()
        
        try:
            LoanFundAllocator.fulfil_loan(loan=loan)
        except ValueError as e:
            loan.delete()
            raise serializers.ValidationError(str(e))
 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
