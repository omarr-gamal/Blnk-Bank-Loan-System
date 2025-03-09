# Loan Management Platform

## Overview

This project is a Django-based loan management platform that allows customers to request loans, make repayments, and manage their loan accounts. Loan providers can fund loans and track their wallet balances. The system enforces loan rules and automatically updates balances based on payments.

## Architecture

The platform is built using Django and Django REST Framework (DRF). It follows a modular architecture with clear separation of concerns:

- **Loan Management**: Handles loan creation, tracking, and repayments.
- **Funding System**: Allows loan providers to fund loans.
- **Payment Processing**: Manages loan repayments and updates provider wallets.
- **Bank Configuration**: Stores global loan settings like interest rates and durations.

## Loan Fulfillment Process
1. **Loan Request:** A customer requests a loan specifying the amount.
2. **Validation:** The system checks if the requested amount falls within the allowed range.
3. **Funding Allocation:** Funds are allocated from available providers using the `LoanFundAllocator` service.
4. **Loan Creation:** Once fully funded, the loan is created and stored in the system.
5. **Disbursement:** The funds become available to the borrower, marking the loan as "Active."

If sufficient funds are unavailable, the loan request is rejected.

## Assumptions
- A loan must be fully funded before being granted.
- Customers repay loans in multiple payments until the balance reaches zero. 
- Only one `BankConfig` instance exists, defining default loan parameters.
- Providers pre-load funds into the platform for loans and have no control over loan interest rates, durations, or to whom their funds are lent.

## Design Choices
### **1. Separate Services for Business Logic**
- **`LoanFundAllocator`**: Handles loan funding by distributing available funds from providers.
- **`PaymentProcessor`**: Handles loan repayments and updates provider wallet balances.

### **2. Atomic Transactions**
- Loan funding and repayment operations are wrapped in transactions to ensure data consistency.

### **3. Read-Optimized API Design**
- API responses include computed fields (`remaining_balance`, `amount_due`, `total_paid`) for convenience.
- A single `BankConfig` instance is exposed via a dedicated read-only API.

## Future Enhancements
- Dynamic interest rates per provider
- Partial loan funding and batch approvals
- Notifications for due payments

## Models

### 1. LoanCustomer

Represents customers who can request loans.

- Linked to a Django `User` model.
- Defines min/max loan amounts for the customer.

### 2. LoanProvider

Represents entities that provide funds for loans.

- Each provider has a wallet balance used for funding loans.

### 3. Loan

Tracks loans requested by customers.

- Stores amount, duration, interest rate, and status.
- Uses `related_name='loans'` to allow querying loans by customer.

### 4. LoanFunding

Records funding transactions between providers and loans.

### 5. Payment

Tracks loan repayments by customers.

- Uses `related_name='payments'` to link payments to a loan.
- Payments reduce outstanding balances and update provider wallets.

### 6. BankConfig

Stores global loan rules like minimum and maximum amounts, interest rate, and loan duration.

## Services

### 1. **PaymentProcessor**

Handles loan repayments:

- Creates payment records.
- Updates loan balance.
- Adjusts provider wallets.

### 2. **LoanFundAllocator**

Manages loan funding:

- Allocates funds from providers.
- Ensures loan funding rules are followed.

## API Endpoints

### Customers

- `GET /api/customers/` - List customers.
- `PATCH /api/customers/me/` - Update the logged-in customer's profile.

### Loans

- `POST /api/loans/` - Request a loan.
- `GET /api/loans/` - List loans.
- `GET /api/loans/{id}/` - Retrieve a loan.

### Payments

- `POST /api/payments/` - Repay a loan.
- `GET /api/payments/` - List payments.

### Providers

- `POST /api/providers/add_funds/` - Add funds to a provider wallet.

### Bank Configuration

- `GET /api/bank_configuration/` - Retrieve global loan settings.

## Database Transactions

- Loan payments and provider wallet updates are handled within **atomic transactions** to ensure consistency.

## Security & Permissions

- Customers can only access their own loans and payments.
- Loan providers can only manage their own funds.
- Bank configuration is read-only via API.

## Future Enhancements

- Implement interest accrual on unpaid balances.
- Add loan repayment schedules.
- Introduce notifications for due payments.
- Extend the funding system to support multiple providers per loan.

This README provides an overview of the system's design and functionality, ensuring clarity on how the platform operates.


***************************************************************************************************************************************************
# Loan Management System

## Overview
This system facilitates loan processing, from funding by providers to repayment by customers. The design ensures financial integrity, efficient loan allocation, and proper tracking of transactions.




