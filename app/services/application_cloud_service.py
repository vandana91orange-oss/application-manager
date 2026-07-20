from fastapi import HTTPException

from app.repositories.application_cloud_repository import (
    ApplicationCloudRepository
)


class ApplicationCloudService:

    def __init__(
        self,
        repository: ApplicationCloudRepository
    ):
        self.repository = repository

    # -----------------------------
    # Create
    # -----------------------------

    def create(
        self,
        name: str
    ):

        existing = self.repository.get_by_cloud_name(name.strip())

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Cloud already exists."
            )

        cloud = self.repository.create(
            name.strip()
        )

        self.repository.db.commit()

        self.repository.db.refresh(cloud)

        return cloud

    # -----------------------------
    # Get All
    # -----------------------------

    def get_all(self):

        return self.repository.get_all_cloud()
    # -----------------------------
    # Get By Id
    # -----------------------------

    def get_by_id(
        self,
        id: int
    ):

        cloud = self.repository.get_by_id(id)

        if not cloud:
            raise HTTPException(
                status_code=404,
                detail="Cloud not found."
            )

        return cloud

    # -----------------------------
    # Update
    # -----------------------------

    def update(
        self,
        id: int,
        name: str
    ):

        cloud = self.repository.get_by_id(id)

        if not cloud:
            raise HTTPException(
                status_code=404,
                detail="Cloud not found."
            )

        cloud = self.repository.update(
            cloud,
            name.strip()
        )

        self.repository.db.commit()

        self.repository.db.refresh(cloud)

        return cloud

    # -----------------------------
    # Delete
    # -----------------------------

    def delete(
        self,
        id: int
    ):

        success = self.repository.delete(id)

        if not success:
            raise HTTPException(
                status_code=404,
                detail="Cloud not found."
            )

        self.repository.db.commit()

        return {
            "message": "Cloud deleted successfully."
        }

    