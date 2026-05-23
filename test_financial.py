from bs4 import BeautifulSoup
from utils.file_manager import FileManager
from config import EVALUATIONS_DIR

html = FileManager.load_html(
    "GEM_2026_B_7501724.html",
    EVALUATIONS_DIR
)

soup = BeautifulSoup(
    html,
    "html.parser"
)

tables = soup.select("table")

print("Total tables:", len(tables))
print()

for i, table in enumerate(tables):

    print("=" * 70)
    print(f"TABLE {i+1}")

    headers = [
        h.get_text(" ", strip=True)
        for h in table.select("th")
    ]

    print("HEADERS:")
    print(headers)

    rows = table.select("tbody tr")

    print("\nSample rows:")

    for row in rows[:3]:

        cols = [
            td.get_text(" ", strip=True)
            for td in row.find_all("td")
        ]

        print(cols)

    print()