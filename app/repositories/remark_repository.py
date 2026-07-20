from typing import List, Optional

from app.utils.converters import to_bool
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.application_remark import ApplicationRemark

class RemarkRepository:

    def __init__(self, db: Session):

        self.db = db

    # ----------------------------------
    # Create Owner
    # ----------------------------------
    def create(
        self,
        application_id: int,
        data: dict
    ) -> ApplicationRemark:

        try:
            converted = to_bool(data.get(
                    "out_of_scope"
                ))

            remark = ApplicationRemark(

                application_id=application_id,

                remark=data.get(
                    "remark"
                ),

                remarks_imp=data.get(
                    "remarks_imp"
                ),

                source_comments=data.get(
                    "source_comments"
                ),

                archived_remarks=data.get(
                    "archived_remarks"
                ),

                out_of_scope=converted

            )

            self.db.add(remark)

            self.db.flush()

            return remark

        except SQLAlchemyError:

            self.db.rollback()

            raise

    # ----------------------------------
    # Get by ID
    # ----------------------------------
    def get_by_id(
        self,
        remark_id: int
    ) -> Optional[ApplicationRemark]:

        return (

            self.db.query(ApplicationRemark)

            .filter(

                ApplicationRemark.id == remark_id

            )

            .first()

        )

    # ----------------------------------
    # Get all owners for an application
    # ----------------------------------
    def get_by_application(
        self,
        application_id: int
    ) -> List[ApplicationRemark]:

        return (

            self.db.query(ApplicationRemark)

            .filter(

                ApplicationRemark.application_id == application_id

            )

            .all()

        )

    # ----------------------------------
    # Update Owner
    # ----------------------------------
    def update(
        self,
        remark: ApplicationRemark,
        data: dict
    ) -> ApplicationRemark:

        try:
            convert = to_bool(data.get(
                "out_of_scope"
            ))
            remark.remark = data.get(
                "remark"
            )

            remark.remarks_imp = data.get(
                "remarks_imp"
            )

            remark.source_comments = data.get(
                "source_comments"
            )

            remark.archived_remarks = data.get(
                "archived_remarks"
            )

            remark.out_of_scope = convert

            self.db.flush()

            return remark

        except SQLAlchemyError:

            self.db.rollback()

            raise

    # ----------------------------------
    # Create or Update
    # ----------------------------------

    def create_or_update(
        self,
        application_id: int,
        data: dict
    ):

        remark = (
            self.db.query(ApplicationRemark)
            .filter(
                ApplicationRemark.application_id == application_id
            )
            .first()
        )

        if not remark:

            remark = ApplicationRemark(
                application_id=application_id
            )

            self.db.add(remark)

        for key, value in data.items():
                setattr(remark, key, value)
        return remark


    # ----------------------------------
    # Delete Owner
    # ----------------------------------
    def delete(
        self,
        remark_id: int
    ) -> bool:

        remark = self.get_by_id(remark_id)

        if not remark:

            return False

        try:

            self.db.delete(remark)

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

                self.db.query(ApplicationRemark)

                .filter(

                    ApplicationRemark.application_id == application_id

                )

                .delete()

            )

            self.db.flush()

        except SQLAlchemyError:

            self.db.rollback()

            raise
