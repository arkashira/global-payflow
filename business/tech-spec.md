```markdown
# Technical Specification for Global Payflow

## Stack
- **Language**: TypeScript
- **Framework**: Node.js with Express.js
- **Runtime**: Docker containers for microservices architecture

## Hosting
- **Free-tier-first**: 
  - **Platforms**: 
    - Heroku (for initial deployment and testing)
    - AWS (for scalable production deployment)
    - DigitalOcean (for cost-effective hosting solutions)
  - **Free Tier**: Utilize AWS Free Tier for initial usage, including Lambda functions and DynamoDB.

## Data Model
### Tables/Collections
1. **Users**
   - `user_id`: UUID (Primary Key)
   - `email`: String (Unique)
   - `password_hash`: String
   - `role`: Enum (Admin, User, Merchant)

2. **Transactions**
   - `transaction_id`: UUID (Primary Key)
   - `user_id`: UUID (Foreign Key)
   - `amount`: Decimal
   - `currency`: String
   - `status`: Enum (Pending, Completed, Failed)
   - `created_at`: Timestamp

3. **Payment_Methods**
   - `payment_method_id`: UUID (Primary Key)
   - `user_id`: UUID (Foreign Key)
   - `type`: Enum (Credit Card, Bank Transfer, Digital Wallet)
   - `details`: JSON (Encrypted)

4. **Exchange_Rates**
   - `rate_id`: UUID (Primary Key)
   - `from_currency`: String
   - `to_currency`: String
   - `rate`: Decimal
   - `updated_at`: Timestamp

## API Surface
1. **User Registration**
   - **Method**: POST
   - **Path**: `/api/v1/users/register`
   - **Purpose**: Register a new user.

2. **User Login**
   - **Method**: POST
   - **Path**: `/api/v1/users/login`
   - **Purpose**: Authenticate a user and return a JWT token.

3. **Create Transaction**
   - **Method**: POST
   - **Path**: `/api/v1/transactions`
   - **Purpose**: Initiate a new transaction.

4. **Get Transaction Status**
   - **Method**: GET
   - **Path**: `/api/v1/transactions/:transaction_id`
   - **Purpose**: Retrieve the status of a specific transaction.

5. **List User Transactions**
   - **Method**: GET
   - **Path**: `/api/v1/users/:user_id/transactions`
   - **Purpose**: List all transactions for a specific user.

6. **Add Payment Method**
   - **Method**: POST
   - **Path**: `/api/v1/payment_methods`
   - **Purpose**: Add a new payment method for a user.

7. **Get Exchange Rate**
   - **Method**: GET
   - **Path**: `/api/v1/exchange_rates/:from_currency/:to_currency`
   - **Purpose**: Retrieve the current exchange rate between two currencies.

## Security Model
- **Authentication**: JWT (JSON Web Tokens) for user sessions.
- **Secrets Management**: Use AWS Secrets Manager to store sensitive information like database credentials and API keys.
- **IAM**: Implement role-based access control (RBAC) to manage user permissions based on roles.

## Observability
- **Logs**: Utilize Winston for logging application events and errors.
- **Metrics**: Integrate Prometheus for collecting metrics on API usage and performance.
- **Traces**: Use OpenTelemetry for distributed tracing to monitor request flows through microservices.

## Build/CI
- **CI/CD Pipeline**: 
  - Use GitHub Actions for Continuous Integration and Continuous Deployment.
  - Automated tests on pull requests.
  - Deploy to staging on successful builds, with manual approval for production deployment.
```
