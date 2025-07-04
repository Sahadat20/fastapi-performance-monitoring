from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from fastapi import Response
from app.metrics.metrics import metrics_endpoint
from app.middleware.metrics_middleware import MetricsMiddleware
from .health import get_health_status

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register Prometheus middleware
app.add_middleware(MetricsMiddleware)

# ✅ Root Endpoint
@app.get("/", response_model=schemas.RootMessage, tags=["Root"])
def root():
    return {"message": "Welcome to the FastAPI Metrics Monitoring System!"}

@app.post("/data", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/data", response_model=list[schemas.UserOut])
def read_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)
@app.get("/metrics")
def get_metrics():
    data, content_type = metrics_endpoint()
    return Response(content=data, media_type=content_type)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return get_health_status(db)