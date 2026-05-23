import re
import pandas as pd


class DataCleaner:

    @staticmethod
    def normalize_vendor_names(df):

        if "seller_name" not in df.columns:
            return df

        df["seller_name"] = (
            df["seller_name"]
            .fillna("")
            .str.upper()
            .str.replace("UNDER PMA","",regex=False)
            .str.replace("M/S","",regex=False)
            .str.replace(r"\(.*?\)","",regex=True)
            .str.strip()
        )

        return df


    @staticmethod
    def remove_duplicates(df):

        return df.drop_duplicates()


    @staticmethod
    def handle_missing_values(df):

        return df.fillna("N/A")


    @staticmethod
    def process(df):

        df=DataCleaner.handle_missing_values(df)

        df=DataCleaner.normalize_vendor_names(df)

        df=DataCleaner.remove_duplicates(df)

        return df