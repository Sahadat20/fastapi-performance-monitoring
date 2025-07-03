import time
import psutil
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import Depends
from .database import SessionLocal

start_time = time.time()

def get_uptime():
    return time.time() - start_time

def get_memory_usage():
    return dict(psutil.virtual_memory()._asdict())

def get_health_status(db: Session):
    try:
        result = db.execute(text("SELECT NOW()"))
        db_time = result.scalar()
        return {
            "status": "healthy",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "database": "connected",
            "uptime": get_uptime(),
            "memory": get_memory_usage(),
            "db_time": db_time.isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "error": str(e)
        }
