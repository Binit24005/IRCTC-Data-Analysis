import os
import copy
import json
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="IRCTC Analytics — Passenger Flow & Ticketing Intelligence",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# DESIGN TOKENS
# ==================================================
# Palette: a railway control-room board — deep near-black slate,
# a signal-amber accent for primary data, cool cyan/green for
# secondary series. Headlines in Space Grotesk, all figures and
# small data labels in a mono face (departure-board feel).

COLORS = {
    "bg": "#0A0E16",
    "bg_elev": "#111826",
    "bg_elev_2": "#161F30",
    "border": "rgba(148, 163, 184, 0.14)",
    "text": "#E7ECF3",
    "text_dim": "#8C96A8",
    "amber": "#F2A93B",
    "cyan": "#4FC3E0",
    "green": "#3FCF8E",
    "rose": "#E27D7D",
}

CHART_SEQUENCE = [
    COLORS["amber"], COLORS["cyan"], COLORS["green"],
    COLORS["rose"], "#8C96A8", "#B98CE0",
]


def apply_plotly_theme(fig, height=450):
    fig.update_layout(
        height=height,
        paper_bgcolor=COLORS["bg_elev"],
        plot_bgcolor=COLORS["bg_elev"],
        font=dict(family="IBM Plex Mono, monospace", color=COLORS["text_dim"], size=12),
        title=dict(font=dict(family="Space Grotesk, sans-serif", color=COLORS["text"], size=16)),
        margin=dict(l=10, r=10, t=50, b=10),
        colorway=CHART_SEQUENCE,
        legend=dict(font=dict(color=COLORS["text_dim"])),
    )
    fig.update_xaxes(showgrid=False, linecolor=COLORS["border"], zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["border"], zeroline=False)
    return fig


