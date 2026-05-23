import pandas as pd


class Insights:

    @staticmethod
    def participant_percentage(df):

        if "bid_id" not in df.columns:
            return 0

        counts = (
            df.groupby("bid_id")
            .size()
        )

        total = len(counts)

        above_3 = len(
            counts[counts > 3]
        )

        if total == 0:
            return 0

        return round(
            (above_3 / total) * 100,
            2
        )

    @staticmethod
    def repeat_winners(df):

        if (
            "rank" not in df.columns
            or
            "seller_name" not in df.columns
        ):
            return None

        winners = df[
            df["rank"] == "L1"
        ]

        return (
            winners["seller_name"]
            .value_counts()
            .head(5)
        )

    @staticmethod
    def duplicate_vendors(df):

        if "seller_name" not in df.columns:
            return None

        duplicates = (
            df["seller_name"]
            .value_counts()
        )

        duplicates = duplicates[
            duplicates > 1
        ]

        return duplicates.head(10)

    @staticmethod
    def generate(df):

        print("\n")
        print("=" * 50)
        print("SUMMARY INSIGHTS")
        print("=" * 50)

        percentage = (
            Insights.participant_percentage(df)
        )

        print(
            f"\nBids with >3 participants: {percentage}%"
        )

        print("\nTop Repeat Winners:")

        winners = (
            Insights.repeat_winners(df)
        )

        if winners is not None:
            print(winners)
        else:
            print("No winner data available")

        print("\nDuplicate Vendors:")

        duplicates = (
            Insights.duplicate_vendors(df)
        )

        if duplicates is not None and len(duplicates) > 0:
            print(duplicates)
        else:
            print("No duplicate vendors found")