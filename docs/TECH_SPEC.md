# TECH_SPEC.md – Global PayFlow

---

## 1. Overview

**Global PayFlow** is a cloud‑native payment infrastructure platform designed to accelerate cross‑border transactions, reduce processing costs, and provide real‑time settlement visibility. It exposes a set of REST/GraphQL APIs that integrate with merchants, banks, and payment processors. The system is built for high availability, low latency, and compliance with global regulatory standards (PCI‑DSS, PSD2, GDPR).

---

## 2. Architecture

```
┌───────────────────────┐
│  Client / Merchant UI │
└────────────┬──────────┘
             │
             ▼
┌───────────────────────┐
│  API Gateway (NGINX)  │
└────────────┬──────────┘
             ▼
┌───────────────────────┐
│  Auth Service (OAuth2) │
└────────────┬──────────┘
             ▼
┌───────────────────────┐
│  Core Services        │
│  ┌─────────────────┐ │
│  │  Payment Engine │ │
│  ├─────────────────┤ │
│  │  Settlement     │ │
│  ├─────────────────┤ │
│  │  Risk & Fraud   │ │
│  └─────────────────┘ │
└────────────┬──────────┘
             ▼
┌───────────────────────┐
│  Event Bus (Kafka)    │
└────────────┬──────────┘
             ▼
┌───────────────────────┐
│  Data Store Layer     │
│  ┌─────────────────┐ │
│  │  PostgreSQL     │ │
│  ├─────────────────┤ │
│  │  Redis (Cache)  │ │
│  └─────────────────┘ │
└────────────┬──────────┘
             ▼
┌───────────────────────┐
│  External Integrations│
│  ├─ Banks (ISO20022)  │
│  ├─ Card Networks     │
│  └─ AML / KYC APIs    │
└───────────────────────┘
```

* **API Gateway**: TLS termination, rate limiting, request routing.  
* **Auth Service**: OAuth2 + OpenID Connect, JWT issuance.  
* **Core Services**: Stateless micro‑services, containerized, orchestrated by Kubernetes.  
* **Event Bus**: Kafka topics for asynchronous workflows (e.g., settlement, fraud alerts).  
* **Data Store**: PostgreSQL for ACID guarantees; Redis for session & cache.  
* **External Integrations**: ISO20022 over SWIFT, REST for card networks, SOAP for legacy banks.

---

## 3. Components & Responsibilities

| Service | Language | Key Libraries | Responsibility |
|---------|----------|---------------|----------------|
| **Auth Service** | Go | `golang.org/x/oauth2`, `github.com/dgrijalva/jwt-go` | Token issuance, user & merchant auth |
| **Payment Engine** | Java (Spring Boot) | `spring-boot-starter-web`, `spring-boot-starter-data-jpa` | Transaction orchestration, routing |
| **Settlement Service** | Rust | `actix-web`, `sqlx` | Batch settlement, ISO20022 message creation |
| **Risk & Fraud** | Python | `fastapi`, `pandas`, `scikit-learn` | ML‑based fraud detection, rule engine |
| **API Gateway** | NGINX | `nginx`, `lua-resty-openidc` | TLS, auth, routing |
| **Event Bus** | Kafka | `confluent-kafka-go` | Pub/Sub for async events |
| **Database** | PostgreSQL | `pgx` | Persistent storage |
| **Cache** | Redis | `go-redis` | Session, rate‑limit cache |

---

## 4. Data Model

### 4.1 Core Tables

| Table | Columns | Notes |
|-------|---------|-------|
| `merchants` | `id (PK)`, `name`, `country`, `status`, `created_at` | Merchant onboarding |
| `users` | `id`, `merchant_id (FK)`, `email`, `hashed_pw`, `role` | Merchant staff |
| `transactions` | `id`, `merchant_id`, `amount`, `currency`, `status`, `created_at`, `updated_at` | Core transaction record |
| `settlements` | `id`, `transaction_id (FK)`, `settlement_id`, `status`, `settlement_date` | Settlement metadata |
| `fraud_events` | `id`, `transaction_id`, `score`, `reason`, `created_at` | Fraud detection results |
| `audit_logs` | `id`, `entity`, `entity_id`, `action`, `performed_by`, `timestamp` | Immutable audit trail |

### 4.2 Schemas

* All timestamps in UTC ISO‑8601.  
* Monetary amounts stored as `numeric(19,4)` to avoid rounding errors.  
* Status enums: `PENDING`, `COMPLETED`, `FAILED`, `REFUNDED`, `SETTLED`, `PENDING_SETTLEMENT`, `FRAUD`.

---

## 5. Key APIs / Interfaces

