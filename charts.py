import matplotlib.pyplot as plt
import seaborn as sns

def plot_pie_chart(df):
    surface_counts = df["surface"].value_counts()
    fig, ax = plt.subplots(figsize=(7,7))
    ax.pie(surface_counts, labels=surface_counts.index, autopct="%1.1f%%", startangle=140)
    ax.set_title("Matches by Surface Type")
    return fig

def plot_histogram(df):
    fig, ax = plt.subplots(figsize=(9,5))
    ax.hist(df["minutes"].dropna(), bins=40, color="steelblue", edgecolor="white")
    ax.set_title("Distribution of Match Duration")
    ax.set_xlabel("Minutes")
    ax.set_ylabel("Frequency")
    return fig

def plot_line_chart(df):
    monthly = df.groupby(df["tourney_date"].dt.to_period("M")).size().reset_index(name="matches")
    monthly["tourney_date"] = monthly["tourney_date"].astype(str)
    fig, ax = plt.subplots(figsize=(12,5))
    ax.plot(monthly["tourney_date"], monthly["matches"], marker="o", color="darkorange")
    ax.set_title("Number of Matches Per Month (2023)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Matches")
    plt.xticks(rotation=45)
    return fig

def plot_bar_chart(df):
    top_winners = df["winner_name"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    top_winners.plot(kind="bar", color="teal", edgecolor="black", ax=ax)
    ax.set_title("Top 10 Players by Wins (2023)")
    ax.set_xlabel("Player")
    ax.set_ylabel("Wins")
    plt.xticks(rotation=45, ha="right")
    return fig

def plot_scatter(df):
    fig, ax = plt.subplots(figsize=(9,6))
    ax.scatter(df["winner_rank"], df["w_ace"], alpha=0.4, color="crimson", s=20)
    ax.set_title("Winner Rank vs Aces Served")
    ax.set_xlabel("Winner Rank")
    ax.set_ylabel("Aces")
    return fig

def plot_box_plot(df):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.boxplot(data=df, x="surface", y="winner_age", hue="surface", palette="Set2", legend=False, ax=ax)
    ax.set_title("Winner Age Distribution by Surface")
    ax.set_xlabel("Surface")
    ax.set_ylabel("Age")
    return fig

def plot_heatmap(df):
    num_df = df[["minutes","w_ace","l_ace","w_df","winner_age","loser_age",
                 "winner_rank","loser_rank","winner_rank_points"]].dropna()
    fig, ax = plt.subplots(figsize=(11,8))
    sns.heatmap(num_df.corr(), annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, ax=ax)
    ax.set_title("Feature Correlation Heatmap")
    return fig

def plot_area_chart(df):
    monthly_cum = df.groupby(df["tourney_date"].dt.to_period("M")).size().cumsum().reset_index(name="cumulative")
    monthly_cum["tourney_date"] = monthly_cum["tourney_date"].astype(str)
    fig, ax = plt.subplots(figsize=(12,5))
    ax.fill_between(monthly_cum["tourney_date"], monthly_cum["cumulative"], alpha=0.5, color="mediumseagreen")
    ax.plot(monthly_cum["tourney_date"], monthly_cum["cumulative"], color="green")
    ax.set_title("Cumulative Matches Over 2023")
    ax.set_xlabel("Month")
    ax.set_ylabel("Cumulative Matches")
    plt.xticks(rotation=45)
    return fig

def plot_count_plot(df):
    round_order = ["R128","R64","R32","R16","QF","SF","F"]
    valid_rounds = [r for r in round_order if r in df["round"].values]
    fig, ax = plt.subplots(figsize=(10,6))
    sns.countplot(data=df, x="round", order=valid_rounds, hue="round", palette="viridis", legend=False, ax=ax)
    ax.set_title("Match Count by Round")
    ax.set_xlabel("Round")
    ax.set_ylabel("Count")
    return fig

def plot_violin(df):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.violinplot(data=df, x="surface", y="minutes", hue="surface", palette="muted", legend=False, ax=ax)
    ax.set_title("Match Duration Distribution by Surface")
    ax.set_xlabel("Surface")
    ax.set_ylabel("Minutes")
    return fig
