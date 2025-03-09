from django.db import transaction
from django.db.models import F

from api.models import LoanFunding, LoanProvider, Loan, BankConfig


class LoanFundAllocator:
    @staticmethod
    def fulfil_loan(loan: Loan) -> None:
        """Allocate funds from providers to a loan."""
        
        with transaction.atomic():
            remaining = loan.amount
            allocations = []

            for provider in LoanProvider.objects.filter(fund_amount__gt=0).order_by('fund_amount'):
                # Lock this provider row to use its funds.
                provider_locked = LoanProvider.objects.select_for_update().get(pk=provider.pk)
                available = provider_locked.fund_amount
                if available > 0:
                    allocation = min(available, remaining)
                    allocations.append((provider_locked, allocation))
                    remaining -= allocation
                if remaining <= 0:
                    break

            if remaining > 0:
                raise ValueError("Not enough funds available.")

            # Update locked rows and create funding records.
            for provider_locked, allocation in allocations:
                LoanFunding.objects.create(loan=loan, provider=provider_locked, amount=allocation)
                provider_locked.fund_amount = F('fund_amount') - allocation
                provider_locked.save()
