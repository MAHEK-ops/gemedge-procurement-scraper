from parser.evaluation_parser import EvaluationParser
from utils.file_manager import FileManager
from config import EVALUATIONS_DIR

files = FileManager.list_html_files(EVALUATIONS_DIR)

total_records=[]

for file in files:

    html = FileManager.load_html(
        file,
        EVALUATIONS_DIR
    )

    results=EvaluationParser.parse(html)

    if results:

        print(f"\n{file}")
        print(f"Records found: {len(results)}")

        print(results[:2])

        total_records.extend(results)

print("\n======================")
print("TOTAL RECORDS")
print(len(total_records))