import pandas as pd


class Insights:

    @staticmethod
    def participant_percentage(df):

        evaluation_df = df[
            df["vendor_name"] != "N/A"
        ]

        participant_counts = (

            evaluation_df
            .groupby("bid_id")
            ["vendor_name"]
            .nunique()

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

        winners=df[
            df["vendor_rank"]=="L1"
        ]

        return (

            winners[
                "vendor_name"
            ]
            .value_counts()
            .head(5)

        )


    @staticmethod
    def duplicate_vendors(df):

        unique=(

            df[
                ["bid_id","vendor_name"]
            ]

            .drop_duplicates()

        )

        duplicates=(

            unique[
                unique[
                    "vendor_name"
                ]!="N/A"
            ]

            [
                "vendor_name"
            ]

            .value_counts()

        )

        return duplicates[
            duplicates>1
        ].head(10)


    @staticmethod
    def price_gap(df):

        financial=df[

            df["vendor_rank"]!="N/A"

        ]

        gaps=[]

        grouped=financial.groupby(
            "bid_id"
        )

        for bid_id,data in grouped:

            l1=data[
                data[
                    "vendor_rank"
                ]=="L1"
            ]

            l2=data[
                data[
                    "vendor_rank"
                ]=="L2"
            ]

            if len(l1)==0 or len(l2)==0:
                continue

            try:

                p1=float(
                    str(
                        l1.iloc[0][
                            "vendor_price"
                        ]
                    ).replace(",","")
                )

                p2=float(
                    str(
                        l2.iloc[0][
                            "vendor_price"
                        ]
                    ).replace(",","")
                )

                gap=round(
                    ((p2-p1)/p1)*100,
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
    def anomaly_detection(df):

        anomalies=[]

        grouped=df.groupby(
            "bid_id"
        )

        for bid_id,data in grouped:

            prices=[]

            for price in data[
                "vendor_price"
            ]:

                try:

                    prices.append(
                        float(
                            str(price)
                            .replace(",","")
                        )
                    )

                except:
                    pass

            if not prices:
                continue

            min_price=min(
                prices
            )

            winner=data[
                data[
                    "vendor_rank"
                ]=="L1"
            ]

            if len(winner)==0:
                continue

            try:

                winner_price=float(

                    str(
                        winner.iloc[0][
                            "vendor_price"
                        ]
                    ).replace(",","")

                )

                if winner_price>min_price:

                    anomalies.append({

                        "bid_id":bid_id,
                        "winner_price":winner_price,
                        "lowest_price":min_price

                    })

            except:
                pass

        return anomalies


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

        print(
            "\nTop Repeat Winners:"
        )

        print(
            Insights.repeat_winners(df)
        )

        print(
            "\nDuplicate Vendors:"
        )

        print(
            Insights.duplicate_vendors(df)
        )

        print(
            "\nL1-L2 Price Gaps:"
        )

        for gap in Insights.price_gap(df)[:5]:

            print(gap)

        print(
            "\nAnomalies:"
        )

        anomalies=(
            Insights.anomaly_detection(df)
        )

        if anomalies:

            for a in anomalies[:5]:

                print(a)

        else:

            print(
                "No anomalies found"
            )