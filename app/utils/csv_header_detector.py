import pandas as pd


class CSVHeaderDetector:

    REQUIRED_COLUMNS = [
        "Orange Carto ID",
        "Application Name",
    ]

    @staticmethod
    def detect(file_path: str) -> int:
        df = pd.read_excel(
            file_path,
            header=None,
            dtype=str
        )
        return CSVHeaderDetector.detect_dataframe(df)
    
    @staticmethod
    def detect_dataframe(df: pd.DataFrame) -> int:

        # Scan the first 20 rows for the header
        for i in range(min(20, len(df))):

            values = (
                df.iloc[i]
                .fillna("")
                .astype(str)
                .str.strip()
                .tolist()
            )

            if all(col in values for col in CSVHeaderDetector.REQUIRED_COLUMNS):
                return i

        raise ValueError("Header row not found.")

