from rest_framework import serializers
from .models import Loan, Payment, LoanFunding, LoanCustomer, LoanProvider

class LoanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['duration', 'interest_rate', 'created_at', 'status']

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


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)

    class Meta:
        model = LoanCustomer
        fields = ['id', 'url', 'min_loan_amount', 'max_loan_amount', 'first_name', 'last_name']
        read_only_fields = ['id', 'min_loan_amount', 'max_loan_amount']
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return super().update(instance, validated_data)


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)

    class Meta:
        model = LoanProvider
        fields = ['id', 'url', 'fund_amount', 'wallet_amount', 'first_name', 'last_name']
        read_only_fields = ['id', 'fund_amount', 'wallet_amount']
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return super().update(instance, validated_data)

class AddFundsSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
