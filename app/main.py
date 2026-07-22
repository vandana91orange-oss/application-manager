from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.api.endpoints import users, roles, auth, upload_file, application_cloud, application, audit_logs, dashboard


# For development only.
# In production, use Alembic migrations instead of create_all().
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application started...")
    yield
    print("Application stopped...")


app = FastAPI(
    title="CSV Management API",
    description="REST APIs for CSV Upload, Authentication, RBAC, and PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(roles.router, prefix="/api/v1", tags=["Roles"])
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(application.router, prefix="/api/v1", tags=["Applications"])
app.include_router(upload_file.router, prefix="/api/v1", tags=["Uploads"])
app.include_router(application_cloud.router, prefix="/api/v1", tags=["Clouds"])
app.include_router(audit_logs.router, prefix="/api/v1", tags=["AuditLogs"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["Dashboard"])


@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "success",
        "message": "CSV Management API is running"
    }


@app.get("/ping", tags=["Health"])
def ping():
    return {
        "message": "pong"
    }
