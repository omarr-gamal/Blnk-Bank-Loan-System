from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanViewSet, PaymentViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'loans', LoanViewSet, basename='loan')
router.register(r'customers', CustomerViewSet, basename='loancustomer')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
