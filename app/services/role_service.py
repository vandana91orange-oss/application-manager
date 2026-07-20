from app.repositories.role_repository import RoleRepository
from app.schemas.role import RoleCreate, RoleUpdate


class RoleService:

    def __init__(
        self,
        repository: RoleRepository
    ):
        self.repository = repository


    def create_role(
        self,
        role: RoleCreate
    ):

        existing = self.repository.get_by_name(
            role.name
        )

        if existing:
            raise Exception(
                "Role already exists"
            )

        return self.repository.create(role)


    def get_roles(self):

        return self.repository.get_all()


    def get_role(
        self,
        role_id: int
    ):

        return self.repository.get_by_id(role_id)


    def update_role(
        self,
        role_id: int,
        data: RoleUpdate
    ):

        return self.repository.update(
            role_id,
            data
        )


    def delete_role(
        self,
        role_id: int
    ):

        return self.repository.delete(role_id)
