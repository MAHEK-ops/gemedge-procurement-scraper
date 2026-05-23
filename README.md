# GemEdge Procurement Intelligence Scraper

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-green.svg)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-orange.svg)

> An end-to-end procurement intelligence scraper for extracting and analyzing procurement data from India's Government e-Marketplace (GeM) portal.

---

## Project Overview

GemEdge Procurement Intelligence Scraper extracts procurement data from the GeM portal by collecting bid listings and result/evaluation pages. The system processes raw HTML into structured datasets and generates procurement insights.

**Target Website:** GeM Portal – All Bids  
https://bidplus.gem.gov.in/all-bids

---

## Features

### Data Extraction
- Extracts bid listing data
- Fetches result/evaluation pages
- Extracts:
  - Bid IDs
  - Buyer/Department details
  - Quantity
  - Vendor names
  - Vendor rankings (L1/L2/L3)
  - Vendor prices
  - Winner name
  - Winner price
  - Number of bidders
  - Technical status

### Evaluation Parsing
- Technical evaluation parsing
- Financial evaluation parsing
- Reverse Auction (RA) handling when available

### Data Processing
- Vendor name cleanup and normalization
- Duplicate detection
- Missing value handling using `"N/A"`
- Data validation and merging

### Insights Generated
- Percentage of bids with more than 3 participants
- Repeat winners analysis
- L1–L2 price gap analysis
- Anomaly detection (winner not lowest bidder)

### Output
- CSV export
- JSON export

---

## Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Core language |
| Playwright | Browser automation |
| BeautifulSoup | HTML parsing |
| Pandas | Data processing |
| Regex | Pattern extraction |

---

## Project Structure

```text
gemedge-procurement-scraper/
│
├── scraper/
│   ├── gem_fetcher.py
│   ├── result_fetcher.py
│   ├── parser.py
│   └── evaluation_parser.py
│
├── processing/
│   └── insights.py
│
├── utils/
│   ├── logger.py
│   └── file_manager.py
│
├── raw_html/
│   ├── listings/
│   └── evaluations/
│
├── output/
│   ├── procurement_data.csv
│   └── procurement_data.json
│
├── config.py
├── main.py
└── requirements.txt
```

---

## Installation

```bash
git clone https://github.com/yourusername/gemedge-procurement-scraper.git

cd gemedge-procurement-scraper

python -m venv venv

source venv/bin/activate
# Windows:
# venv\Scripts\activate

pip install -r requirements.txt

playwright install chromium
```

---

## Usage

### Step 1: Fetch HTML

```bash
python main.py --fetch --limit 50
```

This saves raw HTML locally.

### Step 2: Parse HTML

```bash
python main.py --parse
```

This processes saved files and generates structured datasets.

---

## Output Schema

| Field | Description |
|---------|-------------|
| bid_id | Unique bid identifier |
| buyer | Buyer/department |
| quantity | Required quantity |
| winner_name | Winning vendor |
| winner_price | Winning bid value |
| num_bidders | Number of participants |
| vendor_name | Vendor name |
| vendor_rank | L1/L2/L3 |
| vendor_price | Vendor quotation |
| status_flag | Qualified/Disqualified |

---

## Processing Pipeline

```text
GeM Website
     ↓
Fetch HTML using Playwright
     ↓
Store raw HTML locally
     ↓
Parse HTML using BeautifulSoup + Regex
     ↓
Clean and normalize data
     ↓
Generate insights
     ↓
Export CSV + JSON
```

---

## Sample Insights

```text
Bids with >3 participants: 15.38%

Top Repeat Winners:
- M/S SHREE ENTERPRISES
- R T ENTERPRISES

Sample L1-L2 Price Gaps:
- 0.02%
- 0.35%
- 10.17%

Anomalies:
No anomalies found
```

---

## Challenges Faced

1. Dynamic result pages required browser automation.

2. Technical and financial sections had different structures.

3. Vendor names contained additional labels such as:
- Under PMA
- MSE tags
- Social category labels

4. Some result pages did not contain evaluation tables.

---

## Future Improvements

- Database integration (PostgreSQL/MongoDB)
- Scheduled scraping automation
- Dashboard for procurement insights
- Better category extraction
- Improved validation rules

---
