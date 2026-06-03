import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from charts import (plot_pie_chart, plot_histogram, plot_line_chart, plot_bar_chart,
                    plot_scatter, plot_box_plot, plot_heatmap, plot_area_chart,
                    plot_count_plot, plot_violin)
from filters import apply_filters, get_filter_options

st.set_page_config(page_title="ATP 2023 Dashboard", page_icon="🎾", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/apt_matches_2023.csv")
    df["tourney_date"] = pd.to_datetime(df["tourney_date"], format="%Y%m%d", errors="coerce")
    num_cols = ["minutes","winner_age","loser_age","winner_rank","loser_rank",
                "w_ace","l_ace","w_df","l_df","w_svpt","l_svpt",
                "winner_rank_points","loser_rank_points"]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.dropna(subset=["winner_name","loser_name","surface"], inplace=True)
    return df

df = load_data()

st.title("ATP 2023 Tennis Match Dashboard")
st.markdown("*Explore match statistics, player performance and tournament insights.*")
st.markdown("---")

st.sidebar.header("Filters")
opts = get_filter_options(df)

date_range = st.sidebar.date_input(
    "Tournament Date Range",
    value=(df["tourney_date"].min(), df["tourney_date"].max()),
    min_value=df["tourney_date"].min(),
    max_value=df["tourney_date"].max()
)

surfaces = st.sidebar.multiselect("Surface", opts["surfaces"], default=opts["surfaces"])
levels = st.sidebar.multiselect("Tournament Level", opts["levels"], default=opts["levels"])
rounds = st.sidebar.multiselect("Round", opts["rounds"], default=opts["rounds"])

dur_range = st.sidebar.slider("Match Duration (minutes)",
    int(df["minutes"].min()), int(df["minutes"].max()),
    (int(df["minutes"].min()), int(df["minutes"].max())))

rank_range = st.sidebar.slider("Winner Rank",
    int(df["winner_rank"].dropna().min()), int(df["winner_rank"].dropna().max()),
    (int(df["winner_rank"].dropna().min()), int(df["winner_rank"].dropna().max())))

search_text = st.sidebar.text_input("Search Player Name", "")

if st.sidebar.button("Reset All Filters"):
    st.rerun()

filtered_df = apply_filters(df, date_range, surfaces, levels, rounds, dur_range, rank_range, search_text)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Matches", f"{len(filtered_df):,}")
k2.metric("Avg Duration", f"{filtered_df['minutes'].mean():.0f} min")
k3.metric("Avg Aces", f"{filtered_df['w_ace'].mean():.1f}")
k4.metric("Tournaments", f"{filtered_df['tourney_name'].nunique()}")
k5.metric("Unique Players", f"{pd.concat([filtered_df['winner_name'], filtered_df['loser_name']]).nunique()}")

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Distribution", "Trends", "Comparisons", "Relationships", "Data"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Matches by Surface")
        fig = plot_pie_chart(filtered_df); st.pyplot(fig); plt.close()
    with c2:
        st.subheader("Match Duration Distribution")
        fig = plot_histogram(filtered_df); st.pyplot(fig); plt.close()
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Winner Age by Surface")
        fig = plot_box_plot(filtered_df); st.pyplot(fig); plt.close()
    with c4:
        st.subheader("Duration by Surface")
        fig = plot_violin(filtered_df); st.pyplot(fig); plt.close()

with tab2:
    st.subheader("Matches Per Month")
    fig = plot_line_chart(filtered_df); st.pyplot(fig); plt.close()
    st.subheader("Cumulative Matches")
    fig = plot_area_chart(filtered_df); st.pyplot(fig); plt.close()

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top 10 Winners")
        fig = plot_bar_chart(filtered_df); st.pyplot(fig); plt.close()
    with c2:
        st.subheader("Matches by Round")
        fig = plot_count_plot(filtered_df); st.pyplot(fig); plt.close()

with tab4:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Rank vs Aces")
        fig = plot_scatter(filtered_df); st.pyplot(fig); plt.close()
    with c2:
        st.subheader("Correlation Heatmap")
        fig = plot_heatmap(filtered_df); st.pyplot(fig); plt.close()

with tab5:
    st.subheader("Raw Data")
    cols = ["tourney_name","surface","round","winner_name","loser_name",
            "score","minutes","w_ace","l_ace","winner_rank","loser_rank"]
    st.dataframe(filtered_df[cols].head(200), use_container_width=True)
    st.caption(f"Showing first 200 of {len(filtered_df):,} filtered rows")

st.markdown("---")
st.caption("ATP 2023 Dashboard | EDA Course | Instructor: Ali Hassan Sherazi")
