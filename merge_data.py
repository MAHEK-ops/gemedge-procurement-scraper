import pandas as pd
import json
import os
import re

from scraper.parser import Parser
from scraper.evaluation_parser import EvaluationParser
from utils.file_manager import FileManager
from config import EVALUATIONS_DIR


# --------------------------------
# Parse listing data
# --------------------------------

listing_records = Parser.parse_all()

listing_df = pd.DataFrame(
    listing_records
)

listing_df = listing_df.drop_duplicates(
    subset=["bid_id"]
)


# --------------------------------
# Parse evaluation data
# --------------------------------

evaluation_records = []

files = FileManager.list_html_files(
    EVALUATIONS_DIR
)

for file in files:

    html = FileManager.load_html(
        file,
        EVALUATIONS_DIR
    )

    if not html:
        continue

    rows = EvaluationParser.parse(
        html
    )

    bid_id = (
        file
        .replace(".html", "")
        .replace("_", "/")
    )

    for row in rows:

        row["bid_id"] = bid_id

        seller = row.get(
            "seller_name",
            "N/A"
        )

        if seller != "N/A":

            # Remove anything inside brackets
            seller = re.sub(
                r"\(.*?\)",
                "",
                seller
            )

            # Remove PMA text
            seller = seller.replace(
                "Under PMA",
                ""
            )

            # Normalize spaces
            seller = re.sub(
                r"\s+",
                " ",
                seller
            )

            seller = seller.strip()

        row["seller_name"] = seller

        evaluation_records.append(
            row
        )


evaluation_df = pd.DataFrame(
    evaluation_records
)


# --------------------------------
# Merge listing + evaluation
# --------------------------------

merged = pd.merge(

    evaluation_df,
    listing_df,

    on="bid_id",
    how="left"

)

merged = merged.fillna(
    "N/A"
)

# -------------------------
# Remove listing-only rows
# -------------------------

merged = merged[

    merged["seller_name"] != "N/A"

]

merged = merged[

    merged["seller_name"].notna()

]

merged = merged.reset_index(
    drop=True
)
# -------------------------
# Fix bad category values
# -------------------------

merged["category"] = merged[
    "category"
].replace(
    "Status: Bid Award",
    "N/A"
)

merged["item"] = merged[
    "item"
].replace(
    "Status: Bid Award",
    "N/A"
)


# --------------------------------
# Winner details
# --------------------------------

merged["winner_name"] = "N/A"
merged["winner_price"] = "N/A"

for bid in merged[
    "bid_id"
].unique():

    winner = merged[

        (merged["bid_id"] == bid)

        &

        (
            merged["rank"] == "L1"
        )

    ]

    if len(winner) > 0:

        winner = winner.iloc[0]

        merged.loc[
            merged["bid_id"] == bid,
            "winner_name"
        ] = winner[
            "seller_name"
        ]

        merged.loc[
            merged["bid_id"] == bid,
            "winner_price"
        ] = winner[
            "total_price"
        ]


# --------------------------------
# Bid value
# --------------------------------

merged[
    "bid_value"
] = merged[
    "winner_price"
]


# --------------------------------
# Number of bidders
# --------------------------------

counts = (

    merged.groupby(
        "bid_id"
    )["seller_name"]

    .nunique()

)

merged[
    "num_bidders"
] = (

    merged[
        "bid_id"
    ]
    .map(counts)

)


# --------------------------------
# Rename output columns
# --------------------------------

merged.rename(

    columns={

        "seller_name":
        "vendor_name",

        "rank":
        "vendor_rank",

        "total_price":
        "vendor_price",

        "status":
        "status_flag"

    },

    inplace=True

)


# --------------------------------
# Final cleanup
# --------------------------------

merged = merged.fillna(
    "N/A"
)

# Remove rows without vendors

merged = merged[
    merged["seller_name"] != "N/A"
]

merged = merged[
    merged["seller_name"] != ""
]

merged = merged.reset_index(
    drop=True
)

# Fix wrong category values

bad_values = [

    "Status: Bid Award"

]

for col in ["category","item"]:

    merged[col] = merged[col].replace(
        bad_values,
        "N/A"
    )

    merged[col] = merged[col].apply(

        lambda x:
        "N/A"

        if str(x).startswith(
            "Bid No.:"
        )

        else x
    )


# remove duplicate rows

merged = merged.drop_duplicates()


# clean spaces

for col in merged.columns:

    merged[col] = merged[
        col
    ].astype(str).str.strip()


# --------------------------------
# Save output
# --------------------------------

os.makedirs(
    "output",
    exist_ok=True
)

merged.to_csv(

    "output/procurement_data.csv",

    index=False

)

with open(

    "output/procurement_data.json",
    "w",
    encoding="utf-8"

) as f:

    json.dump(

        merged.to_dict(
            orient="records"
        ),

        f,

        indent=4,
        ensure_ascii=False

    )


print("\n" + "="*50)

print("FILES SAVED")

print("="*50)

print(
    f"CSV rows: {len(merged)}"
)

print(
    "Saved: output/procurement_data.csv"
)

print(
    "Saved: output/procurement_data.json"
)

print("="*50)