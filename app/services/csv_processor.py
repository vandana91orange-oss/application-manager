import logging
from pathlib import Path

import pandas as pd
from app.utils.csv_header_detector import CSVHeaderDetector
from sqlalchemy.orm import Session
from app.constants.column_mapping import CLOUD_SHEET_MAPPING, COLUMN_MAPPING
from app.services.row_processor import RowProcessor
from app.schemas.document_upload import UploadStatus


logger = logging.getLogger(__name__)


class CSVProcessor:

    def __init__(
        self,
        db: Session
    ):

        self.db = db
        self.row_processor = RowProcessor(db)


    def process_file(
        self,
        file_path: str,
        uploaded_file_id: int
    ):

        extension = Path(file_path).suffix.lower()

        dataframes = []

        # ----------------------------
        # CSV
        # ----------------------------
        if extension == ".csv":

            header = CSVHeaderDetector.detect(file_path)

            df = pd.read_csv(
                file_path,
                header=header,
                dtype=str
            )

            dataframes.append(
                (
                    None,   # CSV has no sheet/cloud
                    df
                )
            )

        # ----------------------------
        # Excel
        # ----------------------------
        elif extension in [".xlsx", ".xls"]:

            with pd.ExcelFile(file_path) as excel:


                for sheet_name in excel.sheet_names:

                    raw_df = pd.read_excel(
                        file_path,
                        sheet_name=sheet_name,
                        header=None,
                        dtype=str
                    )

                    try:

                        header = CSVHeaderDetector.detect_dataframe(raw_df)

                    except Exception:

                        logger.warning(
                            f"Skipping sheet '{sheet_name}'. Header not found."
                        )

                        continue

                    df = pd.read_excel(
                        file_path,
                        sheet_name=sheet_name,
                        header=header,
                        dtype=str
                    )

                    dataframes.append(
                        (
                            sheet_name,
                            df
                        )
                    )

        else:

            raise ValueError(
                "Unsupported file format."
            )

        # --------------------------------------------------
        # Process all sheets
        # --------------------------------------------------

        total_rows = 0
        processed_rows = 0
        failed_rows = []

        for sheet_name, df in dataframes:

            # Normalize columns
            df.columns = (
                df.columns
                .astype(str)
                .str.strip()
            )

            df.rename(
                columns=COLUMN_MAPPING,
                inplace=True
            )

            df = df.fillna("")

            total_rows += len(df)

            logger.info(
                f"Processing sheet: {sheet_name or 'CSV'} ({len(df)} rows)"
            )
            if sheet_name:
                normalized = CLOUD_SHEET_MAPPING.get(
                    sheet_name.strip().lower(),
                    sheet_name.strip()
                )
            else:
                normalized = ''
            for index, row in df.iterrows():

                try:

                    self.row_processor.process(
                        row=row.to_dict(),
                        uploaded_file_id=uploaded_file_id,
                        cloud_name=normalized
                    )

                    processed_rows += 1

                except Exception as ex:

                    logger.exception(ex)

                    failed_rows.append(
                        {
                            "sheet": sheet_name or "CSV",
                            "row": index + header + 2 if extension != ".csv" else index + header + 2,
                            "carto_id": row.get("carto_id"),
                            "application": row.get("application_name"),
                            "error": str(ex)
                        }
                    )

        return {

            "total_rows": total_rows,

            "processed": processed_rows,

            "failed": len(failed_rows),

            "errors": failed_rows,

            "status": (
                UploadStatus.COMPLETED
                if processed_rows == total_rows
                else UploadStatus.PARTIAL_SUCCESS
                if processed_rows > 0
                else UploadStatus.FAILED
            )

        }

