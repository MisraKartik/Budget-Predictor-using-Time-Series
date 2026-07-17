from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="CPI Budget Forecaster", layout="wide", page_icon="🏛️")

INDIGO = "#1B2A4A"
GOLD = "#B8934A"
CREAM = "#F7F4EC"
CREAM_LINE = "#D8D3C4"
MUTED = "#6B6252"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {{
        color-scheme: light;
    }}

    html, body, [class*="css"] {{
        color: {INDIGO} !important;
    }}

    .stApp {{
        background-color: {CREAM};
    }}

    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p,
    [data-testid="stHeader"],
    [data-testid="stAppViewContainer"],
    [data-testid="stNumberInputContainer"],
    label,
    .bulletin-kicker {{
        color: {INDIGO} !important;
    }}

    [data-testid="stCaptionContainer"] p {{
        color: {MUTED} !important;
    }}

    .bulletin-kicker {{
        color: {GOLD} !important;
    }}

    h1, h2, h3 {{
        font-family: 'Source Serif 4', Georgia, serif !important;
        font-weight: 500 !important;
        color: {INDIGO} !important;
        letter-spacing: -0.01em;
    }}

    h1 {{
        border-bottom: 2px solid {INDIGO};
        padding-bottom: 0.5rem;
    }}

    p, span, div, label {{
        font-family: 'Source Serif 4', Georgia, serif;
    }}

    .bulletin-kicker {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: {GOLD};
        margin-bottom: -0.6rem;
    }}

    /* Metric cards */
    div[data-testid="stMetric"] {{
        background-color: #FFFFFF;
        border: 0.5px solid {CREAM_LINE};
        border-radius: 0px;
        padding: 0.9rem 1rem;
    }}
    div[data-testid="stMetricLabel"] {{
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem !important;
        color: {MUTED} !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    div[data-testid="stMetricValue"] {{
        font-family: 'JetBrains Mono', monospace !important;
        color: {INDIGO} !important;
    }}
    div[data-testid="stMetricDelta"] {{
        font-family: 'JetBrains Mono', monospace !important;
    }}

    /* Tabs */
    button[data-baseweb="tab"] {{
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: {MUTED} !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {INDIGO} !important;
        border-bottom-color: {GOLD} !important;
    }}
    div[data-baseweb="tab-highlight"] {{
        background-color: {GOLD} !important;
    }}

    /* Number inputs */
    div[data-testid="stNumberInput"] label {{
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.78rem !important;
        color: {MUTED} !important;
    }}

    /* Dataframes */
    div[data-testid="stDataFrame"] {{
        font-family: 'JetBrains Mono', monospace !important;
        border: 0.5px solid {CREAM_LINE} !important;
    }}

    /* Expander */
    div[data-testid="stExpander"] {{
        border: 0.5px solid {CREAM_LINE} !important;
        border-radius: 0px !important;
        background-color: #FFFFFF;
    }}

    hr {{
        border-color: {CREAM_LINE};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

APP_DIR = Path(__file__).parent
CATEGORIES = ["Education", "Energy", "Food", "Housing", "Medical", "Transportation"]

MODEL_FILES = {
    "SARIMA": "sarima_predictions.csv",
    "SARIMAX": "sarimax_predictions.csv",
    "Ridge Regression": "regression_predictions.csv",
}

DEFAULT_BUDGET = {
    "Education": 3000, "Energy": 4000, "Food": 6000,
    "Housing": 15000, "Medical": 2000, "Transportation": 3000,
}

CATEGORY_COLORS = ["#1B2A4A", "#3D5170", "#7C8AA0", "#B8934A", "#D6BD8C", "#8C6B3F"]


def _bulletin_altair_theme():
    return {
        "config": {
            "background": CREAM,
            "font": "Source Serif 4, Georgia, serif",
            "title": {"font": "Source Serif 4, Georgia, serif", "fontSize": 14, "color": INDIGO, "fontWeight": 500},
            "axis": {
                "labelFont": "JetBrains Mono, monospace",
                "labelFontSize": 10,
                "labelColor": MUTED,
                "titleFont": "JetBrains Mono, monospace",
                "titleFontSize": 10,
                "titleColor": MUTED,
                "gridColor": CREAM_LINE,
                "domainColor": CREAM_LINE,
                "tickColor": CREAM_LINE,
            },
            "legend": {
                "labelFont": "JetBrains Mono, monospace",
                "labelFontSize": 10,
                "labelColor": INDIGO,
                "titleFont": "JetBrains Mono, monospace",
                "titleColor": MUTED,
                "titleFontSize": 10,
            },
            "header": {
                "labelFont": "JetBrains Mono, monospace",
                "labelFontSize": 10,
                "labelColor": INDIGO,
                "titleFont": "JetBrains Mono, monospace",
            },
            "range": {"category": CATEGORY_COLORS},
            "view": {"stroke": CREAM_LINE},
        }
    }


alt.themes.register("bulletin", _bulletin_altair_theme)
alt.themes.enable("bulletin")


@st.cache_data
def load_forecast(filename: str) -> pd.DataFrame:
    df = pd.read_csv(APP_DIR / filename, index_col=0, parse_dates=True)
    df.index.name = "Date"
    return df[CATEGORIES]


def project_budget(current_budget: dict, cpi_df: pd.DataFrame) -> pd.DataFrame:
    """
    Scale each category's user-entered current budget forward using the
    ratio of forecasted CPI to the first forecasted month's CPI:
        projected_budget[t] = current_budget * cpi[t] / cpi[0]
    """
    base = cpi_df.iloc[0]
    ratios = cpi_df.divide(base)
    budget_row = pd.Series(current_budget)[CATEGORIES]
    return ratios.multiply(budget_row, axis=1)


def small_multiples_chart(proj_df: pd.DataFrame) -> alt.Chart:
    """
    One mini line chart per category, each with its own y-axis scale, so a
    category with a small absolute budget isn't flattened by one with a
    much larger budget on a shared axis.
    """
    long_df = proj_df.reset_index().melt(id_vars="Date", var_name="Category", value_name="Budget")

    chart = (
        alt.Chart(long_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Date:T", title=None, axis=alt.Axis(format="%b %y")),
            y=alt.Y("Budget:Q", title="₹", scale=alt.Scale(zero=False)),
            tooltip=["Date:T", "Category:N", alt.Tooltip("Budget:Q", format=",.0f")],
            color=alt.Color("Category:N", legend=None),
        )
        .properties(width=220, height=160)
        .facet(facet=alt.Facet("Category:N", title=None), columns=3)
        .resolve_scale(y="independent")
    )
    return chart


def normalized_comparison_chart(proj_df: pd.DataFrame) -> alt.Chart:
    """
    All categories indexed to 100 at the first forecast month, plotted on
    one shared axis -- lets you compare rate of change across categories
    regardless of their absolute budget size.
    """
    indexed = proj_df.divide(proj_df.iloc[0]).multiply(100)
    long_df = indexed.reset_index().melt(id_vars="Date", var_name="Category", value_name="Index")

    chart = (
        alt.Chart(long_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Date:T", title=None, axis=alt.Axis(format="%b %y")),
            y=alt.Y("Index:Q", title="Index (first month = 100)", scale=alt.Scale(zero=False)),
            color=alt.Color("Category:N", title="Category"),
            tooltip=["Date:T", "Category:N", alt.Tooltip("Index:Q", format=".2f")],
        )
        .properties(height=320)
    )
    return chart


def rank_change_chart(cpi_df: pd.DataFrame) -> alt.Chart:
    """
    Ranks categories by percentage change in forecasted CPI from the first
    to the last forecast month, highest change first, so it's immediately
    clear which categories are driving the budget increase.
    """
    pct_change = (cpi_df.iloc[-1] / cpi_df.iloc[0] - 1) * 100
    rank_df = pct_change.reset_index()
    rank_df.columns = ["Category", "Change"]
    rank_df = rank_df.sort_values("Change", ascending=False)

    chart = (
        alt.Chart(rank_df)
        .mark_bar(color=GOLD)
        .encode(
            x=alt.X("Change:Q", title="Forecast CPI change (%)"),
            y=alt.Y("Category:N", sort="-x", title=None),
            tooltip=["Category:N", alt.Tooltip("Change:Q", format="+.2f")],
        )
        .properties(height=220)
    )

    labels = chart.mark_text(
        align="left", dx=4, font="JetBrains Mono, monospace", fontSize=10, color=INDIGO
    ).encode(text=alt.Text("Change:Q", format="+.2f"))

    return chart + labels


def render_model_tab(model_name: str, current_budget: dict):
    cpi_df = load_forecast(MODEL_FILES[model_name])

    proj_df = project_budget(current_budget, cpi_df)

    total_now = sum(current_budget.values())
    total_future = proj_df.iloc[-1].sum()
    pct_change = (total_future / total_now - 1) * 100 if total_now else 0

    m1, m2, m3 = st.columns(3)
    m1.metric("Current total monthly budget", f"${total_now:,.0f}")
    m2.metric(
        f"Projected total ({proj_df.index[-1].strftime('%b %Y')})",
        f"${total_future:,.0f}",
        f"{pct_change:+.2f}%",
    )
    m3.metric("Categories tracked", len(CATEGORIES))

    st.markdown('<p class="bulletin-kicker">Exhibit 1</p>', unsafe_allow_html=True)
    st.markdown("**Projected budget per category** (independent y-axis per category, so small categories don't get flattened by large ones)")
    st.altair_chart(small_multiples_chart(proj_df), use_container_width=False)

    st.markdown('<p class="bulletin-kicker">Exhibit 2</p>', unsafe_allow_html=True)
    st.markdown("**Relative comparison** (all categories indexed to 100 at the first forecast month)")
    st.altair_chart(normalized_comparison_chart(proj_df), use_container_width=True)

    st.markdown('<p class="bulletin-kicker">Exhibit 3</p>', unsafe_allow_html=True)
    st.markdown("**Categories ranked by forecast CPI change** (highest increase first, over the 6-month forecast horizon)")
    st.altair_chart(rank_change_chart(cpi_df), use_container_width=True)

    st.markdown('<p class="bulletin-kicker">Table 1</p>', unsafe_allow_html=True)
    st.markdown("**Projected budget table ($)**")
    st.dataframe(proj_df.style.format("${:,.0f}"), use_container_width=True)

    with st.expander("Show underlying CPI forecast used"):
        st.dataframe(cpi_df.style.format("{:.2f}"), use_container_width=True)


st.markdown('<p class="bulletin-kicker">Statistical release · Household budget series</p>', unsafe_allow_html=True)
st.title("CPI-Adjusted Budget Forecaster")
st.caption(
    "Enter your current monthly spend per category and see how much you'd "
    "need to budget over the next 6 months, based on category-level CPI "
    "forecasts from three different models."
)

st.markdown('<p class="bulletin-kicker">Input</p>', unsafe_allow_html=True)
st.markdown("**Enter your current monthly budget by category ($)**")
cols = st.columns(3)
current_budget = {}
for i, cat in enumerate(CATEGORIES):
    with cols[i % 3]:
        current_budget[cat] = st.number_input(
            cat, min_value=0, value=DEFAULT_BUDGET[cat], step=100, key=f"budget_{cat}",
        )

st.markdown('<p class="bulletin-kicker">Select model</p>', unsafe_allow_html=True)
tab_sarima, tab_sarimax, tab_ridge = st.tabs(["SARIMA", "SARIMAX", "Ridge Regression"])

with tab_sarima:
    render_model_tab("SARIMA", current_budget)

with tab_sarimax:
    render_model_tab("SARIMAX", current_budget)

with tab_ridge:
    render_model_tab("Ridge Regression", current_budget)