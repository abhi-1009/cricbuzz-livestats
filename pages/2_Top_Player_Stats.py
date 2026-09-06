import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styling import apply_custom_style, apply_page_accent
from api_client import get_top_stats

st.set_page_config(page_title="Top Player Stats", page_icon="📊", layout="wide")

apply_custom_style()
apply_page_accent("#F9A825")

st.title("📊 Top Player Stats")

stat_choice = st.selectbox(
    "Category",
    options=["mostRuns", "highestScore", "highestAvg", "highestSr", "mostHundreds",
             "mostFifties", "mostFours", "mostSixes", "mostNineties",
             "mostWickets", "lowestAvg", "bestBowlingInnings", "mostFiveWickets",
             "lowestEcon", "lowestSr"],
    format_func=lambda x: {
        "mostRuns": "Most Runs", "highestScore": "Highest Score",
        "highestAvg": "Best Batting Average", "highestSr": "Best Batting Strike Rate",
        "mostHundreds": "Most Hundreds", "mostFifties": "Most Fifties",
        "mostFours": "Most Fours", "mostSixes": "Most Sixes",
        "mostNineties": "Most Nineties", "mostWickets": "Most Wickets",
        "lowestAvg": "Best Bowling Average", "bestBowlingInnings": "Best Bowling Figures",
        "mostFiveWickets": "Most 5-Wicket Hauls", "lowestEcon": "Best Economy",
        "lowestSr": "Best Bowling Strike Rate",
    }.get(x, x)
)


@st.cache_data(ttl=600)
def load_top_stats(stats_type):
    return get_top_stats(stats_type=stats_type)


data = load_top_stats(stat_choice)

if not data or "values" not in data:
    st.warning("No data available for this category.")
else:
    headers = data.get("headers", [])
    rows = [entry["values"] for entry in data["values"]]
    display_rows = [row[1:] if len(row) == len(headers) + 1 else row for row in rows]

    import pandas as pd
    df = pd.DataFrame(display_rows, columns=headers)
    st.dataframe(df, use_container_width=True, hide_index=True)
    df = pd.DataFrame(display_rows, columns=headers)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Quick bar chart of the top 10 (uses whatever numeric column comes 2nd — runs, wickets, etc.)
    if len(df.columns) >= 2:
        numeric_col = df.columns[1]
        try:
            chart_df = df.head(10).copy()
            chart_df[numeric_col] = pd.to_numeric(chart_df[numeric_col], errors="coerce")
            st.bar_chart(chart_df.set_index(df.columns[0])[numeric_col])
        except Exception:
            pass  # skip chart silently if the column isn't chartable
st.divider()
if st.button("🔄 Refresh (uses 1 API call)"):
    st.cache_data.clear()
    st.rerun()