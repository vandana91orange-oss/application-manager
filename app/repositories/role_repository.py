from sqlalchemy.orm import Session

from app.models.roles import Role
from app.schemas.role import RoleCreate, RoleUpdate


class RoleRepository:

    def __init__(self, db: Session):
        self.db = db


    def create(
        self,
        role: RoleCreate
    ):

        db_role = Role(
            name=role.name,
            description=role.description
        )

        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)

        return db_role


    def get_all(self):

        return (
            self.db.query(Role)
            .all()
        )


    def get_by_id(
        self,
        role_id: int
    ):

        return (
            self.db.query(Role)
            .filter(Role.id == role_id)
            .first()
        )


    def get_by_name(
        self,
        name: str
    ):

        return (
            self.db.query(Role)
            .filter(Role.name == name)
            .first()
        )


    def update(
        self,
        role_id: int,
        data: RoleUpdate
    ):

        role = self.get_by_id(role_id)

        if not role:
            return None


        if data.name:
            role.name = data.name

        if data.description is not None:
            role.description = data.description


        self.db.commit()
        self.db.refresh(role)

        return role


    def delete(
        self,
        role_id: int
    ):

        role = self.get_by_id(role_id)

        if not role:
            return None


        self.db.delete(role)
        self.db.commit()

        return role
