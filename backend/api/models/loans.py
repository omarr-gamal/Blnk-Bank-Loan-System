from django.db import models

from api.models.users import LoanCustomer, LoanProvider


class Loan(models.Model):
    customer = models.ForeignKey(LoanCustomer, on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    duration = models.DurationField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan {self.id} - {self.amount}"

class LoanFunding(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='fundings')
    provider = models.ForeignKey(LoanProvider, on_delete=models.CASCADE, related_name='fundings')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Loan {self.loan.id}"
