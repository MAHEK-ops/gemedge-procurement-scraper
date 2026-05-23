import pandas as pd


class Insights:

    @staticmethod
    def participant_percentage(df):

        if (
            "seller_name" not in df.columns
            or
            "bid_id" not in df.columns
        ):
            return 0

        evaluation_df = df[
            df["seller_name"] != "N/A"
        ]

        evaluation_df = (
            evaluation_df[
                ["bid_id","seller_name"]
            ]
            .drop_duplicates()
        )

        participant_counts = (
            evaluation_df
            .groupby("bid_id")
            .size()
        )

        total = len(
            participant_counts
        )

        above_3 = len(
            participant_counts[
                participant_counts > 3
            ]
        )

        if total == 0:
            return 0

        return round(
            (above_3/total)*100,
            2
        )


    @staticmethod
    def repeat_winners(df):

        winners = df[
            df.get("rank")=="L1"
        ]

        return (
            winners["seller_name"]
            .value_counts()
            .head(5)
        )


    @staticmethod
    def duplicate_vendors(df):

        duplicates = (
            df[
                df["seller_name"]!="N/A"
            ]
            ["seller_name"]
            .value_counts()
        )

        duplicates = duplicates[
            duplicates>1
        ]

        return duplicates.head(10)


    @staticmethod
    def price_gap(df):

        if (
            "rank" not in df.columns
            or
            "total_price" not in df.columns
        ):
            return []

        financial = df[
            df["evaluation_type"]=="financial"
        ].copy()

        financial["total_price"] = (
            financial["total_price"]
            .astype(str)
            .str.replace(
                ",",
                "",
                regex=False
            )
        )

        gaps=[]

        grouped = (
            financial.groupby(
                "bid_id"
            )
        )

        for bid_id,data in grouped:

            l1 = data[
                data["rank"]=="L1"
            ]

            l2 = data[
                data["rank"]=="L2"
            ]

            if (
                len(l1)>0
                and len(l2)>0
            ):

                try:

                    l1_price=float(
                        l1.iloc[0][
                            "total_price"
                        ]
                    )

                    l2_price=float(
                        l2.iloc[0][
                            "total_price"
                        ]
                    )

                    gap=round(
                        (
                            (
                                l2_price
                                -
                                l1_price
                            )
                            /
                            l1_price
                        )*100,
                        2
                    )

                    gaps.append({

                        "bid_id":bid_id,
                        "gap_percent":gap

                    })

                except:
                    pass

        return gaps


    @staticmethod
    def generate(df):

        print("\n")
        print("="*50)
        print("SUMMARY INSIGHTS")
        print("="*50)

        print(
            f"\nBids with >3 participants: "
            f"{Insights.participant_percentage(df)}%"
        )

        print("\nTop Repeat Winners:")
        print(
            Insights.repeat_winners(df)
        )

        print("\nDuplicate Vendors:")
        print(
            Insights.duplicate_vendors(df)
        )

        print("\nL1-L2 Price Gaps:")

        gaps = Insights.price_gap(df)

        if gaps:

            for gap in gaps[:5]:

                print(gap)

        else:

            print(
                "No L1-L2 data found"
            )