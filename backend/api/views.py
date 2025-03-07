from rest_framework import viewsets
from .models import Loan, Payment, LoanFunding
from .serializers import LoanSerializer, PaymentSerializer, LoanFundingSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class LoanFundingViewSet(viewsets.ModelViewSet):
    queryset = LoanFunding.objects.all()
    serializer_class = LoanFundingSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
