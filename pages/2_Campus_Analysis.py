import pandas as pd
import plotly.express as px
import streamlit as st

from common import (
    page_config,
    inject_css,
    sidebar_nav,
    load_data,
    CLOSED_STATUSES,
)


# =========================================================
# PAGE SETUP
# =========================================================
page_config("Campus Analysis")
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
    animation: campusBrandMotion 3.8s ease-in-out infinite alternate;
}

[data-testid="stSidebar"] .brand-sub {
    animation-delay: .18s;
    color: #A9C9EF !important;
    font-size: .72rem !important;
    line-height: 1.35 !important;
}

@keyframes campusBrandMotion {
    from { transform: translateX(-6px); }
    to   { transform: translateX(24px); }
}

[data-testid="stSidebar"] .stPageLink a {
    padding: .56rem .62rem !important;
    margin-bottom: .14rem !important;
    font-size: .90rem !important;
}

/* ---------- Moving page title ---------- */
.campus-header {
    transform: translateY(-13px);
    margin-bottom: -8px;
}

.campus-eyebrow {
    color: #2B6DE8;
    font-size: .67rem;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
    margin-bottom: .05rem;
}

.campus-title-row {
    position: relative;
    width: 100%;
    padding-right: 10.8rem;
}

.campus-title-wrap {
    position: relative;
    width: 100%;
    height: 1.72rem;
    overflow: hidden;
    white-space: nowrap;
}

.campus-title {
    position: absolute;
    top: 0;
    width: max-content;
    color: #0F2A45;
    font-size: 1.28rem;
    font-weight: 850;
    letter-spacing: -.02em;
    line-height: 1.02;
    white-space: nowrap;
    animation: campusTitleShuttle 6.3s linear infinite alternate;
}

@keyframes campusTitleShuttle {
    0% {
        left: 0%;
        transform: translateX(-105%);
    }
    100% {
        left: 100%;
        transform: translateX(4%);
    }
}

