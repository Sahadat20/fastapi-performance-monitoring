# FastAPI Metrics Monitoring System

## 📋 Project Overview
This project is a **production-ready FastAPI application** that implements detailed system-level and application-level metrics monitoring using Prometheus metrics format. It exposes a `/metrics` endpoint that Prometheus can scrape to monitor application and infrastructure health.

---

## 🎯 Objectives
- Collect and expose system metrics: CPU, memory, threads, GC, uptime.
- Track HTTP request volume and performance.
- Enable observability for debugging and infrastructure monitoring.
- Use Prometheus-compatible format and standards.

---


## ⚙️ Tech Stack

### Core Stack
- **FastAPI**: High-performance Python web framework
- **Python 3.11**
- **Uvicorn**: ASGI server

### Monitoring Stack
- **prometheus_client**: Python metrics library
- **Prometheus** (external): Scraping & visualization

### Supporting Libraries
- **psutil**: CPU, memory, and system usage
- **Starlette Middleware**: For custom HTTP monitoring
- **asyncio**: Background metric sampling

---

## 📁 Project Structure

```
fastapi-metrics-app/
├── app/
│   ├── main.py               # App entrypoint
│   ├── metrics/
│   │   ├── __init__.py
│   │   ├── metrics.py # CPU, memory, threads, uptime, GC, Request counters, durations
│   └── middleware/
│       └── metrics_middleware.py # HTTP metric tracking middleware
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🔌 Core Endpoints

| Endpoint      | Method | Description                      |
|---------------|--------|----------------------------------|
| `/`           | GET    | Root hello response              |
| `/health`     | GET    | App + DB health status           |
| `/metrics`    | GET    | Prometheus-formatted metrics     |
| `/data`       | GET    | Retrieve sample data             |
| `/data`       | POST   | Simulate a data operation        |

---

## 📊 Metrics Implemented

### 🔧 System Metrics
- `process_cpu_percentage` – % CPU used by process (custom)
- `process_cpu_seconds_total` – CPU seconds (default)
- `process_resident_memory_bytes` – Physical memory usage
- `process_virtual_memory_bytes` – Virtual memory used
- `process_start_time_seconds` – App start time
- `python_gc_objects_collected_total` – GC objects collected
- `python_threads` – Number of threads

### 🌐 HTTP Metrics
- `http_requests_total{method,route,status_code}` – Total requests
- `http_request_duration_seconds{method,route,status_code}` – Duration histogram
- 95th percentile latency (Grafana query example):
```promql
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

### 🗄️ Database Metrics
- `db_connections_active` – Active DB pool connections
- `db_query_duration_seconds` – DB query durations (if enabled)
- `db_operations_total` – Counter of DB ops by type

---

## 🐳 Deployment Instructions

### Prerequisites
- Docker + Docker Compose installed

### Checkout the Application Repository
- Clone the application repository here as well. It contains the necessary monitoring files:
```bash
git clone https://github.com/Sahadat20/fastapi-performance-monitoring.git
cd fastapi-performance-monitoring
```
### 🚀 Run with Docker
```bash
docker-compose up --d
```

### App URLs
- Metrics Endpoint: http://localhost:8000/metrics
- Health check Endpoint: http://localhost:8000/health
- Data Endpoint: http://localhost:8000/data
- Prometheus client Endpoint: http://localhost:9090


### Insert Data
```bash
    curl -X POST http://localhost:8000/data \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "email": "john@example.com"}'
```
### Get Data
```bash
    curl http://localhost:8000/data
```


## 📘 Documentation

- Prometheus metrics reference: https://prometheus.io/docs/concepts/metric_types/
- FastAPI docs: https://fastapi.tiangolo.com/
- Python Prometheus client: https://github.com/prometheus/client_python

---

## 🏁 Conclusion
This FastAPI Metrics Monitoring System provides a scalable, observable, and production-ready foundation for microservices or monoliths. By using Prometheus and exposing system and app metrics, you gain deep visibility into your application’s performance and health.

---