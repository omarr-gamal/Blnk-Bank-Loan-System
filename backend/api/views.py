from django.db import transaction
from django.db.models import F

from rest_framework import viewsets, serializers, permissions

from .models import Loan, Payment, LoanFunding, LoanProvider, LoanCustomer, BankConfig
from .serializers import LoanSerializer, PaymentSerializer, LoanFundingSerializer


class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Loan.objects.filter(customer__user=self.request.user)

    def perform_create(self, serializer):
        customer = LoanCustomer.objects.get(user=self.request.user)
        amount = serializer.validated_data['amount']
        
        # Check if amount is within customer's allowed range
        if amount < customer.min_loan_amount or amount > customer.max_loan_amount:
            raise serializers.ValidationError(f"Loan amount not within allowed range. Min: {customer.min_loan_amount}, Max: {customer.max_loan_amount}")
        
        with transaction.atomic():
            rate = BankConfig.objects.get().interest_rate
            duration = BankConfig.objects.get().duration
            loan = serializer.save(customer=customer, interest_rate=rate, duration=duration)
            
            remaining = loan.amount
            allocations = []

            for provider in LoanProvider.objects.filter(fund_amount__gt=0).order_by('id'):
                # Lock this provider row to use its funds.
                provider_locked = LoanProvider.objects.select_for_update().get(pk=provider.pk)
                available = provider_locked.fund_amount
                if available > 0:
                    allocation = min(available, remaining)
                    allocations.append((provider_locked, allocation))
                    remaining -= allocation
                if remaining <= 0:
                    break

            if remaining > 0:
                # Not enough funds; raising an error will roll back transaction.
                raise serializers.ValidationError("Not enough provider funds available.")

            # Update locked rows and create funding records.
            for provider_locked, allocation in allocations:
                LoanFunding.objects.create(loan=loan, provider=provider_locked, amount=allocation)
                provider_locked.fund_amount = F('fund_amount') - allocation
                provider_locked.save()


class LoanFundingViewSet(viewsets.ModelViewSet):
    queryset = LoanFunding.objects.all()
    serializer_class = LoanFundingSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
