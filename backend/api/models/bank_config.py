from django.db import models


class BankConfig(models.Model):
    min_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.DurationField()
