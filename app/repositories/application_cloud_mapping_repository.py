from sqlalchemy.orm import Session

from app.models.application_cloud_mapping import ApplicationCloudMapping


class ApplicationCloudMappingRepository:

    def __init__(self, db: Session):

        self.db = db

    def get(
        self,
        application_id: int,
        cloud_id: int
    ):

        return (
            self.db.query(ApplicationCloudMapping)
            .filter(
                ApplicationCloudMapping.application_id == application_id,
                ApplicationCloudMapping.cloud_id == cloud_id
            )
            .first()
        )

    def create(
        self,
        application_id: int,
        cloud_id: int
    ):

        mapping = ApplicationCloudMapping(
            application_id=application_id,
            cloud_id=cloud_id
        )

        self.db.add(mapping)

        self.db.flush()

        return mapping

    def create_or_update(
        self,
        application_id: int,
        cloud_id: int
    ):

        mapping = self.get(
            application_id,
            cloud_id
        )

        if mapping:

            return mapping

        return self.create(
            application_id,
            cloud_id
        )

    def replace_all(self, application_id: int, cloud_ids: list[int]):
        self.db.query(ApplicationCloudMapping).filter(
            ApplicationCloudMapping.application_id == application_id
        ).delete()

        for cloud_id in cloud_ids:
            mapping = ApplicationCloudMapping(
                application_id=application_id,
                cloud_id=cloud_id
            )
            self.db.add(mapping)

        self.db.flush()