| Endpoint | Method | Path | Description | Auth |
|----------|--------|------|-------------|------|
| **Merchant Registration** | POST | `/api/v1/merchants` | Create merchant profile | None |
| **Login** | POST | `/api/v1/auth/login` | OAuth2 password grant | None |
| **Create Transaction** | POST | `/api/v1/transactions` | Initiate payment | Bearer |
| **Transaction Status** | GET | `/api/v1/transactions/{id}` | Retrieve status | Bearer |
| **Settlement Request** | POST | `/api/v1/settlements` | Trigger settlement | Bearer |
| **Fraud Check** | POST | `/api/v1/fraud/check` | Real‑time fraud scoring | Bearer |
| **Webhook** | POST | `/api/v1/webhooks/settlement` | Receive settlement callbacks | HMAC SHA256 |

*All endpoints return JSON with `status`, `data`, and `errors` fields.*

---

## 6. Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| **API Gateway** | NGINX | 1.27 |
| **Auth** | Go | 1.22 |
| **Payment Engine** | Java | 21 (Spring Boot 3.3) |
| **Settlement** | Rust | 1.75 |
| **Risk** | Python | 3.12 (FastAPI) |
| **Event Bus** | Kafka | 3.6 |
| **DB** | PostgreSQL | 16 |
| **Cache** | Redis | 7 |
| **Container Runtime** | Docker | 25 |
| **Orchestration** | Kubernetes | 1.30 |
| **CI/CD** | GitHub Actions | - |
| **Monitoring** | Prometheus + Grafana | - |
| **Tracing** | OpenTelemetry | - |

---

## 7. Dependencies

| Component | Dependency | Purpose |
|-----------|------------|---------|
| Auth Service | `github.com/dgrijalva/jwt-go` | JWT handling |
| Payment Engine | `spring-boot-starter-data-jpa` | ORM |
| Settlement | `actix-web` | Async web server |
| Risk | `scikit-learn` | ML models |
| Event Bus | `confluent-kafka-go` | Kafka client |
| DB | `pgx` | PostgreSQL driver |
| Cache | `go-redis` | Redis client |

All dependencies are pinned to specific versions in `go.mod`, `pom.xml`, `Cargo.toml`, and `requirements.txt`.

---

## 8. Deployment

### 8.1 Infrastructure

| Layer | Tool | Notes |
|-------|------|-------|
| **Provisioning** | Terraform | AWS EKS, RDS, ElastiCache |
| **CI/CD** | GitHub Actions | Build, test, push images |
| **Container Registry** | Amazon ECR | Docker images |
| **Orchestration** | Kubernetes | Helm charts |
| **Secrets** | AWS Secrets Manager | JWT keys, DB creds |
| **Observability** | Prometheus + Grafana | Metrics |
| **Tracing** | Jaeger | Distributed tracing |
| **Logging** | Loki | Centralized logs |

### 8.2 Helm Chart

* `global-payflow/helm/` contains sub‑charts for each micro‑service.  
* Values files (`values-prod.yaml`, `values-dev.yaml`) control replicas, resource limits, and environment variables.  
* Release name: `global-payflow-prod`.

### 8.3 CI Pipeline

1. **Lint**: `golangci-lint`, `mypy`, `flake8`, `shellcheck`.  
2. **Unit Tests**: `go test`, `pytest`, `mvn test`.  
3. **Integration Tests**: Docker Compose with Postgres & Kafka.  
4. **Build**: Docker build, push to ECR.  
5. **Deploy**: Helm upgrade with `--atomic`.  
6. **Smoke Test**: Run `curl` against `/healthz` endpoints.

### 8.4 Rollback Strategy

* Helm `--atomic` ensures rollback on failure.  
* Canary releases via `Istio` (optional).  
* Database migrations are idempotent; use `flyway` for schema changes.

---

## 9. Security & Compliance

* **PCI‑DSS**: All card data is tokenized; no PAN stored.  
* **GDPR**: Data residency per merchant country; right‑to‑be‑forgotten endpoint.  
* **OAuth2**: Refresh tokens stored encrypted.  
* **Transport**: TLS 1.3 everywhere.  
* **Secrets**: Rotated quarterly via Secrets Manager.  
* **Audit**: Immutable logs in PostgreSQL; export to SIEM.

---

## 10. Monitoring & Alerting

| Metric | Source | Alert |
|--------|--------|-------|
| Transaction latency | Prometheus | > 200ms |
| Failure rate | Prometheus | > 5% |
| Settlement queue depth | Kafka | > 10k |
| CPU / Memory | Node Exporter | > 80% |
| Auth failures | Auth Service | > 10/min |

Alerts sent to Slack (`#payflow-alerts`) and PagerDuty.

---

## 11. Future Enhancements

1. **Multi‑currency settlement** – support for local currency conversion.  
2. **GraphQL API** – flexible client queries.  
3. **Serverless functions** – for event‑driven fraud scoring.  
4. **AI‑driven routing** – dynamic path selection based on cost & speed.

---

## 12. Contact & Governance

| Role | Contact |
|------|---------|
| Product Owner | alice@axentx.com |
| Lead Architect | bob@axentx.com |
| DevOps Lead | carol@axentx.com |
| Security Officer | dave@axentx.com |

All changes must pass the **Code Review** and **Security Scan** gates before merging into `main`.

---
