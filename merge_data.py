from scraper.parser import Parser
from scraper.evaluation_parser import EvaluationParser
from utils.file_manager import FileManager
from config import EVALUATIONS_DIR

listing_records = Parser.parse_all()

evaluation_records = []

files = FileManager.list_html_files(
    EVALUATIONS_DIR
)

for file in files:

    html = FileManager.load_html(
        file,
        EVALUATIONS_DIR
    )

    data = EvaluationParser.parse(
        html
    )

    # extract bid_id from filename
    # GEM_2026_B_7527569.html
    bid_id = (
        file
        .replace(".html","")
        .replace("_","/")
    )

    for row in data:

        row["bid_id"] = bid_id

        evaluation_records.append(
            row
        )

print(
    "Listing records:",
    len(listing_records)
)

print(
    "Evaluation records:",
    len(evaluation_records)
)