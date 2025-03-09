from datetime import timedelta

from django.db.models.signals import post_migrate
from django.dispatch import receiver

from django.db import models


class BankConfig(models.Model):
    min_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.DurationField()
    
    @staticmethod
    def get_config():
        return BankConfig.objects.get()
    
    def save(self, *args, **kwargs):
        if BankConfig.objects.exists() and not self.pk:
            raise ValueError("Only one BankConfig instance is allowed.")
        super().save(*args, **kwargs)

@receiver(post_migrate)
def create_bank_config(sender, **kwargs):
    if not BankConfig.objects.exists():
        BankConfig.objects.create(
            min_loan_amount=100,
            max_loan_amount=10000,
            interest_rate=0.05,
            duration=timedelta(days=365)
        )
