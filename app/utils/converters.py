from app.utils.header_mapper import HEADER_MAPPING
from datetime import datetime
import pandas as pd

class HeaderNormalizer:

    @staticmethod
    def normalize(df):

        columns = {}

        for column in df.columns:

            column = column.strip()

            if column in HEADER_MAPPING:

                columns[column] = HEADER_MAPPING[column]

            else:

                columns[column] = (
                    column
                    .strip()
                    .lower()
                    .replace(" ", "_")
                )

        return df.rename(columns=columns)


class DateConverter:

    @staticmethod
    def convert(value):

        if value is None or value == "":
            return None

        if isinstance(value, datetime):
            return value

        if isinstance(value, pd.Timestamp):
            return value.to_pydatetime()

        formats = [
            "%d-%b-%y",             # 26-Apr-26
            "%b-%y",                # Apr-26
            "%d/%m/%Y",             # 26/04/2026
            "%Y-%m-%d",             # 2026-04-26
            "%Y-%m-%d %H:%M:%S",    # 2026-04-26 00:00:00
        ]

        value = str(value).strip()

        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        return None


class PercentageConverter:

    @staticmethod
    def convert(value):

        if value is None:
            return 0

        if isinstance(value, str):
            value = value.replace("%", "").strip()

        try:
            return int(float(value))
        except (TypeError, ValueError):
            return 0


class BooleanConverter:

    TRUE_VALUES = {
        "yes",
        "y",
        "true",
        "1",
        "completed",
        "done",
        "active"
    }

    FALSE_VALUES = {
        "no",
        "n",
        "false",
        "0",
        "pending",
        "inactive"
    }

    @staticmethod
    def convert(value):

        if value is None:
            return None

        if isinstance(value, bool):
            return value

        value = str(value).strip().lower()

        if value in BooleanConverter.TRUE_VALUES:
            return True

        if value in BooleanConverter.FALSE_VALUES:
            return False

        return None


class IntegerConverter:

    @staticmethod
    def convert(value):

        if value is None:
            return None

        try:
            return int(float(value))
        except (TypeError, ValueError):
            return None


class StringConverter:

    @staticmethod
    def convert(value):

        if value is None:
            return None

        value = str(value).strip()

        return value if value else None


def to_bool(value):
    if value is None:
        return None

    if isinstance(value, bool):
        return value

    value = str(value).strip().lower()

    if value in ("1", "true", "yes", "y"):
        return True

    if value in ("0", "false", "no", "n"):
        return False

    return None