from django.contrib import admin

from .models import LoanProvider, LoanCustomer, Loan, LoanFunding, Payment, BankConfig


admin.site.register([LoanProvider, LoanCustomer, Loan, LoanFunding, Payment, BankConfig])
