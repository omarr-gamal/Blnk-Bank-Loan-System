from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanViewSet, PaymentViewSet, CustomerViewSet, ProviderViewSet, BankConfigViewSet

router = DefaultRouter()
router.register(r'loans', LoanViewSet, basename='loan')
router.register(r'customers', CustomerViewSet, basename='loancustomer')
router.register(r'providers', ProviderViewSet, basename='loanprovider')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'bank_configuration', BankConfigViewSet, basename='bankconfig')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
