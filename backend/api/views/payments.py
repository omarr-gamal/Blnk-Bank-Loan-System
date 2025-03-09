from rest_framework import viewsets, permissions
from rest_framework.response import Response

from api.models import Payment
from api.serializers import PaymentSerializer
from api.services import PaymentProcessor


class PaymentViewSet(viewsets.ModelViewSet):
    """
    This endpoint allows the logged-in customer to make a loan repayment.
    
    To submit a payment, provide:
    - `loan`: ID of the loan being paid
    - `amount`: Amount to repay

    The response confirms successful payment processing.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(loan__customer__user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        loan = serializer.validated_data["loan"]
        amount = serializer.validated_data["amount"]

        payment = Payment.objects.create(loan=loan, amount=amount)
        PaymentProcessor.process_payment(payment=payment)

        return Response({"detail": "Payment successful."}, status=201)
