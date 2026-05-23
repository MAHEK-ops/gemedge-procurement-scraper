from scraper.parser import GemParser
from parser.evaluation_parser import EvaluationParser

from utils.file_manager import FileManager
from utils.saver import DataSaver

from config import EVALUATIONS_DIR


listing_parser = GemParser()

listing_records = (
    listing_parser.parse_all_listing_pages()
)

evaluation_records=[]

files = FileManager.list_html_files(
    EVALUATIONS_DIR
)

for file in files:

    html = FileManager.load_html(
        file,
        EVALUATIONS_DIR
    )

    if html:

        records = EvaluationParser.parse(
            html
        )

        evaluation_records.extend(
            records
        )

print(
    "Listing records:",
    len(listing_records)
)

print(
    "Evaluation records:",
    len(evaluation_records)
)

final_data=[]

final_data.extend(
    listing_records
)

final_data.extend(
    evaluation_records
)

DataSaver.save(
    final_data
)

print()

print(
    "Final records:",
    len(final_data)
)