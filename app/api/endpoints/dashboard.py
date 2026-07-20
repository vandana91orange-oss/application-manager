from app.repositories.dashboard_repository import DashboardRepository
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth import UserRole, require_roles
from fastapi import APIRouter, Depends



def get_dashboard_service(
    db: Session = Depends(get_db),
) -> DashboardService:
    return DashboardService(DashboardRepository(db))

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get(
    "/dashboard",
    response_model=DashboardResponse
)
def dashboard(
    service: DashboardService = Depends(get_dashboard_service),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    )
):
    return service.dashboard()
