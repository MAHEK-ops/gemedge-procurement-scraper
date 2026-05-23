from scraper.evaluation_parser import EvaluationParser

parser=EvaluationParser()

records=parser.parse_all_evaluations()

print(records[:5])

print()

print(
    "Total seller records:",
    len(records)
)