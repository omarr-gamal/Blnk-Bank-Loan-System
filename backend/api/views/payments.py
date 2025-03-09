from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Payment, Loan
from api.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(loan__customer__user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Allows the logged-in customer to make a loan repayment."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        loan = serializer.validated_data["loan"]
        amount = serializer.validated_data["amount"]

        Payment.objects.create(loan=loan, amount=amount)
        loan.update_status()

        return Response({"detail": "Payment successful."}, status=201)
