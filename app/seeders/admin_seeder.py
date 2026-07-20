from sqlalchemy.orm import Session

from app.config import settings
from app.models.users import User
from app.models.roles import Role
from app.security.password import hash_password


def seed_admin_user(db: Session):
    """
    Create default admin user.
    """

    # Check existing admin user
    existing_user = (
        db.query(User)
        .filter(
            User.email == settings.ADMIN_EMAIL
        )
        .first()
    )

    if existing_user:
        return


    # Find Admin role
    admin_role = (
        db.query(Role)
        .filter(Role.name == "Admin")
        .first()
    )


    if not admin_role:
        raise Exception(
            "Admin role not found. Run role seeder first."
        )


    admin_user = User(
        first_name=settings.ADMIN_FIRST_NAME,
        last_name=settings.ADMIN_LAST_NAME,
        email=settings.ADMIN_EMAIL,
        hashed_password=hash_password(
            settings.ADMIN_PASSWORD
        ),
        is_active=True,
        role_id=admin_role.id
    )


    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
