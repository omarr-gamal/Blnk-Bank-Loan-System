from rest_framework import viewsets, serializers, permissions

from api.models import LoanCustomer
from api.serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = LoanCustomer.objects.all()
    # def get_queryset(self):
    #     return 
