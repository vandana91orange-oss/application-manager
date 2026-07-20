from sqlalchemy.orm import Session

from app.models.roles import Role


DEFAULT_ROLES = [
    {
        "name": "Admin",
        "description": "Full access to all system features"
    },
    {
        "name": "Manager",
        "description": "Can manage CSV uploads and view data"
    },
    {
        "name": "Employee",
        "description": "Can view assigned data"
    },
    {
        "name": "Viewer",
        "description": "Read-only access"
    }
]


def seed_roles(db: Session):
    """
    Insert default roles if they do not exist.
    """

    for role_data in DEFAULT_ROLES:

        existing_role = (
            db.query(Role)
            .filter(Role.name == role_data["name"])
            .first()
        )

        if not existing_role:
            role = Role(
                name=role_data["name"],
                description=role_data["description"]
            )

            db.add(role)

    db.commit()

    print("Roles seeded successfully.")