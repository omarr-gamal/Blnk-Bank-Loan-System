from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanViewSet, LoanFundingViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'loans', LoanViewSet)
router.register(r'fundings', LoanFundingViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
