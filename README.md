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

- Financial transactions are conducted in a single currency for simplicity. In real-world scenarios, currencies would be tracked, and amounts converted using exchange rates.
- A loan must be fully funded before being granted. In other words there are no partial loan fulfilment.
- Customers repay loans through multiple payments until the outstanding balance is fully paid.
- Providers have no control over loan interest rates, durations, or e recipients of their funds.

## Omissions: Non-Critical Heavy Lifting Tasks

These tasks were omitted to focus on core loan management functionality, and also to save time.

- Job scheduling for payment reminders, and marking overdue and default loans.
- Payment gateway integration for actual payment processing.
- Currency conversion and exchange rate handling.
- Detailed user profile management beyond basic information.

## Future Improvements

These are great additions I found no time to implement:

- Queueing unfunded loans for future funding: The way it is currently implemented, if a loan is not fully funded, it is rejected and it's up to the customer to reapply. A future enhancement could be to queue such loans for funding when more funds become available.
- Interest accrual on unpaid balances: Currently, the system does not accrue interest on unpaid loan balances. This could be added to reflect real-world loan scenarios where interest accumulates on overdue amounts.
- Payment schedules: Implementing payment schedules would allow customers to repay loans in installments over time.
- Calculate and use credit scores: Credit scores could be calculated from customer loan-taking behavior and used to prioritize loan fulfilment, adjust interest rates, increase loan limits, etc.

## Considerations Taken

- **Concurrent Runtime Enviroment**: The system is designed to handle concurrent requests and operations which handle financial transactions are wrapped in atomic transactions to ensure consistency and avoid race conditions.
  
  - **Atomic Transactions**:
Financial transactions are wrapped in atomic transactions so that changes are treated as a single unit of work. If for example the process of allocating funds for a loan fails midway for any reason, then the entire transaction is rolled back, preventing partial updates.

  - **Row-Level Locking**:
To prevent race conditions when multiple loans try to use the same provider funds, the rows are locked during the operation so that no other transaction can use them until the current transaction is complete. This ensures that the allocation process is safe even in a multi-threaded environment.

  - **In-place Field Updates with F()**:
The F() expression is used to atomically update fields in place. So as to prevent race conditions from happening during high concurrency.

## Models

### 1. LoanCustomer

Represents customers who can request loans.

### 2. LoanProvider

Represents entities that provide funds for loans.

### 3. Loan

Tracks loans requested by customers.

- Stores amount, duration, interest rate, and status.

### 4. LoanFunding

Records funding participations between providers and loans.

### 5. Payment

Tracks loan repayments by customers.

### 6. BankConfig

Stores global rules like minimum and maximum amounts, interest rate, and loan duration.

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