.campus-live {
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

.campus-subtitle {
    color: #71839A;
    font-size: .86rem;
    margin-top: .02rem;
}

.campus-accent {
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

/* ---------- Campus KPI cards ---------- */
.campus-kpi {
    position: relative;
    overflow: hidden;
    min-height: 94px;
    border-radius: 14px;
    padding: .64rem .72rem .60rem .72rem;
    background: linear-gradient(145deg, #FFF 0%, var(--wash) 100%);
    border: 1px solid var(--border);
    box-shadow: 0 6px 18px rgba(15,42,69,.045);
    animation: campusFloat 2.15s ease-in-out infinite;
}

.campus-kpi::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 0;
    width: 4px;
    background: linear-gradient(180deg, var(--accent), var(--accent2));
}

.campus-kpi::after {
    content: "";
    position: absolute;
    width: 82px;
    height: 82px;
    border-radius: 50%;
    right: -32px;
    top: -34px;
    background: radial-gradient(circle, var(--bubble) 0%, rgba(255,255,255,0) 72%);
}

.campus-kpi .icon {
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

.campus-kpi .label {
    position: relative;
    z-index: 2;
    color: #60758C;
    font-size: .66rem;
    font-weight: 850;
    white-space: nowrap;
}

.campus-kpi .value {
    position: relative;
    z-index: 2;
    color: #0F2A45;
    font-size: 1.72rem;
    font-weight: 900;
    line-height: 1;
    margin-top: .18rem;
}

.campus-kpi .sub {
    position: relative;
    z-index: 2;
    color: #8293A8;
    font-size: .60rem;
    margin-top: .17rem;
}

.campus-kpi .mini-line {
    position: absolute;
    left: .72rem;
    right: .72rem;
    bottom: .36rem;
    height: 2px;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: .18;
}

@keyframes campusFloat {
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

/* ---------- Section/card ---------- */
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
.campus-insight {
    padding: .70rem .76rem;
    border-radius: 10px;
    border: 1px solid #DFE7F0;
    background: #FFFFFF;
    box-shadow: 0 4px 12px rgba(15,42,69,.025);
    margin-bottom: .48rem;
}

.campus-insight .label {
    font-size: .64rem;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: .04em;
    color: #74879D;
}

.campus-insight .value {
    font-size: .96rem;
    font-weight: 900;
    color: #0F2A45;
    margin-top: .12rem;
}

.campus-insight .note {
    color: #7E90A6;
    font-size: .68rem;
    line-height: 1.42;
    margin-top: .18rem;
}

.campus-action {
    margin-top: .25rem;
    padding: .68rem .74rem;
    border-radius: 10px;
    background: linear-gradient(90deg, #EFF6FF 0%, #FBFDFF 100%);
    border: 1px solid #D9E7FA;
    border-left: 4px solid #2B6DE8;
}

.campus-action.teal {
    background: linear-gradient(90deg, #EFFBF8 0%, #FBFEFD 100%);
    border-color: #D6EFEA;
    border-left-color: #159E8C;
}

.campus-action.violet {
    background: linear-gradient(90deg, #F6F2FF 0%, #FCFAFF 100%);
    border-color: #E6DCFF;
    border-left-color: #7C3AED;
}

.campus-action.amber {
    background: linear-gradient(90deg, #FFF8EC 0%, #FFFDFB 100%);
    border-color: #F2E0BE;
    border-left-color: #D98B16;
}

.campus-action .title {
    color: #173A61;
    font-size: .69rem;
    font-weight: 850;
}

.campus-action .body {
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
    .campus-title,
    .campus-kpi,
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
def campus_kpi(label, value, subtitle, icon, css_class):
    st.markdown(
        (
            f'<div class="campus-kpi {css_class}">'
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


def campus_insight(label, value, note):
    st.markdown(
        (
            '<div class="campus-insight">'
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
            f'<div class="campus-action {tone_class}">'
            f'<div class="title">{title}</div>'
            f'<div class="body">{body}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def clean_chart(fig, height=245, legend=True):
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
    '<div class="campus-header">'
    '<div class="campus-eyebrow">PGDM Outreach Intelligence</div>'
    '<div class="campus-title-row">'
    '<div class="campus-title-wrap">'
    '<div class="campus-title">Campus Analysis</div>'
    '</div>'
    '<div class="campus-live">● LIVE GOOGLE SHEET</div>'
    '</div>'
    '<div class="campus-subtitle">'
    'Compare outreach volume, institution coverage, geography and reach across campuses.'
    '</div>'
    '<div class="campus-accent"></div>'
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
        key="campus_page_campus",
    )

with f2:
    activity_values = (
        ["All"] + sorted(df["Activity Type"].dropna().unique().tolist())
        if "Activity Type" in df.columns else ["All"]
    )
    activity_filter = st.selectbox(
        "Activity Type",
        activity_values,
        key="campus_page_activity",
    )

with f3:
    segment_values = (
        ["All"] + sorted(df["Target Segment"].dropna().unique().tolist())
        if "Target Segment" in df.columns else ["All"]
    )
    segment_filter = st.selectbox(
        "Target Segment",
        segment_values,
        key="campus_page_segment",
    )

with f4:
    owner_values = (
        ["All"] + sorted(df["Activity Owner"].dropna().unique().tolist())
        if "Activity Owner" in df.columns else ["All"]
    )
    owner_filter = st.selectbox(
        "Owner",
        owner_values,
        key="campus_page_owner",
    )

with f5:
    status_values = (
        ["All"] + sorted(df["Status"].dropna().unique().tolist())
        if "Status" in df.columns else ["All"]
    )
    status_filter = st.selectbox(
        "Status",
        status_values,
        key="campus_page_status",
    )

with f6:
    priority_values = (
        ["All"] + sorted(df["Priority"].dropna().unique().tolist())
        if "Priority" in df.columns else ["All"]
    )
    priority_filter = st.selectbox(
        "Priority",
        priority_values,
        key="campus_page_priority",
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
            key="campus_page_date",
        )
    else:
        st.text_input(
            "Date Range",
            value="",
            disabled=True,
            key="campus_page_date_text",
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
        "Selected filters ke liye koi campus outreach data available nahi hai."
    )
    st.stop()

if "Campus" not in f.columns:
    st.info("Campus column available nahi hai.")
    st.stop()


# =========================================================
# CAMPUS AGGREGATION — BLANK ACTUAL REACH REMAINS MISSING
# =========================================================
today = pd.Timestamp.today().normalize()

agg_dict = {
    "Activities": ("Campus", "size"),
}

if "Institution / Event Name" in f.columns:
    agg_dict["Institutions"] = (
        "Institution / Event Name",
        "nunique",
    )

if "City" in f.columns:
    agg_dict["Cities"] = (
        "City",
        "nunique",
    )

if "Planned Student Reach" in f.columns:
    agg_dict["Planned_Reach"] = (
        "Planned Student Reach",
        lambda s: s.sum(min_count=1),
    )

if "Actual Student Reach" in f.columns:
    agg_dict["Actual_Reach"] = (
        "Actual Student Reach",
        lambda s: s.sum(min_count=1),
    )

camp = (
    f.groupby("Campus", as_index=False)
    .agg(**agg_dict)
)

# Fill count metrics only; do not fill reach with zero.
for col in ["Activities", "Institutions", "Cities"]:
    if col in camp.columns:
        camp[col] = (
            pd.to_numeric(
                camp[col],
                errors="coerce",
            )
            .fillna(0)
            .astype(int)
        )

# Upcoming/open activities by campus
if "Activity Date" in f.columns:
    upcoming_mask = f["Activity Date"].ge(today)

    if "Status" in f.columns:
        upcoming_mask &= ~f["Status"].isin(CLOSED_STATUSES)

    upcoming_campus = (
        f.loc[upcoming_mask]
        .groupby("Campus")
        .size()
        .rename("Upcoming")
        .reset_index()
    )

    camp = camp.merge(
        upcoming_campus,
        on="Campus",
        how="left",
    )

    camp["Upcoming"] = (
        camp["Upcoming"]
        .fillna(0)
        .astype(int)
    )
else:
    camp["Upcoming"] = 0

# Open activities by campus
if "Status" in f.columns:
    open_mask = ~f["Status"].isin(CLOSED_STATUSES)

    open_campus = (
        f.loc[open_mask]
        .groupby("Campus")
        .size()
        .rename("Open_Activities")
        .reset_index()
    )

    camp = camp.merge(
        open_campus,
        on="Campus",
        how="left",
    )

    camp["Open_Activities"] = (
        camp["Open_Activities"]
        .fillna(0)
        .astype(int)
    )
else:
    camp["Open_Activities"] = camp["Activities"]

# High priority by campus
if "Priority" in f.columns:
    high_campus = (
        f.loc[f["Priority"].eq("High")]
        .groupby("Campus")
        .size()
        .rename("High_Priority")
        .reset_index()
    )

    camp = camp.merge(
        high_campus,
        on="Campus",
        how="left",
    )

    camp["High_Priority"] = (
        camp["High_Priority"]
        .fillna(0)
        .astype(int)
    )
else:
    camp["High_Priority"] = 0

# Reach realization percentage only where both values exist and planned > 0
if {
    "Planned_Reach",
    "Actual_Reach",
}.issubset(camp.columns):

    camp["Reach_Realization_%"] = pd.NA

    valid_realization = (
        camp["Planned_Reach"].notna()
        & camp["Actual_Reach"].notna()
        & camp["Planned_Reach"].gt(0)
    )

    camp.loc[
        valid_realization,
        "Reach_Realization_%",
    ] = (
        camp.loc[
            valid_realization,
            "Actual_Reach",
        ]
        / camp.loc[
            valid_realization,
            "Planned_Reach",
        ]
        * 100
    ).round(1)


# =========================================================
# KPI CALCULATIONS
# =========================================================
total_activities = int(len(f))
active_campuses = int(
    f["Campus"]
    .dropna()
    .nunique()
)

total_institutions = (
    int(
        f["Institution / Event Name"]
        .dropna()
        .nunique()
    )
    if "Institution / Event Name" in f.columns
    else 0
)

total_cities = (
    int(
        f["City"]
        .dropna()
        .nunique()
    )
    if "City" in f.columns
    else 0
)

planned_total = (
    f["Planned Student Reach"].sum(min_count=1)
    if "Planned Student Reach" in f.columns
    else pd.NA
)

actual_total = (
    f["Actual Student Reach"].sum(min_count=1)
    if "Actual Student Reach" in f.columns
    else pd.NA
)

planned_display = (
    "N/A"
    if pd.isna(planned_total)
    else f"{int(planned_total):,}"
)

actual_display = (
    "N/A"
    if pd.isna(actual_total)
    else f"{int(actual_total):,}"
)


# =========================================================
# KPI ROW
# =========================================================
k1, k2, k3, k4, k5, k6 = st.columns(
    6,
    gap="small",
)

with k1:
    campus_kpi(
        "Activities",
        f"{total_activities:,}",
        "Filtered outreach volume",
        "●",
        "kpi-blue",
    )

with k2:
    campus_kpi(
        "Active Campuses",
        f"{active_campuses:,}",
        "Campuses in current view",
        "⌂",
        "kpi-cyan",
    )

with k3:
    campus_kpi(
        "Institutions",
        f"{total_institutions:,}",
        "Unique institution coverage",
        "◆",
        "kpi-violet",
    )

with k4:
    campus_kpi(
        "Cities Covered",
        f"{total_cities:,}",
        "Unique geographic footprint",
        "⌖",
        "kpi-teal",
    )

with k5:
    campus_kpi(
        "Planned Reach",
        planned_display,
        "Known planned reach only",
        "◎",
        "kpi-amber",
    )

with k6:
    campus_kpi(
        "Actual Reach",
        actual_display,
        "Entered actual reach only",
        "✓",
        "kpi-green",
    )


# =========================================================
# CAMPUS SCORECARD TABLE
# =========================================================
st.markdown(
    '<div class="table-heading">Campus Performance Scorecard</div>'
    '<div class="table-subheading">'
    'Compact campus-level comparison. Blank reach values remain missing and are not converted to zero.'
    '</div>',
    unsafe_allow_html=True,
)

scorecard = camp.copy()

# Rename for professional display
rename_map = {
    "Planned_Reach": "Planned Reach",
    "Actual_Reach": "Actual Reach",
    "Reach_Realization_%": "Reach Realization %",
    "Open_Activities": "Open Activities",
    "High_Priority": "High Priority",
}

scorecard = scorecard.rename(
    columns=rename_map
)

display_cols = [
    "Campus",
    "Activities",
    "Institutions",
    "Cities",
    "Upcoming",
    "Open Activities",
    "High Priority",
    "Planned Reach",
    "Actual Reach",
    "Reach Realization %",
]

display_cols = [
    col for col in display_cols
    if col in scorecard.columns
]

st.dataframe(
    scorecard[display_cols],
    width="stretch",
    hide_index=True,
    height=220,
    row_height=31,
    column_config={
        "Campus": st.column_config.TextColumn(
            "Campus",
            width="small",
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
        "Cities": st.column_config.NumberColumn(
            "Cities",
            format="%d",
            width="small",
        ),
        "Upcoming": st.column_config.NumberColumn(
            "Upcoming",
            format="%d",
            width="small",
        ),
        "Open Activities": st.column_config.NumberColumn(
            "Open",
            format="%d",
            width="small",
        ),
        "High Priority": st.column_config.NumberColumn(
            "High Priority",
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
        "Reach Realization %": st.column_config.NumberColumn(
            "Reach Realization %",
            format="%.1f%%",
            width="small",
        ),
    },
)


# =========================================================
# ROW 1 — ACTIVITY VOLUME + MANAGEMENT INTELLIGENCE
# =========================================================
left, right = st.columns(
    [2.25, 1.0],
    gap="medium",
)

with left:
    with st.container(border=True):
        card_header(
            "Activity Volume by Campus",
            "Compare the number of outreach activities handled by each campus.",
        )

        volume_df = (
            camp[
                [
                    "Campus",
                    "Activities",
                ]
            ]
            .sort_values(
                "Activities",
                ascending=True,
            )
        )

        fig = px.bar(
            volume_df,
            x="Activities",
            y="Campus",
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
            dtick=1,
            rangemode="tozero",
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

        top_volume = (
            camp.sort_values(
                "Activities",
                ascending=False,
            )
            .iloc[0]
        )

        activity_share = (
            round(
                top_volume["Activities"]
                / camp["Activities"].sum()
                * 100,
                1,
            )
            if camp["Activities"].sum() > 0
            else 0
        )

        action_note(
            "Activity Volume Insight",
            (
                f'{top_volume["Campus"]} has the highest outreach load with '
                f'{int(top_volume["Activities"])} activities, representing '
                f'{activity_share}% of the selected activity volume.'
            ),
            "blue",
        )


with right:
    with st.container(border=True):
        card_header(
            "Campus Management Intelligence",
            "Fast comparison points for the selected view.",
        )

        top_institutions = (
            camp.sort_values(
                "Institutions",
                ascending=False,
            )
            .iloc[0]
            if "Institutions" in camp.columns
            else None
        )

        top_cities = (
            camp.sort_values(
                "Cities",
                ascending=False,
            )
            .iloc[0]
            if "Cities" in camp.columns
            else None
        )

        top_upcoming = (
            camp.sort_values(
                "Upcoming",
                ascending=False,
            )
            .iloc[0]
        )

        campus_insight(
            "Highest activity load",
            str(top_volume["Campus"]),
            f'{int(top_volume["Activities"])} outreach activities',
        )

        if top_institutions is not None:
            campus_insight(
                "Strongest institution coverage",
                str(top_institutions["Campus"]),
                f'{int(top_institutions["Institutions"])} unique institutions',
            )

        if top_cities is not None:
            campus_insight(
                "Widest city footprint",
                str(top_cities["Campus"]),
                f'{int(top_cities["Cities"])} cities covered',
            )

        campus_insight(
            "Highest upcoming load",
            str(top_upcoming["Campus"]),
            f'{int(top_upcoming["Upcoming"])} upcoming open activities',
        )


# =========================================================
# ROW 2 — INSTITUTION + CITY COVERAGE
# =========================================================
c1, c2 = st.columns(
    2,
    gap="medium",
)

with c1:
    with st.container(border=True):
        card_header(
            "Institution Coverage by Campus",
            "Unique institutions engaged by each campus.",
        )

        if "Institutions" not in camp.columns:
            st.info(
                "Institution coverage data available nahi hai."
            )
        else:
            inst_df = (
                camp[
                    [
                        "Campus",
                        "Institutions",
                    ]
                ]
                .sort_values(
                    "Institutions",
                    ascending=True,
                )
            )

            fig = px.bar(
                inst_df,
                x="Institutions",
                y="Campus",
                orientation="h",
                text="Institutions",
            )

            fig.update_traces(
                marker_color="#7A56D8",
                textposition="outside",
                textfont=dict(size=9),
                marker_line_width=0,
            )

            fig.update_xaxes(
                title="Institutions",
                dtick=1,
                rangemode="tozero",
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

            top_inst = (
                camp.sort_values(
                    "Institutions",
                    ascending=False,
                )
                .iloc[0]
            )

            action_note(
                "Institution Coverage Insight",
                (
                    f'{top_inst["Campus"]} currently leads institution coverage '
                    f'with {int(top_inst["Institutions"])} unique institutions. '
                    f'Use lower-coverage campuses to identify where additional '
                    f'institution acquisition may be required.'
                ),
                "violet",
            )


with c2:
    with st.container(border=True):
        card_header(
            "City Coverage by Campus",
            "Unique outreach cities covered by each campus.",
        )

        if "Cities" not in camp.columns:
            st.info(
                "City coverage data available nahi hai."
            )
        else:
            city_df = (
                camp[
                    [
                        "Campus",
                        "Cities",
                    ]
                ]
                .sort_values(
                    "Cities",
                    ascending=True,
                )
            )

            fig = px.bar(
                city_df,
                x="Cities",
                y="Campus",
                orientation="h",
                text="Cities",
            )

            fig.update_traces(
                marker_color="#159E8C",
                textposition="outside",
                textfont=dict(size=9),
                marker_line_width=0,
            )

            fig.update_xaxes(
                title="Cities",
                dtick=1,
                rangemode="tozero",
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

            top_city = (
                camp.sort_values(
                    "Cities",
                    ascending=False,
                )
                .iloc[0]
            )

            action_note(
                "Geographic Coverage Insight",
                (
                    f'{top_city["Campus"]} has the widest current footprint with '
                    f'{int(top_city["Cities"])} cities. Compare this against '
                    f'institution count to distinguish broad reach from deep coverage.'
                ),
                "teal",
            )


# =========================================================
# ROW 3 — REACH + PRIORITY / EXECUTION
# =========================================================
r1, r2 = st.columns(
    2,
    gap="medium",
)

with r1:
    with st.container(border=True):
        card_header(
            "Planned vs Actual Student Reach",
            "Actual reach is plotted only where it has been entered.",
        )

        if not {
            "Planned_Reach",
            "Actual_Reach",
        }.issubset(camp.columns):

            st.info(
                "Planned/Actual Reach columns available nahi hain."
            )

        else:
            reach_view = camp[
                [
                    "Campus",
                    "Planned_Reach",
                    "Actual_Reach",
                ]
            ].copy()

            reach_long = (
                reach_view.melt(
                    id_vars="Campus",
                    var_name="Reach Type",
                    value_name="Students",
                )
                .dropna(
                    subset=["Students"]
                )
            )

            reach_long["Reach Type"] = (
                reach_long["Reach Type"]
                .replace(
                    {
                        "Planned_Reach": "Planned",
                        "Actual_Reach": "Actual",
                    }
                )
            )

            if reach_long.empty:
                st.info(
                    "Reach values available nahi hain."
                )
            else:
                fig = px.bar(
                    reach_long,
                    x="Campus",
                    y="Students",
                    color="Reach Type",
                    barmode="group",
                    text="Students",
                    color_discrete_map={
                        "Planned": "#2D6CDF",
                        "Actual": "#18A999",
                    },
                    category_orders={
                        "Campus": [
                            "Lucknow",
                            "Noida",
                            "Jaipur",
                            "Indore",
                        ]
                    },
                )

                fig.update_traces(
                    textposition="outside",
                    textfont=dict(size=9),
                    marker_line_width=0,
                )

                fig.update_xaxes(title="")
                fig.update_yaxes(
                    title="Students",
                    rangemode="tozero",
                )

                st.plotly_chart(
                    clean_chart(
                        fig,
                        235,
                    ),
                    width="stretch",
                    config=CHART_CONFIG,
                )

                actual_missing = int(
                    camp["Actual_Reach"]
                    .isna()
                    .sum()
                )

                valid_realization = camp.dropna(
                    subset=[
                        "Reach_Realization_%",
                    ]
                )

                if valid_realization.empty:
                    realization_text = (
                        "No campus currently has enough entered data "
                        "for a reach-realization percentage."
                    )
                else:
                    best_realization = (
                        valid_realization.sort_values(
                            "Reach_Realization_%",
                            ascending=False,
                        )
                        .iloc[0]
                    )

                    realization_text = (
                        f'{best_realization["Campus"]} has the highest known '
                        f'reach realization at '
                        f'{float(best_realization["Reach_Realization_%"]):.1f}%.'
                    )

                action_note(
                    "Reach Insight",
                    (
                        realization_text
                        + f" Actual reach is still missing for "
                        f"{actual_missing} campus(es), so blanks are not "
                        f"treated as zero."
                    ),
                    "teal",
                )


with r2:
    with st.container(border=True):
        card_header(
            "Open & High-Priority Activity Load",
            "Execution pressure by campus using open and High-priority activity counts.",
        )

        pressure_df = camp[
            [
                "Campus",
                "Open_Activities",
                "High_Priority",
            ]
        ].copy()

        pressure_long = (
            pressure_df.melt(
                id_vars="Campus",
                var_name="Load Type",
                value_name="Activities",
            )
        )

        pressure_long["Load Type"] = (
            pressure_long["Load Type"]
            .replace(
                {
                    "Open_Activities": "Open",
                    "High_Priority": "High Priority",
                }
            )
        )

        fig = px.bar(
            pressure_long,
            x="Campus",
            y="Activities",
            color="Load Type",
            barmode="group",
            text="Activities",
            color_discrete_map={
                "Open": "#5B8FD6",
                "High Priority": "#D9534F",
            },
            category_orders={
                "Campus": [
                    "Lucknow",
                    "Noida",
                    "Jaipur",
                    "Indore",
                ]
            },
        )

        fig.update_traces(
            textposition="outside",
            textfont=dict(size=9),
            marker_line_width=0,
        )

        fig.update_xaxes(title="")
        fig.update_yaxes(
            title="Activities",
            dtick=1,
            rangemode="tozero",
        )

        st.plotly_chart(
            clean_chart(
                fig,
                235,
            ),
            width="stretch",
            config=CHART_CONFIG,
        )

        highest_open = (
            camp.sort_values(
                "Open_Activities",
                ascending=False,
            )
            .iloc[0]
        )

        highest_high = (
            camp.sort_values(
                "High_Priority",
                ascending=False,
            )
            .iloc[0]
        )

        action_note(
            "Execution Pressure Insight",
            (
                f'{highest_open["Campus"]} has the highest open activity load '
                f'({int(highest_open["Open_Activities"])}). '
                f'{highest_high["Campus"]} currently has the highest High-priority '
                f'load ({int(highest_high["High_Priority"])}).'
            ),
            "amber",
        )


# =========================================================
# CAMPUS-WISE MANAGEMENT CARDS
# =========================================================
st.markdown(
    '<div class="table-heading">Campus Management Insight</div>'
    '<div class="table-subheading">'
    'Campus-level summaries generated from the same filtered live data.'
    '</div>',
    unsafe_allow_html=True,
)

management_view = (
    camp.sort_values(
        "Activities",
        ascending=False,
    )
    .reset_index(drop=True)
)

if len(management_view) > 0:
    insight_columns = st.columns(
        min(4, len(management_view)),
        gap="small",
    )

    for idx, row in management_view.head(4).iterrows():
        with insight_columns[idx]:
            institutions_value = (
                int(row["Institutions"])
                if "Institutions" in row
                else 0
            )

            cities_value = (
                int(row["Cities"])
                if "Cities" in row
                else 0
            )

            upcoming_value = (
                int(row["Upcoming"])
                if "Upcoming" in row
                else 0
            )

            high_value = (
                int(row["High_Priority"])
                if "High_Priority" in row
                else 0
            )

            campus_insight(
                str(row["Campus"]),
                f'{int(row["Activities"])} activities',
                (
                    f'{institutions_value} institutions • '
                    f'{cities_value} cities • '
                    f'{upcoming_value} upcoming • '
                    f'{high_value} High priority'
                ),
            )


# =========================================================
# FINAL MANAGEMENT RECOMMENDATION
# =========================================================
if len(camp) > 1:
    max_activity = camp["Activities"].max()
    min_activity = camp["Activities"].min()
    activity_gap = int(max_activity - min_activity)
else:
    activity_gap = 0

if activity_gap > 0:
    balance_message = (
        f"The activity-volume gap between the highest and lowest campus is "
        f"{activity_gap} activities. Review whether this difference reflects "
        f"market opportunity, capacity, or under-planning."
    )
else:
    balance_message = (
        "Activity volume is currently balanced across the campuses visible "
        "in this selection."
    )

action_note(
    "Campus Management Recommendation",
    (
        balance_message
        + " Compare volume with institution depth, city footprint, upcoming load "
          "and entered reach before changing outreach targets."
    ),
    "blue",
)
