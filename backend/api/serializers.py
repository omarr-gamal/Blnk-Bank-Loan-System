from rest_framework import serializers
from .models import Loan, Payment, LoanFunding, LoanCustomer

class LoanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Loan
        fields = ['url', 'amount', 'duration', 'interest_rate', 'created_at']
        read_only_fields = ['duration', 'interest_rate', 'created_at']

class LoanFundingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LoanFunding
        fields = '__all__'

    # def validate(self, data):
    #     provider = data['provider']
    #     loan = data['loan']
    #     amount = data['amount']
    #     if amount > provider.available_funds():
    #         raise serializers.ValidationError("Provider does not have enough available funds")
    #     remaining = loan.amount - loan.total_funded()
    #     if amount > remaining:
    #         raise serializers.ValidationError("Funding amount exceeds remaining loan amount")
    #     return data

class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class CustomerSerializer(serializers.Serializer):
    class Meta:
        model = LoanCustomer
        fields = '__all__'
        # read_only_fields = ['min_loan_amount', 'max_loan_amount']
        