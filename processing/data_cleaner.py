import pandas as pd


class DataCleaner:

    @staticmethod
    def process(df):

        # ----------------------
        # Fill missing values
        # ----------------------

        df = df.fillna("N/A")

        df = df.replace(
            "",
            "N/A"
        )

        # ----------------------
        # Normalize vendor names
        # ----------------------

        if "seller_name" in df.columns:

            df["seller_name"] = (

                df["seller_name"]

                .astype(str)

                .str.replace(
                    "Under PMA",
                    "",
                    regex=False
                )

                .str.replace(
                    r"\(.*?\)",
                    "",
                    regex=True
                )

                .str.strip()
            )

        # ----------------------
        # buyer
        # ----------------------

        if "department" in df.columns:

            df["buyer"] = (
                df["department"]
            )

        else:

            df["buyer"]="N/A"

        # ----------------------
        # category
        # ----------------------

        if "item" in df.columns:

            df["category"]=(
                df["item"]
            )

        else:

            df["category"]="N/A"

        # ----------------------
        # vendor fields
        # ----------------------

        if "seller_name" in df.columns:

            df["vendor_name"]=(
                df["seller_name"]
            )

        else:

            df["vendor_name"]="N/A"


        if "rank" in df.columns:

            df["vendor_rank"]=(
                df["rank"]
            )

        else:

            df["vendor_rank"]="N/A"


        if "total_price" in df.columns:

            df["vendor_price"]=(
                df["total_price"]
            )

        else:

            df["vendor_price"]="N/A"


        if "status" in df.columns:

            df["status_flag"]=(
                df["status"]
            )

        else:

            df["status_flag"]="N/A"


        # ----------------------
        # winner details
        # ----------------------

        df["winner_name"]="N/A"
        df["winner_price"]="N/A"

        if (
            "bid_id" in df.columns
            and
            "vendor_rank" in df.columns
        ):

            for bid in df["bid_id"].unique():

                bid_rows = df[
                    df["bid_id"]==bid
                ]

                winner = bid_rows[
                    bid_rows["vendor_rank"]=="L1"
                ]

                if len(winner)>0:

                    winner_name = (
                        winner.iloc[0]
                        .get(
                            "vendor_name",
                            "N/A"
                        )
                    )

                    winner_price = (
                        winner.iloc[0]
                        .get(
                            "vendor_price",
                            "N/A"
                        )
                    )

                    mask=(
                        df["bid_id"]==bid
                    )

                    df.loc[
                        mask,
                        "winner_name"
                    ]=winner_name

                    df.loc[
                        mask,
                        "winner_price"
                    ]=winner_price


        # ----------------------
        # number of bidders
        # ----------------------

        df["num_bidders"]=0

        if (
            "bid_id" in df.columns
            and
            "vendor_name" in df.columns
        ):

            bidder_counts=(

                df[
                    df["vendor_name"]!="N/A"
                ]

                .groupby(
                    "bid_id"
                )

                [
                    "vendor_name"
                ]

                .nunique()

            )

            for bid,count in bidder_counts.items():

                df.loc[
                    df["bid_id"]==bid,
                    "num_bidders"
                ]=count


        # ----------------------
        # bid value
        # ----------------------

        df["bid_value"]=(
            df["winner_price"]
        )


        # ----------------------
        # award date
        # ----------------------

        df["award_date"]="N/A"

        return df