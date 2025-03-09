from rest_framework import serializers
from .models import Loan, Payment, LoanFunding, LoanCustomer, LoanProvider

class LoanSerializer(serializers.HyperlinkedModelSerializer):
    remaining_balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, source='get_remaining_balance')
    amount_due = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_paid = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, source='get_total_paid')
    
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = [
            'duration', 'interest_rate', 'created_at', 'status', 'customer', 
            'amount_due', 'remaining_balance', 'total_paid' 
        ]

class LoanFundingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LoanFunding
        fields = '__all__'

class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, 
        help_text="Amount to repay for a loan."
    )
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['payment_date']

    def validate(self, data):
        loan: Loan = data["loan"]
        amount = data["amount"]
        
        request_user = self.context["request"].user
        if loan.customer.user != request_user:
            raise serializers.ValidationError("You can only pay back your own loans.")

        if loan.status == Loan.Status.PAID:
            raise serializers.ValidationError("This loan has already been paid off.")
        if loan.status == Loan.Status.DEFAULTED:
            raise serializers.ValidationError("This loan has been defaulted.")

        if amount > loan.get_remaining_balance():
            raise serializers.ValidationError("Payment amount exceeds the remaining balance.")

        return data
        

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
