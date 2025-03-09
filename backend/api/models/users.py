from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .bank_config import BankConfig


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

@receiver(pre_save, sender=LoanCustomer)
def set_default_customer_limits(sender, instance: LoanCustomer, **kwargs):
    instance.min_loan_amount = BankConfig.get_config().min_loan_amount
    instance.max_loan_amount = BankConfig.get_config().max_loan_amount
