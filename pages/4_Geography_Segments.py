import pandas as pd
import plotly.express as px
import streamlit as st

from common import (
    page_config,
    inject_css,
    sidebar_nav,
    load_data,
)


# =========================================================
# PAGE SETUP
# =========================================================
page_config("Geography & Segments")
inject_css()
sidebar_nav()


# =========================================================
# PAGE-SPECIFIC PROFESSIONAL DESIGN
# =========================================================
st.markdown(
    """
<style>
/* ---------- Main canvas ---------- */
.block-container {
    max-width: none !important;
    padding-top: 0.10rem !important;
    padding-left: 1.35rem !important;
    padding-right: 1.35rem !important;
    padding-bottom: 1.2rem !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 92% 2%, rgba(43,109,232,.055), transparent 28%),
        linear-gradient(180deg, #F7F9FC 0%, #F3F6FA 100%) !important;
}

header[data-testid="stHeader"] {
    background: rgba(247,249,252,.92) !important;
}

/* ---------- Narrow sidebar + moving brand ---------- */
[data-testid="stSidebar"] {
    width: 240px !important;
    min-width: 240px !important;
    max-width: 240px !important;
}

[data-testid="stSidebar"] > div:first-child {
    width: 240px !important;
    min-width: 240px !important;
    max-width: 240px !important;
}

[data-testid="stSidebarUserContent"] {
    padding: 0 .90rem 0 .90rem !important;
    margin-top: -26px !important;
}

[data-testid="stSidebar"] .brand-wrap {
    position: relative;
    overflow: hidden;
    transform: translateY(-10px);
    margin-bottom: .45rem !important;
    padding: .05rem 0 .16rem .68rem !important;
    border-left: 4px solid #F0B44D;
}

[data-testid="stSidebar"] .brand-name,
[data-testid="stSidebar"] .brand-sub {
    width: max-content;
    max-width: none !important;
    white-space: nowrap;
    display: block;
    animation: geoBrandMotion 3.8s ease-in-out infinite alternate;
}

[data-testid="stSidebar"] .brand-sub {
    animation-delay: .18s;
    color: #A9C9EF !important;
    font-size: .72rem !important;
    line-height: 1.35 !important;
}

@keyframes geoBrandMotion {
    from { transform: translateX(-6px); }
    to   { transform: translateX(24px); }
}

[data-testid="stSidebar"] .stPageLink a {
    padding: .56rem .62rem !important;
    margin-bottom: .14rem !important;
    font-size: .90rem !important;
}

/* ---------- Moving page title ---------- */
.geo-header {
    transform: translateY(-13px);
    margin-bottom: -8px;
}

.geo-eyebrow {
    color: #2B6DE8;
    font-size: .67rem;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
    margin-bottom: .05rem;
}

.geo-title-row {
    position: relative;
    width: 100%;
    padding-right: 10.8rem;
}

.geo-title-wrap {
    position: relative;
    width: 100%;
    height: 1.72rem;
    overflow: hidden;
    white-space: nowrap;
}

.geo-title {
    position: absolute;
    top: 0;
    width: max-content;
    color: #0F2A45;
    font-size: 1.28rem;
    font-weight: 850;
    letter-spacing: -.02em;
    line-height: 1.02;
    white-space: nowrap;
    animation: geoTitleShuttle 6.3s linear infinite alternate;
}

@keyframes geoTitleShuttle {
    0% {
        left: 0%;
        transform: translateX(-105%);
    }
    100% {
        left: 100%;
        transform: translateX(4%);
    }
}

.geo-live {
    position: absolute;
    right: 0;
    top: 0;
    padding: .38rem .64rem;
    border-radius: 999px;
    background: #EAF8F0;
    color: #17784A;
    border: 1px solid #C6EBD6;
    font-size: .69rem;
    font-weight: 800;
}

.geo-subtitle {
    color: #71839A;
    font-size: .86rem;
    margin-top: .02rem;
}

.geo-accent {
    height: 3px;
    margin-top: .42rem;
    border-radius: 999px;
    background: linear-gradient(
        90deg,
        #235FC4 0%,
        #5591F4 38%,
        rgba(85,145,244,.14) 72%,
        rgba(85,145,244,0) 100%
    );
}

/* ---------- Filters ---------- */
.filter-panel-title {
    color: #0F2A45;
    font-size: 1.0rem;
    font-weight: 850;
    margin: 0 0 .18rem 0;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stDateInput"] label {
    color: #294766 !important;
    font-size: .73rem !important;
    font-weight: 750 !important;
}

div[data-baseweb="select"] > div,
div[data-testid="stDateInput"] input {
    min-height: 2.60rem !important;
    background: #FFFFFF !important;
    border: 1px solid #DFE7F0 !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 8px rgba(15,42,69,.025);
}

/* ---------- KPI cards ---------- */
.geo-kpi {
    position: relative;
    overflow: hidden;
    min-height: 94px;
    border-radius: 14px;
    padding: .64rem .72rem .60rem .72rem;
    background: linear-gradient(145deg, #FFF 0%, var(--wash) 100%);
    border: 1px solid var(--border);
    box-shadow: 0 6px 18px rgba(15,42,69,.045);
    animation: geoFloat 2.15s ease-in-out infinite;
}

.geo-kpi::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 0;
    width: 4px;
    background: linear-gradient(180deg, var(--accent), var(--accent2));
}

.geo-kpi::after {
    content: "";
    position: absolute;
    width: 82px;
    height: 82px;
    border-radius: 50%;
    right: -32px;
    top: -34px;
    background: radial-gradient(circle, var(--bubble) 0%, rgba(255,255,255,0) 72%);
}

.geo-kpi .icon {
    position: relative;
    z-index: 2;
    width: 27px;
    height: 27px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--iconbg);
    color: var(--accent);
    border: 1px solid var(--border);
    font-size: 13px;
    font-weight: 900;
    margin-bottom: .30rem;
}

.geo-kpi .label {
    position: relative;
    z-index: 2;
    color: #60758C;
    font-size: .66rem;
    font-weight: 850;
    white-space: nowrap;
}

.geo-kpi .value {
    position: relative;
    z-index: 2;
    color: #0F2A45;
    font-size: 1.72rem;
    font-weight: 900;
    line-height: 1;
    margin-top: .18rem;
}

.geo-kpi .sub {
    position: relative;
    z-index: 2;
    color: #8293A8;
    font-size: .60rem;
    margin-top: .17rem;
}

.geo-kpi .mini-line {
    position: absolute;
    left: .72rem;
    right: .72rem;
    bottom: .36rem;
    height: 2px;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: .18;
}

@keyframes geoFloat {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-5px); }
}

.kpi-blue {
    --accent:#2563EB; --accent2:#60A5FA; --wash:#F2F7FF;
    --border:#D7E5FF; --bubble:#DCE9FF; --iconbg:#EAF2FF;
}
.kpi-cyan {
    --accent:#0891B2; --accent2:#22D3EE; --wash:#F0FBFD;
    --border:#D2F0F6; --bubble:#D8F5FA; --iconbg:#E6F9FC;
}
.kpi-violet {
    --accent:#7C3AED; --accent2:#A78BFA; --wash:#F7F3FF;
    --border:#E6DBFF; --bubble:#E9DEFF; --iconbg:#F0E9FF;
}
.kpi-teal {
    --accent:#0F9F8F; --accent2:#2DD4BF; --wash:#F0FBF8;
    --border:#D4F2EC; --bubble:#DAF6F0; --iconbg:#E7F9F5;
}
.kpi-amber {
    --accent:#D98B16; --accent2:#FBBF24; --wash:#FFF9EE;
    --border:#F6E6C4; --bubble:#FFF0CF; --iconbg:#FFF5DF;
}
.kpi-green {
    --accent:#238A57; --accent2:#4ADE80; --wash:#F2FAF5;
    --border:#D6EFDF; --bubble:#DCF4E4; --iconbg:#EAF8EF;
}

/* ---------- Card styling ---------- */
.card-title {
    color: #0F2A45;
    font-size: 1.02rem;
    font-weight: 850;
    margin-bottom: .05rem;
}

.card-subtitle {
    color: #7D8FA5;
    font-size: .74rem;
    margin-bottom: .30rem;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid #DFE7F0 !important;
    border-radius: 14px !important;
    box-shadow: 0 6px 20px rgba(15,42,69,.035);
}

/* ---------- Insight ---------- */
.geo-insight {
    padding: .70rem .76rem;
    border-radius: 10px;
    border: 1px solid #DFE7F0;
    background: #FFFFFF;
    box-shadow: 0 4px 12px rgba(15,42,69,.025);
    margin-bottom: .48rem;
}

.geo-insight .label {
    font-size: .64rem;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: .04em;
    color: #74879D;
}

.geo-insight .value {
    font-size: .96rem;
    font-weight: 900;
    color: #0F2A45;
    margin-top: .12rem;
}

.geo-insight .note {
    color: #7E90A6;
    font-size: .68rem;
    line-height: 1.42;
    margin-top: .18rem;
}

.geo-action {
    margin-top: .25rem;
    padding: .68rem .74rem;
    border-radius: 10px;
    background: linear-gradient(90deg, #EFF6FF 0%, #FBFDFF 100%);
    border: 1px solid #D9E7FA;
    border-left: 4px solid #2B6DE8;
}

.geo-action.teal {
    background: linear-gradient(90deg, #EFFBF8 0%, #FBFEFD 100%);
    border-color: #D6EFEA;
    border-left-color: #159E8C;
}

.geo-action.violet {
    background: linear-gradient(90deg, #F6F2FF 0%, #FCFAFF 100%);
    border-color: #E6DCFF;
    border-left-color: #7C3AED;
}

.geo-action.amber {
    background: linear-gradient(90deg, #FFF8EC 0%, #FFFDFB 100%);
    border-color: #F2E0BE;
    border-left-color: #D98B16;
}

.geo-action .title {
    color: #173A61;
    font-size: .69rem;
    font-weight: 850;
}

.geo-action .body {
    color: #6C7E91;
    font-size: .70rem;
    line-height: 1.42;
    margin-top: .18rem;
}

/* ---------- Table ---------- */
.table-heading {
    color: #0F2A45;
    font-size: 1.02rem;
    font-weight: 850;
    margin-top: .15rem;
}

.table-subheading {
    color: #7D8FA5;
    font-size: .74rem;
    margin-bottom: .35rem;
}

[data-testid="stDataFrame"] {
    border: 1px solid #DFE7F0 !important;
    border-radius: 12px !important;
    overflow: hidden;
    box-shadow: 0 5px 16px rgba(15,42,69,.03);
}

[data-testid="stVerticalBlock"] {
    gap: .55rem;
}

@media (prefers-reduced-motion: reduce) {
    .geo-title,
    .geo-kpi,
    [data-testid="stSidebar"] .brand-name,
    [data-testid="stSidebar"] .brand-sub {
        animation: none !important;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HELPERS
# =========================================================
def geo_kpi(label, value, subtitle, icon, css_class):
    st.markdown(
        (
            f'<div class="geo-kpi {css_class}">'
            f'<div class="icon">{icon}</div>'
            f'<div class="label">{label}</div>'
            f'<div class="value">{value}</div>'
            f'<div class="sub">{subtitle}</div>'
            f'<div class="mini-line"></div>'
            f'</div>'
        ),
        unsafe_allow_html=True,
    )


def card_header(title, subtitle=""):
    st.markdown(
        f'<div class="card-title">{title}</div>'
        f'<div class="card-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )


def geo_insight(label, value, note):
    st.markdown(
        (
            '<div class="geo-insight">'
            f'<div class="label">{label}</div>'
            f'<div class="value">{value}</div>'
            f'<div class="note">{note}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def action_note(title, body, tone="blue"):
    tone_class = "" if tone == "blue" else tone
    st.markdown(
        (
            f'<div class="geo-action {tone_class}">'
            f'<div class="title">{title}</div>'
            f'<div class="body">{body}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def clean_chart(fig, height=235, legend=True):
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=10, t=10, b=8),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial, sans-serif",
            size=10,
            color="#61758C",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=9),
        ),
        showlegend=legend,
        bargap=.25,
        hoverlabel=dict(
            bgcolor="#0F2A45",
            font_color="#FFFFFF",
            bordercolor="#0F2A45",
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#E6EDF5",
        tickfont=dict(size=9, color="#71839A"),
        title_font=dict(size=10, color="#61758C"),
        automargin=True,
    )

    fig.update_yaxes(
        gridcolor="#E9EEF5",
        zeroline=False,
        linecolor="#E6EDF5",
        tickfont=dict(size=9, color="#71839A"),
        title_font=dict(size=10, color="#61758C"),
        automargin=True,
    )

    return fig


CHART_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
    "scrollZoom": False,
    "displaylogo": False,
}


# =========================================================
# LOAD DATA
# =========================================================
df = load_data()


# =========================================================
# HEADER
# =========================================================
header_html = (
    '<div class="geo-header">'
    '<div class="geo-eyebrow">PGDM Outreach Intelligence</div>'
    '<div class="geo-title-row">'
    '<div class="geo-title-wrap">'
    '<div class="geo-title">Geography &amp; Segments</div>'
    '</div>'
    '<div class="geo-live">● LIVE GOOGLE SHEET</div>'
    '</div>'
    '<div class="geo-subtitle">'
    'State, city and audience coverage intelligence for outreach planning.'
    '</div>'
    '<div class="geo-accent"></div>'
    '</div>'
)

st.markdown(
    header_html,
    unsafe_allow_html=True,
)


# =========================================================
# FILTERS
# =========================================================
st.markdown(
    '<div class="filter-panel-title">Filters</div>',
    unsafe_allow_html=True,
)

f1, f2, f3, f4, f5, f6, f7 = st.columns(
    [1.0, 1.05, 1.08, 1.0, 1.0, .92, 1.18],
    gap="small",
)

with f1:
    campus_values = (
        ["All"] + sorted(df["Campus"].dropna().unique().tolist())
        if "Campus" in df.columns else ["All"]
    )
    campus_filter = st.selectbox(
        "Campus",
        campus_values,
        key="geo_page_campus",
    )

with f2:
    activity_values = (
        ["All"] + sorted(df["Activity Type"].dropna().unique().tolist())
        if "Activity Type" in df.columns else ["All"]
    )
    activity_filter = st.selectbox(
        "Activity Type",
        activity_values,
        key="geo_page_activity",
    )

with f3:
    segment_values = (
        ["All"] + sorted(df["Target Segment"].dropna().unique().tolist())
        if "Target Segment" in df.columns else ["All"]
    )
    segment_filter = st.selectbox(
        "Target Segment",
        segment_values,
        key="geo_page_segment",
    )

with f4:
    owner_values = (
        ["All"] + sorted(df["Activity Owner"].dropna().unique().tolist())
        if "Activity Owner" in df.columns else ["All"]
    )
    owner_filter = st.selectbox(
        "Owner",
        owner_values,
        key="geo_page_owner",
    )

with f5:
    status_values = (
        ["All"] + sorted(df["Status"].dropna().unique().tolist())
        if "Status" in df.columns else ["All"]
    )
    status_filter = st.selectbox(
        "Status",
        status_values,
        key="geo_page_status",
    )

with f6:
    priority_values = (
        ["All"] + sorted(df["Priority"].dropna().unique().tolist())
        if "Priority" in df.columns else ["All"]
    )
    priority_filter = st.selectbox(
        "Priority",
        priority_values,
        key="geo_page_priority",
    )

date_range = None

with f7:
    if (
        "Activity Date" in df.columns
        and df["Activity Date"].notna().any()
    ):
        min_date = df["Activity Date"].min().date()
        max_date = df["Activity Date"].max().date()

        date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="geo_page_date",
        )
    else:
        st.text_input(
            "Date Range",
            value="",
            disabled=True,
            key="geo_page_date_text",
        )


# =========================================================
# APPLY FILTERS
# =========================================================
f = df.copy()

if campus_filter != "All" and "Campus" in f.columns:
    f = f[f["Campus"] == campus_filter]

if activity_filter != "All" and "Activity Type" in f.columns:
    f = f[f["Activity Type"] == activity_filter]

if segment_filter != "All" and "Target Segment" in f.columns:
    f = f[f["Target Segment"] == segment_filter]

if owner_filter != "All" and "Activity Owner" in f.columns:
    f = f[f["Activity Owner"] == owner_filter]

if status_filter != "All" and "Status" in f.columns:
    f = f[f["Status"] == status_filter]

if priority_filter != "All" and "Priority" in f.columns:
    f = f[f["Priority"] == priority_filter]

if (
    date_range
    and isinstance(date_range, (list, tuple))
    and len(date_range) == 2
    and "Activity Date" in f.columns
):
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)

    f = f[
        (f["Activity Date"] >= start_date)
        & (f["Activity Date"] < end_date)
    ]

if f.empty:
    st.warning(
        "Selected filters ke liye koi geography/segment data available nahi hai."
    )
    st.stop()


# =========================================================
# KPI CALCULATIONS
# =========================================================
states_count = (
    int(f["State"].dropna().nunique())
    if "State" in f.columns
    else 0
)

cities_count = (
    int(f["City"].dropna().nunique())
    if "City" in f.columns
    else 0
)

segments_count = (
    int(f["Target Segment"].dropna().nunique())
    if "Target Segment" in f.columns
    else 0
)

institutions_count = (
    int(f["Institution / Event Name"].dropna().nunique())
    if "Institution / Event Name" in f.columns
    else 0
)

total_activities = int(len(f))

participation_captured = (
    int(f["Participation Type"].notna().sum())
    if "Participation Type" in f.columns
    else 0
)

participation_rate = (
    round(participation_captured / len(f) * 100, 1)
    if len(f) > 0
    else 0
)


# =========================================================
# KPI ROW
# =========================================================
k1, k2, k3, k4, k5, k6 = st.columns(
    6,
    gap="small",
)

with k1:
    geo_kpi(
        "States Covered",
        f"{states_count:,}",
        "Unique states",
        "◇",
        "kpi-blue",
    )

with k2:
    geo_kpi(
        "Cities Covered",
        f"{cities_count:,}",
        "Unique cities",
        "⌖",
        "kpi-cyan",
    )

with k3:
    geo_kpi(
        "Target Segments",
        f"{segments_count:,}",
        "Audience categories",
        "◆",
        "kpi-violet",
    )

with k4:
    geo_kpi(
        "Institutions",
        f"{institutions_count:,}",
        "Unique institutions",
        "▦",
        "kpi-teal",
    )

with k5:
    geo_kpi(
        "Activities",
        f"{total_activities:,}",
        "Filtered outreach volume",
        "●",
        "kpi-amber",
    )

with k6:
    geo_kpi(
        "Participation Captured",
        f"{participation_rate:.1f}%",
        "Rows with participation type",
        "✓",
        "kpi-green",
    )


# =========================================================
# ROW 1 — STATE + GEOGRAPHY INTELLIGENCE
# =========================================================
left, right = st.columns(
    [2.25, 1.0],
    gap="medium",
)

state_df = pd.DataFrame()

if "State" in f.columns:
    state_df = (
        f["State"]
        .dropna()
        .value_counts()
        .rename_axis("State")
        .reset_index(name="Activities")
    )

with left:
    with st.container(border=True):
        card_header(
            "Activities by State",
            "Outreach activity concentration across states.",
        )

        if state_df.empty:
            st.info(
                "State data available nahi hai."
            )
        else:
            state_chart = (
                state_df.sort_values(
                    "Activities",
                    ascending=True,
                )
            )

            fig = px.bar(
                state_chart,
                x="Activities",
                y="State",
                orientation="h",
                text="Activities",
            )

            fig.update_traces(
                marker_color="#2468B4",
                textposition="outside",
                textfont=dict(size=9),
                marker_line_width=0,
            )

            fig.update_xaxes(
                title="Activities",
                rangemode="tozero",
                showticklabels=False,
                ticks="",
                showgrid=False,
                zeroline=False,
            )

            fig.update_yaxes(title="")

            st.plotly_chart(
                clean_chart(
                    fig,
                    245,
                    legend=False,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )

            top_state_row = (
                state_df.sort_values(
                    "Activities",
                    ascending=False,
                )
                .iloc[0]
            )

            state_share = (
                round(
                    int(top_state_row["Activities"])
                    / total_activities
                    * 100,
                    1,
                )
                if total_activities > 0
                else 0
            )

            action_note(
                "State Coverage Insight",
                (
                    f'{top_state_row["State"]} has the highest outreach '
                    f'concentration with {int(top_state_row["Activities"])} '
                    f'activities ({state_share}% of the selected outreach volume).'
                ),
                "blue",
            )


with right:
    with st.container(border=True):
        card_header(
            "Geography Intelligence",
            "Management-ready coverage summary.",
        )

        if not state_df.empty:
            top_state_row = (
                state_df.sort_values(
                    "Activities",
                    ascending=False,
                )
                .iloc[0]
            )

            geo_insight(
                "Top state",
                str(top_state_row["State"]),
                f'{int(top_state_row["Activities"])} outreach activities',
            )
        else:
            geo_insight(
                "Top state",
                "N/A",
                "State values are not available.",
            )

        if (
            "City" in f.columns
            and f["City"].notna().any()
        ):
            city_counts = (
                f["City"]
                .dropna()
                .value_counts()
            )

            geo_insight(
                "Top city",
                str(city_counts.index[0]),
                f'{int(city_counts.iloc[0])} outreach activities',
            )
        else:
            geo_insight(
                "Top city",
                "N/A",
                "City values are not available.",
            )

        if (
            "Target Segment" in f.columns
            and f["Target Segment"].notna().any()
        ):
            segment_counts = (
                f["Target Segment"]
                .dropna()
                .value_counts()
            )

            geo_insight(
                "Dominant segment",
                str(segment_counts.index[0]),
                f'{int(segment_counts.iloc[0])} outreach activities',
            )
        else:
            geo_insight(
                "Dominant segment",
                "N/A",
                "Target Segment values are not available.",
            )

        geo_insight(
            "Coverage footprint",
            f"{states_count} states / {cities_count} cities",
            f"{institutions_count} unique institutions in the selected view.",
        )


# =========================================================
# ROW 2 — CITY + SEGMENT
# =========================================================
c1, c2 = st.columns(
    2,
    gap="medium",
)

with c1:
    with st.container(border=True):
        card_header(
            "Activities by City",
            "City-level activity concentration.",
        )

        if (
            "City" not in f.columns
            or not f["City"].notna().any()
        ):
            st.info(
                "City data available nahi hai."
            )
        else:
            city_df = (
                f["City"]
                .dropna()
                .value_counts()
                .rename_axis("City")
                .reset_index(name="Activities")
                .sort_values("Activities")
            )

            fig = px.bar(
                city_df,
                x="Activities",
                y="City",
                orientation="h",
                text="Activities",
            )

            fig.update_traces(
                marker_color="#159E8C",
                textposition="outside",
                textfont=dict(size=9),
                marker_line_width=0,
            )

            fig.update_xaxes(
                title="Activities",
                rangemode="tozero",
                showticklabels=False,
                ticks="",
                showgrid=False,
                zeroline=False,
            )

            fig.update_yaxes(title="")

            st.plotly_chart(
                clean_chart(
                    fig,
                    235,
                    legend=False,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )

            top_city = (
                city_df.sort_values(
                    "Activities",
                    ascending=False,
                )
                .iloc[0]
            )

            city_share = (
                round(
                    int(top_city["Activities"])
                    / total_activities
                    * 100,
                    1,
                )
                if total_activities > 0
                else 0
            )

            action_note(
                "City Coverage Insight",
                (
                    f'{top_city["City"]} has the highest current activity '
                    f'concentration with {int(top_city["Activities"])} activities '
                    f'({city_share}% of the selected outreach volume).'
                ),
                "teal",
            )


with c2:
    with st.container(border=True):
        card_header(
            "Target Segment Mix",
            "Audience categories reached through outreach activities.",
        )

        if (
            "Target Segment" not in f.columns
            or not f["Target Segment"].notna().any()
        ):
            st.info(
                "Target Segment data available nahi hai."
            )
        else:
            segment_df = (
                f["Target Segment"]
                .dropna()
                .value_counts()
                .rename_axis("Target Segment")
                .reset_index(name="Activities")
                .sort_values("Activities")
            )

            fig = px.bar(
                segment_df,
                x="Activities",
                y="Target Segment",
                orientation="h",
                text="Activities",
            )

            fig.update_traces(
                marker_color="#7A56D8",
                textposition="outside",
                textfont=dict(size=9),
                marker_line_width=0,
            )

            fig.update_xaxes(
                title="Activities",
                rangemode="tozero",
                showticklabels=False,
                ticks="",
                showgrid=False,
                zeroline=False,
            )

            fig.update_yaxes(title="")

            st.plotly_chart(
                clean_chart(
                    fig,
                    235,
                    legend=False,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )

            dominant_segment = (
                segment_df.sort_values(
                    "Activities",
                    ascending=False,
                )
                .iloc[0]
            )

            segment_share = (
                round(
                    int(dominant_segment["Activities"])
                    / total_activities
                    * 100,
                    1,
                )
                if total_activities > 0
                else 0
            )

            action_note(
                "Segment Insight",
                (
                    f'{dominant_segment["Target Segment"]} is the dominant '
                    f'audience segment with {int(dominant_segment["Activities"])} '
                    f'activities ({segment_share}% of the selected mix). '
                    f'The current plan covers {segments_count} distinct segments.'
                ),
                "violet",
            )


# =========================================================
# ROW 3 — PARTICIPATION + CAMPUS GEOGRAPHY
# =========================================================
r1, r2 = st.columns(
    2,
    gap="medium",
)

with r1:
    with st.container(border=True):
        card_header(
            "Participation Type",
            "Participation format captured for outreach activities.",
        )

        if "Participation Type" not in f.columns:
            st.info(
                "Participation Type column available nahi hai."
            )
        else:
            participation_df = (
                f["Participation Type"]
                .fillna("Not Captured")
                .value_counts()
                .rename_axis("Participation Type")
                .reset_index(name="Activities")
                .sort_values("Activities")
            )

            colors = {
                "Not Captured": "#A4AFBD",
            }

            fig = px.bar(
                participation_df,
                x="Activities",
                y="Participation Type",
                orientation="h",
                text="Activities",
                color="Participation Type",
                color_discrete_map=colors,
            )

            # Any non-mapped categories get Plotly colors; override them for consistency
            fig.for_each_trace(
                lambda trace: trace.update(
                    marker_line_width=0,
                    textposition="outside",
                    textfont=dict(size=9),
                )
            )

            fig.update_xaxes(
                title="Activities",
                rangemode="tozero",
                showticklabels=False,
                ticks="",
                showgrid=False,
                zeroline=False,
            )

            fig.update_yaxes(title="")

            st.plotly_chart(
                clean_chart(
                    fig,
                    225,
                    legend=False,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )

            not_captured = int(
                f["Participation Type"]
                .isna()
                .sum()
            )

            dominant_participation = (
                participation_df.sort_values(
                    "Activities",
                    ascending=False,
                )
                .iloc[0]
            )

            action_note(
                "Participation Insight",
                (
                    f'{dominant_participation["Participation Type"]} is the most '
                    f'common participation category with '
                    f'{int(dominant_participation["Activities"])} activities. '
                    f'{not_captured} records currently have Participation Type missing.'
                ),
                "amber",
            )


with r2:
    with st.container(border=True):
        card_header(
            "Campus × State Coverage",
            "How each campus is distributed across outreach states.",
        )

        if not {
            "Campus",
            "State",
        }.issubset(f.columns):
            st.info(
                "Campus / State data available nahi hai."
            )
        else:
            campus_state = (
                f.dropna(
                    subset=[
                        "Campus",
                        "State",
                    ]
                )
                .groupby(
                    [
                        "Campus",
                        "State",
                    ]
                )
                .size()
                .reset_index(name="Activities")
            )

            if campus_state.empty:
                st.info(
                    "Campus-state coverage available nahi hai."
                )
            else:
                fig = px.bar(
                    campus_state,
                    x="Campus",
                    y="Activities",
                    color="State",
                    barmode="stack",
                    text="Activities",
                )

                fig.update_traces(
                    textposition="inside",
                    textfont=dict(size=8),
                    marker_line_width=0,
                )

                fig.update_xaxes(title="")
                fig.update_yaxes(
                    title="Activities",
                    rangemode="tozero",
                    showticklabels=False,
                    ticks="",
                    showgrid=False,
                    zeroline=False,
                )

                st.plotly_chart(
                    clean_chart(
                        fig,
                        225,
                        legend=True,
                    ),
                    width="stretch",
                    config=CHART_CONFIG,
                )

                state_per_campus = (
                    f.dropna(
                        subset=[
                            "Campus",
                            "State",
                        ]
                    )
                    .groupby("Campus")["State"]
                    .nunique()
                    .sort_values(
                        ascending=False
                    )
                )

                top_geo_campus = (
                    state_per_campus.index[0]
                )

                top_geo_states = int(
                    state_per_campus.iloc[0]
                )

                action_note(
                    "Campus Geography Insight",
                    (
                        f'{top_geo_campus} currently has the broadest state '
                        f'coverage with {top_geo_states} unique states in the selected view.'
                    ),
                    "blue",
                )


# =========================================================
# GEOGRAPHY SCORECARD
# =========================================================
st.markdown(
    '<div class="table-heading">Geography & Segment Scorecard</div>'
    '<div class="table-subheading">'
    'State/city activity view with institution and audience coverage.'
    '</div>',
    unsafe_allow_html=True,
)

score_group_cols = [
    col
    for col in [
        "State",
        "City",
    ]
    if col in f.columns
]

if score_group_cols:
    score_agg = {
        "Activities": (
            score_group_cols[0],
            "size",
        ),
    }

    if "Institution / Event Name" in f.columns:
        score_agg["Institutions"] = (
            "Institution / Event Name",
            "nunique",
        )

    if "Target Segment" in f.columns:
        score_agg["Segments"] = (
            "Target Segment",
            "nunique",
        )

    if "Planned Student Reach" in f.columns:
        score_agg["Planned_Reach"] = (
            "Planned Student Reach",
            lambda s: s.sum(min_count=1),
        )

    if "Actual Student Reach" in f.columns:
        score_agg["Actual_Reach"] = (
            "Actual Student Reach",
            lambda s: s.sum(min_count=1),
        )

    geo_score = (
        f.groupby(
            score_group_cols,
            dropna=False,
        )
        .agg(**score_agg)
        .reset_index()
    )

    geo_score = geo_score.rename(
        columns={
            "Planned_Reach": "Planned Reach",
            "Actual_Reach": "Actual Reach",
        }
    )

    display_cols = [
        "State",
        "City",
        "Activities",
        "Institutions",
        "Segments",
        "Planned Reach",
        "Actual Reach",
    ]

    display_cols = [
        col
        for col in display_cols
        if col in geo_score.columns
    ]

    st.dataframe(
        geo_score[display_cols].sort_values(
            [
                "Activities",
                "State",
                "City",
            ],
            ascending=[
                False,
                True,
                True,
            ],
        ),
        width="stretch",
        hide_index=True,
        height=260,
        row_height=30,
        column_config={
            "State": st.column_config.TextColumn(
                "State",
                width="medium",
            ),
            "City": st.column_config.TextColumn(
                "City",
                width="medium",
            ),
            "Activities": st.column_config.NumberColumn(
                "Activities",
                format="%d",
                width="small",
            ),
            "Institutions": st.column_config.NumberColumn(
                "Institutions",
                format="%d",
                width="small",
            ),
            "Segments": st.column_config.NumberColumn(
                "Segments",
                format="%d",
                width="small",
            ),
            "Planned Reach": st.column_config.NumberColumn(
                "Planned Reach",
                format="%d",
                width="small",
            ),
            "Actual Reach": st.column_config.NumberColumn(
                "Actual Reach",
                format="%d",
                width="small",
            ),
        },
    )


# =========================================================
# FINAL MANAGEMENT RECOMMENDATION
# =========================================================
if not state_df.empty and total_activities > 0:
    top_state_share = round(
        int(
            state_df.sort_values(
                "Activities",
                ascending=False,
            )
            .iloc[0]["Activities"]
        )
        / total_activities
        * 100,
        1,
    )
else:
    top_state_share = 0

if top_state_share >= 50:
    concentration_message = (
        f"Geographic concentration is high: the leading state accounts for "
        f"{top_state_share}% of selected outreach activity."
    )
else:
    concentration_message = (
        f"The leading state accounts for {top_state_share}% of selected outreach "
        f"activity, indicating a relatively distributed geography."
    )

action_note(
    "Geography & Segment Recommendation",
    (
        concentration_message
        + " Review state concentration together with city coverage, target-segment "
          "mix and institution depth. Participation Type completeness should also "
          "be improved where values are missing so future outreach format decisions "
          "can be based on reliable data."
    ),
    "blue",
)
