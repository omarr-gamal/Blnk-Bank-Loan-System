from django.db import models
from django.contrib.auth.models import User


class LoanProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fund_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        help_text='Funds available for loan taking.',
        default=0.0
    ) 
    wallet_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        help_text='Earnings from paid back loans.',
        default=0.0
    )
    
    def __str__(self):
        return self.user.username


class LoanCustomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    min_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.user.username