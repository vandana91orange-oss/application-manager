import pandas as pd


class CSVReader:

    @staticmethod
    def read(file_path: str):

        if file_path.endswith(".csv"):

            df = pd.read_csv(file_path)

        elif file_path.endswith(".xlsx"):

            df = pd.read_excel(file_path)

        elif file_path.endswith(".xls"):

            df = pd.read_excel(file_path)

        else:

            raise Exception("Unsupported file type")

        return df