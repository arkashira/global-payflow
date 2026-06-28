```markdown
# Dataflow Architecture for Global Payflow

## External Data Sources
- **Payment Gateways**: APIs from various payment processors (e.g., Stripe, PayPal, Square).
- **Banking APIs**: Data from banks for transaction validation and fund transfers.
- **Currency Exchange Rates**: APIs providing real-time exchange rates (e.g., Open Exchange Rates).
- **Fraud Detection Services**: External services for risk assessment and fraud detection (e.g., Sift, Kount).
- **User Data Sources**: Customer information from CRM systems and user profiles.

## Ingestion Layer
```
+--------------------+
|   Ingestion Layer   |
|                    |
|   +--------------+ |
|   | API Gateway  | | <--- Auth Boundary
|   +--------------+ |
|   | Message Queue | |
|   +--------------+ |
+--------------------+
```
- **API Gateway**: Handles incoming requests from external data sources and clients.
- **Message Queue**: Manages asynchronous processing of incoming data (e.g., RabbitMQ, Kafka).

## Processing/Transform Layer
```
+-------------------------+
| Processing/Transform Layer |
|                         |
|   +-------------------+ |
|   | Data Processor    | |
|   +-------------------+ |
|   | Fraud Detection    | |
|   +-------------------+ |
|   | Currency Converter | |
|   +-------------------+ |
+-------------------------+
```
- **Data Processor**: Validates and transforms incoming data into a standardized format.
- **Fraud Detection**: Analyzes transactions for potential fraud using external services.
- **Currency Converter**: Converts transaction amounts based on real-time exchange rates.

## Storage Tier
```
+---------------------+
|     Storage Tier    |
|                     |
|   +---------------+ |
|   | Relational DB | | <--- Auth Boundary
|   +---------------+ |
|   | NoSQL DB      | |
|   +---------------+ |
|   | Data Warehouse | |
|   +---------------+ |
+---------------------+
```
- **Relational Database**: Stores structured transaction data (e.g., PostgreSQL).
- **NoSQL Database**: Stores unstructured or semi-structured data (e.g., MongoDB).
- **Data Warehouse**: Aggregates data for analytics and reporting (e.g., Snowflake).

## Query/Serving Layer
```
+---------------------+
|   Query/Serving Layer |
|                     |
|   +---------------+ |
|   | API Layer     | | <--- Auth Boundary
|   +---------------+ |
|   | Analytics API | |
|   +---------------+ |
+---------------------+
```
- **API Layer**: Provides endpoints for clients to access transaction data and analytics.
- **Analytics API**: Serves aggregated data for reporting and insights.

## Egress to User
```
+---------------------+
|    Egress to User   |
|                     |
|   +---------------+ |
|   | Client Apps   | |
|   +---------------+ |
|   | Web Portal    | |
|   +---------------+ |
|   | Mobile App    | |
|   +---------------+ |
+---------------------+
```
- **Client Apps**: Interfaces for users to interact with the payment platform (e.g., web and mobile applications).
- **Web Portal**: Dashboard for users to manage transactions and view analytics.

## Auth Boundaries
- **API Gateway**: Enforces authentication and authorization for all incoming requests.
- **Storage Tier**: Access control to databases ensuring only authorized services can read/write data.
- **Query/Serving Layer**: Authentication for API access to ensure data security.
```