def render_animated_chart(fig, div_id, value_key="y", trace_index=0, height=450):
    """
    Renders a Plotly figure that grows/animates in from a zero state
    the moment it lands on the page — a departure-board "flip in"
    for the data, rather than a static image appearing.

    value_key: which attribute holds the plotted magnitude
               ("y" for vertical bars, "x" for horizontal bars,
               "values" for pie charts).

    Plotly.js is bundled inline (include_plotlyjs=True) rather than
    pulled from a CDN, so the chart still renders with no internet
    access or if a CDN request is blocked. A hard fallback forces
    the real data onto the chart a few seconds in regardless of
    whether the animation itself fired, so the chart can never be
    left showing an empty/zeroed-out state.
    """

    # Read the real values off the ORIGINAL figure first. Newer Plotly
    # versions store array data in a compact binary form internally
    # ({'dtype': ..., 'bdata': ...}) that surfaces after a deepcopy or
    # serialization pass, so grabbing this after copying would silently
    # hand back garbage instead of the actual numbers.
    target = [float(v) for v in fig.data[trace_index][value_key]]

    anim_fig = copy.deepcopy(fig)

    start = [1e-6] * len(target) if value_key == "values" else [0] * len(target)

    anim_fig.data[trace_index][value_key] = start

    trace_type = anim_fig.data[trace_index].type

    anim_fig.frames = [
        go.Frame(
            data=[{"type": trace_type, value_key: target}],
            traces=[trace_index],
            name="grow",
        )
    ]

    html_str = anim_fig.to_html(
        include_plotlyjs=True,
        full_html=False,
        div_id=div_id,
        config={"displaylogo": False, "responsive": True},
    )

    target_json = json.dumps(target)

    autoplay_script = f"""
    <style>
        html, body {{ margin: 0; background: {COLORS["bg_elev"]}; }}
    </style>
    <script>
    (function() {{
        var TARGET = {target_json};

        function forceFinal() {{
            var gd = document.getElementById('{div_id}');
            if (gd && window.Plotly) {{
                try {{
                    Plotly.restyle(gd, {{'{value_key}': [TARGET]}}, [{trace_index}]);
                }} catch (e) {{ /* no-op: chart may already show final data */ }}
            }}
        }}

        function tryAnimate(attempt) {{
            var gd = document.getElementById('{div_id}');
            if (gd && gd.data && window.Plotly) {{
                var p = Plotly.animate(gd, ['grow'], {{
                    frame: {{ duration: 950, redraw: true }},
                    transition: {{ duration: 750, easing: 'cubic-in-out' }}
                }});
                if (p && typeof p.catch === 'function') {{
                    p.catch(forceFinal);
                }}
            }} else if (attempt < 25) {{
                setTimeout(function() {{ tryAnimate(attempt + 1); }}, 120);
            }} else {{
                forceFinal();
            }}
        }}

        setTimeout(function() {{ tryAnimate(0); }}, 200);
        // Safety net: whatever happened above, guarantee the real
        // data is on screen shortly after load.
        setTimeout(forceFinal, 2500);
    }})();
    </script>
    """

    components.html(html_str + autoplay_script, height=height + 30, scrolling=False)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'IBM Plex Mono', monospace;
    }}

    .stApp {{
        background-color: {COLORS["bg"]};
        color: {COLORS["text"]};
    }}

    section[data-testid="stSidebar"] {{
        background-color: {COLORS["bg_elev"]};
        border-right: 1px solid {COLORS["border"]};
    }}

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        animation: fadeInUp 0.6s ease both;
    }}

    h1, h2, h3, .dashboard-title {{
        font-family: 'Space Grotesk', sans-serif !important;
        color: {COLORS["text"]} !important;
    }}

    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(14px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes pulse {{
        0%   {{ box-shadow: 0 0 0 0 rgba(63, 207, 142, 0.55); }}
        70%  {{ box-shadow: 0 0 0 8px rgba(63, 207, 142, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(63, 207, 142, 0); }}
    }}

    @keyframes trackMove {{
        from {{ background-position: 0 0; }}
        to   {{ background-position: 60px 0; }}
    }}

    /* ---------- AMBIENT BACKGROUND ---------- */

    .bg-fx {{
        position: fixed;
        inset: 0;
        z-index: 0;
        overflow: hidden;
        pointer-events: none;
    }}

    .bg-grid {{
        position: absolute;
        inset: -10%;
        background-image:
            linear-gradient(rgba(242, 169, 59, 0.055) 1px, transparent 1px),
            linear-gradient(90deg, rgba(79, 195, 224, 0.055) 1px, transparent 1px);
        background-size: 48px 48px;
        animation: gridDrift 32s linear infinite;
    }}

    @keyframes gridDrift {{
        from {{ transform: translate(0, 0); }}
        to   {{ transform: translate(48px, 48px); }}
    }}

    .bg-sweep {{
        position: absolute;
        top: -30%;
        left: -20%;
        width: 60%;
        height: 160%;
        background: linear-gradient(
            100deg,
            transparent 40%,
            rgba(79, 195, 224, 0.05) 48%,
            rgba(242, 169, 59, 0.06) 50%,
            transparent 58%
        );
        animation: sweepAcross 14s ease-in-out infinite;
    }}

    @keyframes sweepAcross {{
        0%   {{ transform: translateX(0%); }}
        50%  {{ transform: translateX(220%); }}
        100% {{ transform: translateX(0%); }}
    }}

    .bg-spark {{
        position: absolute;
        bottom: -12px;
        border-radius: 50%;
        opacity: 0;
        animation-name: floatUp;
        animation-timing-function: linear;
        animation-iteration-count: infinite;
    }}

    @keyframes floatUp {{
        0%   {{ transform: translateY(0) scale(1); opacity: 0; }}
        8%   {{ opacity: 0.75; }}
        92%  {{ opacity: 0.35; }}
        100% {{ transform: translateY(-108vh) scale(0.5); opacity: 0; }}
    }}

    .block-container {{
        position: relative;
        z-index: 1;
    }}

    /* ---------- HERO ---------- */

    .hero {{
        padding: 34px 36px 28px 36px;
        border-radius: 14px;
        background: linear-gradient(180deg, {COLORS["bg_elev"]} 0%, {COLORS["bg"]} 100%);
        border: 1px solid {COLORS["border"]};
        margin-bottom: 22px;
    }}

    .hero-live {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
        letter-spacing: 0.04em;
        color: {COLORS["green"]};
        margin-bottom: 14px;
    }}

    .hero-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: {COLORS["green"]};
        animation: pulse 2s infinite;
    }}

    .hero-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 40px;
        font-weight: 700;
        margin: 0 0 6px 0;
        line-height: 1.15;
        animation: titleGlow 5s ease-in-out infinite;
    }}

    @keyframes titleGlow {{
        0%, 100% {{ text-shadow: 0 0 0 rgba(242, 169, 59, 0); }}
        50%      {{ text-shadow: 0 0 18px rgba(242, 169, 59, 0.28); }}
    }}

    .hero-sub {{
        font-size: 15.5px;
        color: {COLORS["text_dim"]};
        max-width: 640px;
        margin-bottom: 20px;
        line-height: 1.55;
    }}

    .hero-track {{
        height: 2px;
        width: 100%;
        margin-bottom: 22px;
        background-image: repeating-linear-gradient(
            90deg,
            {COLORS["amber"]} 0px, {COLORS["amber"]} 22px,
            transparent 22px, transparent 38px
        );
        opacity: 0.55;
        animation: trackMove 2.4s linear infinite;
    }}

    .stat-strip {{
        display: flex;
        gap: 14px;
        flex-wrap: wrap;
    }}

    .stat-tile {{
        flex: 1;
        min-width: 150px;
        padding: 14px 18px;
        border-radius: 10px;
        background: {COLORS["bg_elev_2"]};
        border: 1px solid {COLORS["border"]};
    }}

    .stat-tile .stat-value {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 22px;
        font-weight: 600;
        color: {COLORS["amber"]};
    }}

    .stat-tile .stat-label {{
        font-size: 11.5px;
        color: {COLORS["text_dim"]};
        margin-top: 2px;
    }}

    /* ---------- KPI + INSIGHT CARDS ---------- */

    .kpi-card {{
        padding: 18px 20px;
        border-radius: 12px;
        background: {COLORS["bg_elev"]};
        border: 1px solid {COLORS["border"]};
        transition: transform 0.2s ease, border-color 0.2s ease;
        min-height: 96px;
    }}

    .kpi-card:hover {{
        transform: translateY(-3px);
        border-color: {COLORS["amber"]};
    }}

    .kpi-label {{
        font-size: 12px;
        color: {COLORS["text_dim"]};
        margin-bottom: 8px;
    }}

    .kpi-value {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: {COLORS["text"]};
    }}

    .insight-box {{
        padding: 16px 18px;
        border-radius: 10px;
        background: {COLORS["bg_elev"]};
        border: 1px solid {COLORS["border"]};
        border-left: 3px solid var(--accent, {COLORS["amber"]});
        margin-bottom: 12px;
        min-height: 84px;
        transition: transform 0.2s ease;
    }}

    .insight-box:hover {{
        transform: translateY(-2px);
    }}

    .insight-label {{
        font-size: 12px;
        color: {COLORS["text_dim"]};
        margin-bottom: 6px;
    }}

    .insight-value {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 16.5px;
        font-weight: 600;
        color: {COLORS["text"]};
    }}

    .section-heading {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 21px;
        font-weight: 600;
        margin-bottom: 2px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .section-description {{
        color: {COLORS["text_dim"]};
        font-size: 13.5px;
        margin-bottom: 14px;
    }}

    .info-card {{
        padding: 20px;
        border-radius: 12px;
        background: {COLORS["bg_elev"]};
        border: 1px solid {COLORS["border"]};
        min-height: 150px;
    }}

    hr {{
        border-color: {COLORS["border"]} !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


SPARKS = [
    {"left": "4%",  "size": 4, "dur": 16, "delay": 0,  "color": COLORS["amber"]},
    {"left": "12%", "size": 3, "dur": 21, "delay": 3,  "color": COLORS["cyan"]},
    {"left": "21%", "size": 5, "dur": 18, "delay": 7,  "color": COLORS["green"]},
    {"left": "33%", "size": 3, "dur": 24, "delay": 1,  "color": COLORS["amber"]},
    {"left": "44%", "size": 4, "dur": 19, "delay": 9,  "color": COLORS["cyan"]},
    {"left": "55%", "size": 3, "dur": 22, "delay": 4,  "color": COLORS["rose"]},
    {"left": "64%", "size": 5, "dur": 17, "delay": 11, "color": COLORS["green"]},
    {"left": "73%", "size": 3, "dur": 25, "delay": 2,  "color": COLORS["amber"]},
    {"left": "84%", "size": 4, "dur": 20, "delay": 6,  "color": COLORS["cyan"]},
    {"left": "93%", "size": 3, "dur": 23, "delay": 13, "color": COLORS["green"]},
]

_spark_html = "".join(
    f'<span class="bg-spark" style="left:{s["left"]}; width:{s["size"]}px; '
    f'height:{s["size"]}px; background:{s["color"]}; '
    f'animation-duration:{s["dur"]}s; animation-delay:{s["delay"]}s;"></span>'
    for s in SPARKS
)

st.markdown(
    f"""
    <div class="bg-fx">
        <div class="bg-grid"></div>
        <div class="bg-sweep"></div>
        {_spark_html}
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# LOAD DATA
# ==================================================
# BASE_DIR always points to the folder app.py lives in, so this
# works the same way whether it's run locally on Windows
# (E:\IRCTC-Data-Analysis) or on Streamlit Cloud after deployment.
# It never depends on a hard-coded Windows path.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "cleaned_uts_data.csv"
)

# The columns every part of this dashboard relies on. If the CSV
# doesn't have one of these, we stop with a clear message instead
# of letting the app crash later with a confusing KeyError.
REQUIRED_COLUMNS = [
    "From_Station",
    "To_Station",
    "Railway_Line",
    "Booking_Mode",
    "Hour",
    "Total_Fare",
]

if not os.path.exists(DATA_PATH):
    st.error(
        "❌ Dataset not found.\n\n"
        f"Expected the cleaned dataset at:\n`{DATA_PATH}`\n\n"
        "Make sure `cleaned_uts_data.csv` exists inside the `data/` "
        "folder next to `app.py`."
    )
    st.stop()

try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    st.error(
        "❌ The dataset file was found, but could not be read as a CSV.\n\n"
        f"Error details: {e}"
    )
    st.stop()

missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

if missing_columns:
    st.error(
        "❌ The dataset is missing required column(s):\n\n"
        + "\n".join(f"- `{col}`" for col in missing_columns)
        + "\n\nPlease check `cleaned_uts_data.csv` and make sure these "
        "columns exist with these exact names."
    )
    st.stop()

if df.empty:
    st.error("❌ The dataset was loaded but contains no rows.")
    st.stop()


# ==================================================
# PREPARE DATA (safe cleaning, mirrors the checks the
# brief asked for — no values are invented, rows that
# genuinely can't be used are dropped and reported)
# ==================================================

rows_before_cleaning = len(df)

# Strip stray whitespace from the text fields used for filtering
# and grouping, so " Mobile" and "Mobile" aren't treated as two
# different booking modes.
for text_col in ["From_Station", "To_Station", "Railway_Line", "Booking_Mode"]:
    df[text_col] = df[text_col].astype(str).str.strip()
    df[text_col] = df[text_col].replace({"nan": pd.NA, "": pd.NA})

# Hour must be a whole number from 0-23. Anything that isn't a
# valid number, or falls outside that range, is dropped rather
# than guessed at.
df["Hour"] = pd.to_numeric(df["Hour"], errors="coerce")
df = df[df["Hour"].notna()]
df["Hour"] = df["Hour"].astype(int)
df = df[(df["Hour"] >= 0) & (df["Hour"] <= 23)]

# Total_Fare must be a usable number. Negative or non-numeric
# fares are dropped rather than replaced with a made-up value.
df["Total_Fare"] = pd.to_numeric(df["Total_Fare"], errors="coerce")
df = df[df["Total_Fare"].notna()]
df = df[df["Total_Fare"] >= 0]

# A row with no station, railway line, or booking mode can't be
# analyzed meaningfully by this dashboard, so it's dropped too.
df = df.dropna(subset=["From_Station", "To_Station", "Railway_Line", "Booking_Mode"])

rows_after_cleaning = len(df)
rows_dropped = rows_before_cleaning - rows_after_cleaning

if df.empty:
    st.error(
        "❌ After cleaning, no valid rows remained. "
        "Please check that `Hour` (0-23) and `Total_Fare` (numeric) "
        "contain usable values in the dataset."
    )
    st.stop()

if "Route" not in df.columns:

    df["Route"] = (
        df["From_Station"].astype(str)
        + " → "
        + df["To_Station"].astype(str)
    )


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🚆 IRCTC Analytics")

    st.markdown("---")

    st.subheader("📌 Project")

    st.write(
        """
        **IRCTC UTS Ticketing & Passenger Flow Analysis**

        An interactive data analytics dashboard
        for exploring railway ticketing patterns.
        """
    )

    st.markdown("---")

    # --------------------------------------------------
    # FILTERS
    # --------------------------------------------------

    st.subheader("🔎 Dashboard Filters")

    railway_lines = ["All"] + sorted(
        df["Railway_Line"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_line = st.selectbox(
        "🚆 Railway Line",
        railway_lines
    )


    booking_modes = ["All"] + sorted(
        df["Booking_Mode"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_mode = st.selectbox(
        "🎫 Booking Mode",
        booking_modes
    )


    min_hour = int(df["Hour"].min())
    max_hour = int(df["Hour"].max())


    selected_hours = st.slider(
        "🕐 Travel Hour",
        min_value=min_hour,
        max_value=max_hour,
        value=(min_hour, max_hour)
    )


    st.markdown("---")

    st.subheader("🛠 Technologies")

    st.write(
        """
        Python  
        Pandas  
        MySQL  
        SQL  
        Plotly  
        Streamlit
        """
    )


    st.markdown("---")

    st.subheader("📊 Dataset")

    st.write(
        f"""
        **Records:** {len(df):,}

        **Stations:** {
            pd.concat(
                [
                    df["From_Station"],
                    df["To_Station"]
                ]
            ).nunique()
        }

        **Routes:** {df["Route"].nunique()}
        """
    )


    st.markdown("---")

    st.caption(
        "IRCTC UTS Ticketing & Passenger Flow Analysis"
    )


# ==================================================
# APPLY FILTERS
# ==================================================

filtered_df = df.copy()


if selected_line != "All":

    filtered_df = filtered_df[
        filtered_df["Railway_Line"].astype(str)
        == selected_line
    ]


if selected_mode != "All":

    filtered_df = filtered_df[
        filtered_df["Booking_Mode"].astype(str)
        == selected_mode
    ]


filtered_df = filtered_df[
    (filtered_df["Hour"] >= selected_hours[0])
    & (filtered_df["Hour"] <= selected_hours[1])
]


# ==================================================
# HERO HEADER
# ==================================================

total_records_all = len(df)
total_stations_all = pd.concat([df["From_Station"], df["To_Station"]]).nunique()
total_routes_all = df["Route"].nunique()

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-live"><span class="hero-dot"></span> LIVE ANALYTICS</div>
        <div class="hero-title">🚆 IRCTC Analytics</div>
        <div class="hero-sub">
            Passenger flow &amp; ticketing intelligence — explore railway demand,
            booking behavior, travel-hour patterns, routes, and revenue across
            the unreserved ticketing (UTS) network.
        </div>
        <div class="hero-track"></div>
        <div class="stat-strip">
            <div class="stat-tile">
                <div class="stat-value">{total_records_all:,}</div>
                <div class="stat-label">RECORDS</div>
            </div>
            <div class="stat-tile">
                <div class="stat-value">{total_stations_all:,}</div>
                <div class="stat-label">STATIONS</div>
            </div>
            <div class="stat-tile">
                <div class="stat-value">{total_routes_all:,}</div>
                <div class="stat-label">ROUTES</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.info(
    f"Showing {len(filtered_df):,} records based on the selected filters."
)

if rows_dropped > 0:
    st.caption(
        f"ℹ️ {rows_dropped:,} row(s) were excluded during data cleaning "
        "(invalid/missing Hour, Total_Fare, station, railway line, or "
        f"booking mode values). {rows_after_cleaning:,} valid rows remain."
    )


# ==================================================
# PROJECT OVERVIEW
# ==================================================

with st.expander("📖 Project Overview", expanded=False):

    overview1, overview2 = st.columns(2)


    with overview1:

        st.markdown(
            """
            ### 🎯 Objective

            The objective of this project is to analyze
            railway ticketing data and identify meaningful
            patterns in passenger movement, booking behavior,
            travel hours, routes, and revenue.

            ### ❓ Key Questions

            • When are passenger bookings highest?

            • Which routes have the highest booking volume?

            • Which booking channel is used most frequently?

            • Which railway lines generate the most revenue?

            • How does passenger activity vary across
              different filters?
            """
        )


    with overview2:

        st.markdown(
            """
            ### 🔄 Analysis Methodology

            **1. Data Collection**

            Railway ticketing data was collected and
            prepared for analysis.

            **2. Data Cleaning**

            Missing, inconsistent, and unnecessary
            values were processed using Pandas.

            **3. Data Transformation**

            Important analytical fields such as
            travel hour and route were prepared.

            **4. Analysis**

            Python, Pandas, and SQL concepts were used
            to identify passenger and revenue patterns.

            **5. Visualization**

            Interactive charts were created using
            Plotly and Streamlit.
            """
        )


# ==================================================
# KPI METRICS
# ==================================================

total_bookings = len(filtered_df)

total_revenue = filtered_df["Total_Fare"].sum()

unique_routes = filtered_df["Route"].nunique()

unique_stations = pd.concat(
    [
        filtered_df["From_Station"],
        filtered_df["To_Station"]
    ]
).nunique()


def kpi_card(label, value):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("🎫 TOTAL BOOKINGS", f"{total_bookings:,}")

with col2:
    kpi_card("💰 TOTAL REVENUE", f"₹{total_revenue:,.0f}")

with col3:
    kpi_card("🚉 UNIQUE ROUTES", f"{unique_routes:,}")

with col4:
    kpi_card("📍 STATIONS", f"{unique_stations:,}")


st.markdown("---")


# ==================================================
# EMPTY DATA CHECK
# ==================================================

if filtered_df.empty:

    st.warning(
        "No records match the selected filters. "
        "Please change the filters in the sidebar."
    )

    st.stop()


# ==================================================
# KEY INSIGHTS
# ==================================================

st.markdown('<div class="section-heading">💡 Key Insights</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="section-description">'
    'Automatically generated insights based on the current filters.'
    '</div>',
    unsafe_allow_html=True
)


peak_hour = (
    filtered_df["Hour"]
    .value_counts()
    .idxmax()
)


top_route = (
    filtered_df["Route"]
    .value_counts()
    .idxmax()
)


top_booking_mode = (
    filtered_df["Booking_Mode"]
    .value_counts()
    .idxmax()
)


top_railway_line = (
    filtered_df
    .groupby("Railway_Line")["Total_Fare"]
    .sum()
    .idxmax()
)


def insight_box(accent, label, value):
    st.markdown(
        f"""
        <div class="insight-box" style="--accent: {accent};">
            <div class="insight-label">{label}</div>
            <div class="insight-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


insight1, insight2 = st.columns(2)

with insight1:
    insight_box(COLORS["amber"], "🕐 PEAK TRAVEL HOUR",
                f"Highest booking volume occurs around <b>{peak_hour}:00</b>.")
    insight_box(COLORS["cyan"], "🚉 BUSIEST ROUTE",
                f"<b>{top_route}</b> has the highest number of recorded bookings.")

with insight2:
    insight_box(COLORS["green"], "🎫 MOST USED BOOKING MODE",
                f"<b>{top_booking_mode}</b> is the most frequently used booking channel.")
    insight_box(COLORS["rose"], "🚆 HIGHEST REVENUE LINE",
                f"<b>{top_railway_line}</b> generates the highest total fare revenue.")


st.markdown("---")


# ==================================================
# PEAK TRAVEL HOURS
# ==================================================

st.markdown('<div class="section-heading">🕐 Peak Travel Hours</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="section-description">'
    'Passenger booking volume by hour of the day.'
    '</div>',
    unsafe_allow_html=True
)


hourly_bookings = (
    filtered_df["Hour"]
    .value_counts()
    .sort_index()
    .reset_index()
)


hourly_bookings.columns = [
    "Hour",
    "Bookings"
]


fig_hours = px.bar(
    hourly_bookings,
    x="Hour",
    y="Bookings",
    title="Hourly Passenger Booking Volume",
    labels={
        "Hour": "Hour of Day",
        "Bookings": "Bookings"
    },
    color_discrete_sequence=[COLORS["amber"]],
)


fig_hours.update_layout(
    xaxis=dict(dtick=1),
)

apply_plotly_theme(fig_hours, height=450)

render_animated_chart(fig_hours, "hourly_chart", value_key="y", height=450)


# ==================================================
# TOP ROUTES
# ==================================================

st.markdown('<div class="section-heading">🚉 Top 10 Busiest Routes</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="section-description">'
    'Routes with the highest number of recorded bookings.'
    '</div>',
    unsafe_allow_html=True
)


top_routes = (
    filtered_df["Route"]
    .value_counts()
    .head(10)
    .reset_index()
)


top_routes.columns = [
    "Route",
    "Bookings"
]


fig_routes = px.bar(
    top_routes.sort_values("Bookings"),
    x="Bookings",
    y="Route",
    orientation="h",
    title="Top 10 Busiest Commuter Routes",
    labels={
        "Bookings": "Bookings",
        "Route": "Route"
    },
    color_discrete_sequence=[COLORS["cyan"]],
)

apply_plotly_theme(fig_routes, height=500)

render_animated_chart(fig_routes, "routes_chart", value_key="x", height=500)


# ==================================================
# BOOKING MODE + REVENUE
# ==================================================

col1, col2 = st.columns(2)


# --------------------------------------------------
# BOOKING MODE
# --------------------------------------------------

with col1:

    st.markdown('<div class="section-heading">🎫 Booking Mode</div>', unsafe_allow_html=True)

    booking_mode = (
        filtered_df["Booking_Mode"]
        .value_counts()
        .reset_index()
    )


    booking_mode.columns = [
        "Booking Mode",
        "Bookings"
    ]


    fig_booking = px.pie(
        booking_mode,
        names="Booking Mode",
        values="Bookings",
        hole=0.55,
        title="Booking Channel Distribution",
        color_discrete_sequence=CHART_SEQUENCE,
    )

    fig_booking.update_traces(
        textfont=dict(color=COLORS["text"]),
        marker=dict(line=dict(color=COLORS["bg_elev"], width=2)),
    )

    apply_plotly_theme(fig_booking, height=420)

    render_animated_chart(fig_booking, "booking_pie", value_key="values", height=420)


# --------------------------------------------------
# RAILWAY REVENUE
# --------------------------------------------------

with col2:

    st.markdown('<div class="section-heading">🚆 Railway Line Revenue</div>', unsafe_allow_html=True)


    line_revenue = (
        filtered_df
        .groupby("Railway_Line")["Total_Fare"]
        .sum()
        .reset_index()
        .sort_values(
            "Total_Fare",
            ascending=False
        )
    )


    fig_revenue = px.bar(
        line_revenue,
        x="Railway_Line",
        y="Total_Fare",
        title="Revenue by Railway Line",
        labels={
            "Railway_Line": "Railway Line",
            "Total_Fare": "Revenue (₹)"
        },
        color_discrete_sequence=[COLORS["green"]],
    )

    apply_plotly_theme(fig_revenue, height=420)

    render_animated_chart(fig_revenue, "revenue_chart", value_key="y", height=420)


# ==================================================
# ROUTE ANALYTICS
# ==================================================

st.markdown("---")

st.markdown('<div class="section-heading">🔍 Route Analytics</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="section-description">'
    'Pick a route to see its own bookings, revenue, and activity pattern.'
    '</div>',
    unsafe_allow_html=True
)

# Routes available under the CURRENT sidebar filters. filtered_df can
# never be empty here — the empty-data check above already stopped
# the app earlier if it were — so this list always has at least one
# route and the selectbox below can never be empty.
available_routes = sorted(filtered_df["Route"].dropna().unique().tolist())

selected_route = st.selectbox(
    "🚉 Select a Route",
    available_routes,
)

route_df = filtered_df[filtered_df["Route"] == selected_route]

if route_df.empty:
    # Defensive fallback only — with the current dropdown this can't
    # actually happen, since selected_route always comes from
    # filtered_df itself. Kept in case the dropdown logic changes later.
    st.warning("No records found for the selected route.")
else:
    route_bookings = len(route_df)
    route_revenue = route_df["Total_Fare"].sum()
    route_avg_fare = route_df["Total_Fare"].mean()
    route_top_mode = route_df["Booking_Mode"].value_counts().idxmax()

    rcol1, rcol2, rcol3, rcol4 = st.columns(4)

    with rcol1:
        kpi_card("🎫 BOOKINGS", f"{route_bookings:,}")

    with rcol2:
        kpi_card("💰 REVENUE", f"₹{route_revenue:,.0f}")

    with rcol3:
        kpi_card("📊 AVG FARE", f"₹{route_avg_fare:,.0f}")

    with rcol4:
        kpi_card("🎫 TOP MODE", route_top_mode)

    route_hourly = (
        route_df["Hour"]
        .value_counts()
        .sort_index()
        .reset_index()
    )
    route_hourly.columns = ["Hour", "Bookings"]

    fig_route_hourly = px.bar(
        route_hourly,
        x="Hour",
        y="Bookings",
        title=f"Hourly Booking Activity — {selected_route}",
        labels={"Hour": "Hour of Day", "Bookings": "Bookings"},
        color_discrete_sequence=[COLORS["amber"]],
    )
    fig_route_hourly.update_layout(xaxis=dict(dtick=1))
    apply_plotly_theme(fig_route_hourly, height=380)
    render_animated_chart(fig_route_hourly, "route_hourly_chart", value_key="y", height=380)


# ==================================================
# DOWNLOAD FILTERED DATA
# ==================================================

st.markdown("---")

st.markdown('<div class="section-heading">⬇️ Download Filtered Data</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="section-description">'
    'Download exactly the records currently selected by the sidebar filters.'
    '</div>',
    unsafe_allow_html=True
)

st.download_button(
    label="⬇️ Download Filtered Data (CSV)",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="irctc_filtered_data.csv",
    mime="text/csv",
)


# ==================================================
# DATASET PREVIEW
# ==================================================

st.markdown("---")

st.markdown('<div class="section-heading">📋 Dataset Preview</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="section-description">'
    'Explore the records currently selected by the dashboard filters.'
    '</div>',
    unsafe_allow_html=True
)


st.dataframe(
    filtered_df.head(100),
    use_container_width=True,
    height=400
)


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "IRCTC UTS Ticketing & Passenger Flow Analysis • "
    "Built with Python, Pandas, Plotly & Streamlit"
)
