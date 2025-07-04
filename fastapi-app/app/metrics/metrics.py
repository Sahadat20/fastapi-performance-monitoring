# app/metrics.py

import time
import threading
import psutil
import os
from prometheus_client import (
    Gauge, Counter, Histogram, generate_latest,
    CONTENT_TYPE_LATEST, CollectorRegistry,
    ProcessCollector, PlatformCollector, GCCollector
)
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import SessionLocal

registry = CollectorRegistry()

# Register default collectors
ProcessCollector(registry=registry)
PlatformCollector(registry=registry)
GCCollector(registry=registry)

# CPU usage gauge (sampled every 5s)
cpu_percent_gauge = Gauge(
    'process_cpu_percentage',
    'CPU usage percentage of this Python process (sampled every 5s)',
    registry=registry
)

# HTTP metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'route', 'status_code'],
    registry=registry
)

http_request_duration = Histogram(
    'http_request_duration_seconds',
    'Duration of HTTP requests in seconds',
    ['method', 'route', 'status_code'],
    buckets=[0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10],
    registry=registry
)

# DB metrics
db_connections_active = Gauge(
    'db_connections_active',
    'Number of active database connections',
    registry=registry
)

db_query_duration = Histogram(
    'db_query_duration_seconds',
    'Duration of database queries in seconds',
    ['operation'],
    buckets=[0.01, 0.05, 0.1, 0.3, 0.5, 1, 2, 5],
    registry=registry
)

db_operations_total = Counter(
    'db_operations_total',
    'Total number of database operations',
    ['operation', 'status'],
    registry=registry
)

# CPU usage sampling (every 5s)
def cpu_usage_sampler():
    num_cores = psutil.cpu_count()
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_percent_gauge.set(cpu_percent)
        time.sleep(4)  # total interval = 5s

threading.Thread(target=cpu_usage_sampler, daemon=True).start()

# DB connection check every 5s
def db_connection_sampler():
    from app.database import engine
    while True:
        if engine.pool:
            db_connections_active.set(engine.pool.checkedin() + engine.pool.checkedout())
        time.sleep(5)

threading.Thread(target=db_connection_sampler, daemon=True).start()

# Metrics endpoint


def metrics_endpoint():
    return generate_latest(registry), CONTENT_TYPE_LATEST


