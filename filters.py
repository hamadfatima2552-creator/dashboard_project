import pandas as pd

def get_filter_options(df):
    return {
        "surfaces": sorted(df["surface"].dropna().unique().tolist()),
        "levels": sorted(df["tourney_level"].dropna().unique().tolist()),
        "rounds": sorted(df["round"].dropna().unique().tolist())
    }

def apply_filters(df, date_range, surfaces, levels, rounds, dur_range, rank_range, search_text):
    filtered = df.copy()

    # Date filter
    if len(date_range) == 2:
        filtered = filtered[
            (filtered["tourney_date"].dt.date >= date_range[0]) &
            (filtered["tourney_date"].dt.date <= date_range[1])
        ]

    # Surface filter
    if surfaces:
        filtered = filtered[filtered["surface"].isin(surfaces)]

    # Level filter
    if levels:
        filtered = filtered[filtered["tourney_level"].isin(levels)]

    # Round filter
    if rounds:
        filtered = filtered[filtered["round"].isin(rounds)]

    # Duration filter
    filtered = filtered[
        (filtered["minutes"] >= dur_range[0]) &
        (filtered["minutes"] <= dur_range[1])
    ]

    # Rank filter
    filtered = filtered[
        (filtered["winner_rank"] >= rank_range[0]) &
        (filtered["winner_rank"] <= rank_range[1])
    ]

    # Search filter
    if search_text:
        mask = (
            filtered["winner_name"].str.contains(search_text, case=False, na=False) |
            filtered["loser_name"].str.contains(search_text, case=False, na=False)
        )
        filtered = filtered[mask]

    return filtered
