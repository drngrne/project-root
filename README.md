# Backend Developer Assessment

## Project Overview
This project has a Dockerized backend data pipeline consisting of three services:

- **Flask Mock Server (Port 5000)**  
  Serves paginated customer data from a local JSON file.

- **FastAPI Pipeline Service (Port 8000)**  
  Fetches (ingests) data from the mock server and stores it in PostgreSQL.

- **PostgreSQL (Port 5432)**  
  Persists customer data.

---

## Prerequisites
Make sure you have the following installed:

- Docker Desktop
- Docker Compose
- Python 3.10+
- Git

---

## Project Structure
```
project-root/
│
├── docker-compose.yml
│
├── mock-server/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── data/
│       └── customers.json
│
├── pipeline-service/
│   ├── main.py
│   ├── database.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── models/
│   │   └── customer.py
│   └── services/
│       └── ingestion.py
│
└── README.md
```

---

## How to Run

### 1. Clone the Repository
```
git clone https://github.com/drngrne/project-root.git
cd project-root
```

### 2. Start Services
```
docker-compose up -d
```

### 3. Verify Containers
```
docker ps
```

---

## API Endpoints

### Flask Mock Server (Port 5000)

| Method | Endpoint | Description |
|--------|---------|------------|
| GET | /api/health | Health check |
| GET | /api/customers | Paginated customer data |
| GET | /api/customers/{id} | Get customer by ID |

#### Example Response
```
{
  "data": [...],
  "total": 20,
  "page": 1,
  "limit": 10
}
```

---

### FastAPI Pipeline Service (Port 8000)

| Method | Endpoint | Description |
|--------|---------|------------|
| POST | /api/ingest | Ingest data from mock server |
| GET | /api/customers | Fetch customers from DB |
| GET | /api/customers/{id} | Get customer by ID |

#### Example Response (Ingestion)
```
{
  "status": "success",
  "records_processed": 20
}
```

---

## Testing the Pipeline

Run the following commands:

```
curl "http://localhost:5000/api/customers?page=1&limit=5"

curl -X POST http://localhost:8000/api/ingest

curl "http://localhost:8000/api/customers?page=1&limit=5"
```

---

## Architecture Diagram
```
        ┌──────────────────────┐
        │   Flask Mock Server  │
        │   (Port 5000)        │
        └──────────┬───────────┘
                   │ HTTP API
                   ▼
        ┌──────────────────────┐
        │ FastAPI Pipeline     │
        │ (Port 8000)          │
        └──────────┬───────────┘
                   │ SQLAlchemy
                   ▼
        ┌──────────────────────┐
        │     PostgreSQL       │
        │     (Port 5432)      │
        └──────────────────────┘
```