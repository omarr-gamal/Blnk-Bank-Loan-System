from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from api.models import BankConfig
from api.serializers import BankConfigSerializer 


class BankConfigViewSet(viewsets.ModelViewSet):
    """
    This endpoint retrieves the bank configuration settings.
    """
    queryset = BankConfig.get_config()
    serializer_class = BankConfigSerializer
    http_method_names = ['get', 'head', 'options']

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({}, status=404)
