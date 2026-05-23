from utils.file_manager import FileManager
from config import EVALUATIONS_DIR

files = FileManager.list_html_files(
    EVALUATIONS_DIR
)

keywords = [
    "L1",
    "Financial Evaluation",
    "Quoted Value",
    "Price",
    "Financial"
]

for file in files:

    html = FileManager.load_html(
        file,
        EVALUATIONS_DIR
    )

    if not html:
        continue

    for keyword in keywords:

        if keyword.lower() in html.lower():

            print(
                f"{file} → found '{keyword}'"
            )

            break
