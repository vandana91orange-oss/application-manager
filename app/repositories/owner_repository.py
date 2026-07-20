from typing import List, Optional

from app.models.users import User
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.application_owner import ApplicationOwner


class OwnerRepository:

    def __init__(self, db: Session):

        self.db = db

    # ----------------------------------
    # Create Owner
    # ----------------------------------
    def create(self, application_id: int, data: dict):

        user = self.db.query(User).filter(
            User.email == data["owner_email"]
        ).first()

        owner = ApplicationOwner(
            application_id=application_id,
            owner_type=data.get("owner_type"),
            owner_name=(
                f"{user.first_name} {user.last_name}"
                if user
                else data.get("owner_name")
            ),
            owner_email=(
                user.email
                if user
                else data.get("owner_email")
            )
        )

        self.db.add(owner)
        self.db.flush()

        return owner

    # ----------------------------------
    # Get by ID
    # ----------------------------------
    def get_by_id(
        self,
        owner_id: int
    ) -> Optional[ApplicationOwner]:

        return (

            self.db.query(ApplicationOwner)

            .filter(

                ApplicationOwner.id == owner_id

            )

            .first()

        )

    # ----------------------------------
    # Get all owners for an application
    # ----------------------------------
    def get_by_application(
        self,
        application_id: int
    ) -> List[ApplicationOwner]:

        return (

            self.db.query(ApplicationOwner)

            .filter(

                ApplicationOwner.application_id == application_id

            )

            .all()

        )

    # ----------------------------------
    # Get owner by type
    # ----------------------------------
    def get_owner(
        self,
        application_id: int,
        owner_type: str
    ) -> Optional[ApplicationOwner]:

        return (

            self.db.query(ApplicationOwner)

            .filter(

                ApplicationOwner.application_id == application_id,

                ApplicationOwner.owner_type == owner_type

            )

            .first()

        )

    # ----------------------------------
    # Update Owner
    # ----------------------------------
    def update(
        self,
        owner: ApplicationOwner,
        owner_name: str,
        owner_email: Optional[str] = None
    ) -> ApplicationOwner:

        try:

            owner.owner_name = owner_name

            owner.owner_email = owner_email

            self.db.flush()

            return owner

        except SQLAlchemyError:

            self.db.rollback()

            raise

    # ----------------------------------
    # Create or Update
    # ----------------------------------

    def create_or_update(
        self,
        application_id,
        owner_type,
        owner_name,
        owner_email
    ):

        owner = (
            self.db.query(ApplicationOwner)
            .filter(
                ApplicationOwner.application_id == application_id,
                ApplicationOwner.owner_type == owner_type
            )
            .first()
        )

        if owner:

            owner.owner_name = owner_name
            owner.owner_email = owner_email

        else:

            owner = ApplicationOwner(

                application_id=application_id,

                owner_type=owner_type,

                owner_name=owner_name,

                owner_email=owner_email

            )

            self.db.add(owner)

        return owner
    # ----------------------------------
    # Delete Owner
    # ----------------------------------
    def delete(
        self,
        owner_id: int
    ) -> bool:

        owner = self.get_by_id(owner_id)

        if not owner:

            return False

        try:

            self.db.delete(owner)

            self.db.flush()

            return True

        except SQLAlchemyError:

            self.db.rollback()

            raise

    # ----------------------------------
    # Delete all owners of an application
    # ----------------------------------
    def delete_by_application(
        self,
        application_id: int
    ) -> None:

        try:

            (

                self.db.query(ApplicationOwner)

                .filter(

                    ApplicationOwner.application_id == application_id

                )

                .delete()

            )

            self.db.flush()

        except SQLAlchemyError:

            self.db.rollback()

            raise
    
    def replace_all(self, application_id: int, owners: list):
        self.db.query(ApplicationOwner).filter(
            ApplicationOwner.application_id == application_id
        ).delete()

        for owner in owners:
            if hasattr(owner, "model_dump"):
                owner = owner.model_dump()

            self.create(application_id, owner)

        self.db.flush()