"""
Saves final procurement data
"""

import json
import pandas as pd

from utils.logger import setup_logger
from config import CSV_FILE, JSON_FILE

logger = setup_logger()


class DataSaver:

    @staticmethod
    def save(records):

        if not records:

            logger.warning(
                "No records to save"
            )

            return

        # Convert to DataFrame
        df = pd.DataFrame(records)

        # Save CSV
        df.to_csv(
            CSV_FILE,
            index=False
        )

        logger.info(
            f"CSV saved: {CSV_FILE}"
        )

        # Save JSON
        with open(
            JSON_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                records,
                f,
                indent=4,
                ensure_ascii=False
            )

        logger.info(
            f"JSON saved: {JSON_FILE}"
        )