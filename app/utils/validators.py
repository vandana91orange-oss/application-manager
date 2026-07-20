import pandas as pd
import re


class DataCleaner:

    @staticmethod
    def clean(value):

        if pd.isna(value):
            return None

        if isinstance(value, str):

            value = value.strip()

            if value == "":
                return None

            if value.upper() == "N/A":
                return None

            if value == "-":
                return None

        return value
    
    @staticmethod
    def clean_dataframe(df):

        return df.map(DataCleaner.clean)


EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

def extract_emails(text: str) -> list[str]:
    if not text:
        return []

    return re.findall(EMAIL_REGEX, text)