from scraper.parser import GemParser

parser = GemParser()

records = parser.parse_all_listing_pages()

print(records[:3])
print()
print("Total records:", len(records))