from django.db import models
from django.db.models import Sum

from api.models.users import LoanCustomer, LoanProvider


class Loan(models.Model):
    class Status(models.TextChoices):
        PENDING_REPAYMENT = 'pending_repayment', 'Pending Repayment'
        PARTIALLY_PAID = 'partially_paid', 'Partially Paid'
        PAID = 'paid', 'Paid'
        OVERDUE = 'overdue', 'Overdue'
        DEFAULTED = 'defaulted', 'Defaulted'
        
    customer = models.ForeignKey(LoanCustomer, on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    duration = models.DurationField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING_REPAYMENT)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def amount_due(self):
        return self.amount + (self.amount * self.interest_rate)

    def get_total_paid(self):
        return self.payments.aggregate(Sum("amount"))["amount__sum"] or 0

    def get_remaining_balance(self):
        return self.amount_due - self.get_total_paid()

    def update_status(self):
        total_paid = self.get_total_paid()

        if self.status == Loan.Status.DEFAULTED or self.status == Loan.Status.PAID:
            return

        if total_paid >= self.amount_due:
            self.status = Loan.Status.PAID
        elif total_paid > 0:
            self.status = Loan.Status.PARTIALLY_PAID
        else:
            self.status = Loan.Status.PENDING_REPAYMENT

        self.save()

    def __str__(self):
        return f"Loan {self.id} - {self.amount} ({self.get_status_display()})"


class LoanFunding(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='fundings')
    provider = models.ForeignKey(LoanProvider, on_delete=models.CASCADE, related_name='fundings')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Loan {self.loan.id}"
