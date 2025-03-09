from django.db import transaction
from django.db.models import F

from api.models import Payment


class PaymentProcessor:
    @staticmethod
    def process_payment(payment: Payment) -> None:
        """Process the loan repayment and update provider wallets."""
        with transaction.atomic():
            loan = payment.loan
            fundings = loan.fundings.all()

            for funding in fundings:
                provider = funding.provider
                proportion = funding.amount / loan.amount
                payment_amount = payment.amount * proportion

                provider.wallet_amount = F('wallet_amount') + payment_amount
                provider.save()

            loan.update_status()
