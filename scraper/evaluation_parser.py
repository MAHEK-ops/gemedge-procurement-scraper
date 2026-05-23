"""
Parses saved evaluation pages
"""

from bs4 import BeautifulSoup

from utils.logger import setup_logger
from utils.file_manager import FileManager

from config import EVALUATIONS_DIR

logger = setup_logger()


class EvaluationParser:

    def __init__(self):

        self.logger = logger


    def parse_all_evaluations(self):

        all_records=[]

        files=FileManager.list_html_files(
            EVALUATIONS_DIR
        )

        self.logger.info(
            f"Found {len(files)} evaluation files"
        )

        for file in files:

            html=FileManager.load_html(
                file,
                EVALUATIONS_DIR
            )

            if html:

                records=self.parse_page(
                    html,
                    file
                )

                all_records.extend(
                    records
                )

        return all_records


    def parse_page(
        self,
        html,
        filename
    ):

        records=[]

        soup=BeautifulSoup(
            html,
            "html.parser"
        )


        technical_section=soup.select(
            "#collapseTwo tbody tr"
        )


        self.logger.info(
            f"{filename}: "
            f"{len(technical_section)} sellers"
        )


        for seller in technical_section:

            try:

                cols=seller.find_all(
                    "td"
                )

                if len(cols)<5:
                    continue


                record={}

                record["file"]=filename

                seller = cols[1].select_one(".cid")

                if seller:

                    record["seller_name"] = (
                        seller.text.strip()
                    )

                else:

                    record["seller_name"] = (
                        cols[1]
                        .get_text(
                            " ",
                            strip=True
                        )
                    )

                record["participated_on"]=(
                    cols[3]
                    .get_text(
                        strip=True
                    )
                )

                record["status"]=(
                    cols[-1]
                    .get_text(
                        strip=True
                    )
                )

                records.append(
                    record
                )

            except Exception as e:

                self.logger.error(
                    f"Parse error: {e}"
                )

        return records