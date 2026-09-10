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
page_config("Institution Coverage")
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
    animation: institutionBrandMotion 3.8s ease-in-out infinite alternate;
}

[data-testid="stSidebar"] .brand-sub {
    animation-delay: .18s;
    color: #A9C9EF !important;
    font-size: .72rem !important;
    line-height: 1.35 !important;
}

@keyframes institutionBrandMotion {
    from { transform: translateX(-6px); }
    to   { transform: translateX(24px); }
}

[data-testid="stSidebar"] .stPageLink a {
    padding: .56rem .62rem !important;
    margin-bottom: .14rem !important;
    font-size: .90rem !important;
}

/* ---------- Moving page title ---------- */
.inst-header {
    transform: translateY(-13px);
    margin-bottom: -8px;
}

.inst-eyebrow {
    color: #2B6DE8;
    font-size: .67rem;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
    margin-bottom: .05rem;
}

.inst-title-row {
    position: relative;
    width: 100%;
    padding-right: 10.8rem;
}

.inst-title-wrap {
    position: relative;
    width: 100%;
    height: 1.72rem;
    overflow: hidden;
    white-space: nowrap;
}

.inst-title {
    position: absolute;
    top: 0;
    width: max-content;
    color: #0F2A45;
    font-size: 1.28rem;
    font-weight: 850;
    letter-spacing: -.02em;
    line-height: 1.02;
    white-space: nowrap;
    animation: institutionTitleShuttle 6.3s linear infinite alternate;
}

@keyframes institutionTitleShuttle {
    0% {
        left: 0%;
        transform: translateX(-105%);
    }
    100% {
        left: 100%;
        transform: translateX(4%);
    }
}

.inst-live {
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

.inst-subtitle {
    color: #71839A;
    font-size: .86rem;
    margin-top: .02rem;
}

.inst-accent {
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
.inst-kpi {
    position: relative;
    overflow: hidden;
    min-height: 94px;
    border-radius: 14px;
    padding: .64rem .72rem .60rem .72rem;
    background: linear-gradient(145deg, #FFF 0%, var(--wash) 100%);
    border: 1px solid var(--border);
    box-shadow: 0 6px 18px rgba(15,42,69,.045);
    animation: instFloat 2.15s ease-in-out infinite;
}

.inst-kpi::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 0;
    width: 4px;
    background: linear-gradient(180deg, var(--accent), var(--accent2));
}

.inst-kpi::after {
    content: "";
    position: absolute;
    width: 82px;
    height: 82px;
    border-radius: 50%;
    right: -32px;
    top: -34px;
    background: radial-gradient(circle, var(--bubble) 0%, rgba(255,255,255,0) 72%);
}

.inst-kpi .icon {
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

.inst-kpi .label {
    position: relative;
    z-index: 2;
    color: #60758C;
    font-size: .66rem;
    font-weight: 850;
    white-space: nowrap;
}

.inst-kpi .value {
    position: relative;
    z-index: 2;
    color: #0F2A45;
    font-size: 1.72rem;
    font-weight: 900;
    line-height: 1;
    margin-top: .18rem;
}

.inst-kpi .sub {
    position: relative;
    z-index: 2;
    color: #8293A8;
    font-size: .60rem;
    margin-top: .17rem;
}

.inst-kpi .mini-line {
    position: absolute;
    left: .72rem;
    right: .72rem;
    bottom: .36rem;
    height: 2px;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: .18;
}

@keyframes instFloat {
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

/* ---------- Generic cards ---------- */
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
.inst-insight {
    padding: .70rem .76rem;
    border-radius: 10px;
    border: 1px solid #DFE7F0;
    background: #FFFFFF;
    box-shadow: 0 4px 12px rgba(15,42,69,.025);
    margin-bottom: .48rem;
}

.inst-insight .label {
    font-size: .64rem;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: .04em;
    color: #74879D;
}

.inst-insight .value {
    font-size: .96rem;
    font-weight: 900;
    color: #0F2A45;
    margin-top: .12rem;
}

.inst-insight .note {
    color: #7E90A6;
    font-size: .68rem;
    line-height: 1.42;
    margin-top: .18rem;
}

/* Institution Management Insight cards — subtle professional motion only */
.inst-insight.management-motion {
    position: relative;
    overflow: hidden;
    transition:
        transform .22s ease,
        box-shadow .22s ease,
        border-color .22s ease;
    animation: institutionManagementFloat 2.4s ease-in-out infinite;
}

.inst-insight.management-motion::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    border-radius: 10px 0 0 10px;
    background: linear-gradient(180deg, #2B6DE8, #60A5FA);
}

.inst-insight.management-motion::after {
    content: "";
    position: absolute;
    width: 78px;
    height: 78px;
    border-radius: 50%;
    right: -30px;
    top: -34px;
    background: radial-gradient(
        circle,
        rgba(96,165,250,.15) 0%,
        rgba(255,255,255,0) 72%
    );
    pointer-events: none;
}

.inst-insight.management-motion:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 24px rgba(15,42,69,.075);
    border-color: #CFE0F4;
}

@keyframes institutionManagementFloat {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-4px); }
}

.inst-action {
    margin-top: .25rem;
    padding: .68rem .74rem;
    border-radius: 10px;
    background: linear-gradient(90deg, #EFF6FF 0%, #FBFDFF 100%);
    border: 1px solid #D9E7FA;
    border-left: 4px solid #2B6DE8;
}

.inst-action.teal {
    background: linear-gradient(90deg, #EFFBF8 0%, #FBFEFD 100%);
    border-color: #D6EFEA;
    border-left-color: #159E8C;
}

.inst-action.violet {
    background: linear-gradient(90deg, #F6F2FF 0%, #FCFAFF 100%);
    border-color: #E6DCFF;
    border-left-color: #7C3AED;
}

.inst-action.amber {
    background: linear-gradient(90deg, #FFF8EC 0%, #FFFDFB 100%);
    border-color: #F2E0BE;
    border-left-color: #D98B16;
}

.inst-action .title {
    color: #173A61;
    font-size: .69rem;
    font-weight: 850;
}

.inst-action .body {
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
    .inst-title,
    .inst-kpi,
    .inst-insight.management-motion,
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
def institution_kpi(label, value, subtitle, icon, css_class):
    st.markdown(
        (
            f'<div class="inst-kpi {css_class}">'
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


def institution_insight(label, value, note):
    st.markdown(
        (
            '<div class="inst-insight">'
            f'<div class="label">{label}</div>'
            f'<div class="value">{value}</div>'
            f'<div class="note">{note}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def institution_management_insight(label, value, note):
    st.markdown(
        (
            '<div class="inst-insight management-motion">'
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
            f'<div class="inst-action {tone_class}">'
            f'<div class="title">{title}</div>'
            f'<div class="body">{body}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def clean_chart(fig, height=240, legend=True):
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
    '<div class="inst-header">'
    '<div class="inst-eyebrow">PGDM Outreach Intelligence</div>'
    '<div class="inst-title-row">'
    '<div class="inst-title-wrap">'
    '<div class="inst-title">Institution Coverage</div>'
    '</div>'
    '<div class="inst-live">● LIVE GOOGLE SHEET</div>'
    '</div>'
    '<div class="inst-subtitle">'
    'Institution engagement depth, repeat activity, relationship strength and student-reach coverage.'
    '</div>'
    '<div class="inst-accent"></div>'
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
        key="inst_page_campus",
    )

with f2:
    activity_values = (
        ["All"] + sorted(df["Activity Type"].dropna().unique().tolist())
        if "Activity Type" in df.columns else ["All"]
    )
    activity_filter = st.selectbox(
        "Activity Type",
        activity_values,
        key="inst_page_activity",
    )

with f3:
    segment_values = (
        ["All"] + sorted(df["Target Segment"].dropna().unique().tolist())
        if "Target Segment" in df.columns else ["All"]
    )
    segment_filter = st.selectbox(
        "Target Segment",
        segment_values,
        key="inst_page_segment",
    )

with f4:
    owner_values = (
        ["All"] + sorted(df["Activity Owner"].dropna().unique().tolist())
        if "Activity Owner" in df.columns else ["All"]
    )
    owner_filter = st.selectbox(
        "Owner",
        owner_values,
        key="inst_page_owner",
    )

with f5:
    status_values = (
        ["All"] + sorted(df["Status"].dropna().unique().tolist())
        if "Status" in df.columns else ["All"]
    )
    status_filter = st.selectbox(
        "Status",
        status_values,
        key="inst_page_status",
    )

with f6:
    priority_values = (
        ["All"] + sorted(df["Priority"].dropna().unique().tolist())
        if "Priority" in df.columns else ["All"]
    )
    priority_filter = st.selectbox(
        "Priority",
        priority_values,
        key="inst_page_priority",
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
            key="inst_page_date",
        )
    else:
        st.text_input(
            "Date Range",
            value="",
            disabled=True,
            key="inst_page_date_text",
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
        "Selected filters ke liye koi institution coverage data available nahi hai."
    )
    st.stop()

if "Institution / Event Name" not in f.columns:
    st.info("Institution / Event Name column available nahi hai.")
    st.stop()


# =========================================================
# INSTITUTION AGGREGATION
# =========================================================
group_cols = [
    col
    for col in [
        "Campus",
        "Institution / Event Name",
        "City",
        "State",
    ]
    if col in f.columns
]

agg_dict = {
    "Activities": (
        "Institution / Event Name",
        "size",
    ),
}

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

if "Activity Date" in f.columns:
    agg_dict["Last_Activity_Date"] = (
        "Activity Date",
        "max",
    )

inst = (
    f.groupby(
        group_cols,
        dropna=False,
    )
    .agg(**agg_dict)
    .reset_index()
)

inst["Activities"] = (
    pd.to_numeric(
        inst["Activities"],
        errors="coerce",
    )
    .fillna(0)
    .astype(int)
)

# Relationship strength is shown as most frequent captured value for each row.
if "Relationship Strength" in f.columns:
    relationship_lookup = (
        f.dropna(
            subset=[
                "Institution / Event Name",
                "Relationship Strength",
            ]
        )
        .groupby(
            group_cols,
            dropna=False,
        )["Relationship Strength"]
        .agg(
            lambda s: (
                s.value_counts().index[0]
                if not s.empty
                else pd.NA
            )
        )
        .rename("Relationship Strength")
        .reset_index()
    )

    inst = inst.merge(
        relationship_lookup,
        on=group_cols,
        how="left",
    )


# =========================================================
# PAGE METRICS
# =========================================================
unique_institutions = int(
    f["Institution / Event Name"]
    .dropna()
    .nunique()
)

institution_activity_count = (
    f["Institution / Event Name"]
    .dropna()
    .value_counts()
)

repeat_institutions = int(
    institution_activity_count.gt(1).sum()
)

cities_covered = (
    int(f["City"].dropna().nunique())
    if "City" in f.columns
    else 0
)

states_covered = (
    int(f["State"].dropna().nunique())
    if "State" in f.columns
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
    institution_kpi(
        "Institutions",
        f"{unique_institutions:,}",
        "Unique institutions",
        "◆",
        "kpi-blue",
    )

with k2:
    institution_kpi(
        "Repeat Institutions",
        f"{repeat_institutions:,}",
        "2+ outreach activities",
        "↻",
        "kpi-cyan",
    )

with k3:
    institution_kpi(
        "Cities Covered",
        f"{cities_covered:,}",
        "Institution geography",
        "⌖",
        "kpi-violet",
    )

with k4:
    institution_kpi(
        "States Covered",
        f"{states_covered:,}",
        "State-level footprint",
        "◇",
        "kpi-teal",
    )

with k5:
    institution_kpi(
        "Planned Reach",
        planned_display,
        "Known planned reach only",
        "◎",
        "kpi-amber",
    )

with k6:
    institution_kpi(
        "Actual Reach",
        actual_display,
        "Entered actual reach only",
        "✓",
        "kpi-green",
    )


# =========================================================
# INSTITUTION ENGAGEMENT TABLE
# =========================================================
st.markdown(
    '<div class="table-heading">Institution Engagement Scorecard</div>'
    '<div class="table-subheading">'
    'Compact institution-level view. Missing reach values remain blank and are not treated as zero.'
    '</div>',
    unsafe_allow_html=True,
)

scorecard = inst.rename(
    columns={
        "Planned_Reach": "Planned Reach",
        "Actual_Reach": "Actual Reach",
        "Last_Activity_Date": "Last Activity",
    }
).copy()

display_cols = [
    "Campus",
    "Institution / Event Name",
    "City",
    "State",
    "Activities",
    "Relationship Strength",
    "Planned Reach",
    "Actual Reach",
    "Last Activity",
]

display_cols = [
    col
    for col in display_cols
    if col in scorecard.columns
]

scorecard_view = scorecard[display_cols].sort_values(
    ["Activities", "Institution / Event Name"],
    ascending=[False, True],
)

visible_scorecard_rows = min(
    max(len(scorecard_view), 1),
    8,
)

scorecard_height = 38 + (
    visible_scorecard_rows * 30
)

st.dataframe(
    scorecard_view,
    width="stretch",
    hide_index=True,
    height=scorecard_height,
    row_height=30,
    column_config={
        "Campus": st.column_config.TextColumn(
            "Campus",
            width="small",
        ),
        "Institution / Event Name": st.column_config.TextColumn(
            "Institution / Event",
            width="large",
        ),
        "City": st.column_config.TextColumn(
            "City",
            width="small",
        ),
        "State": st.column_config.TextColumn(
            "State",
            width="medium",
        ),
        "Activities": st.column_config.NumberColumn(
            "Activities",
            format="%d",
            width="small",
        ),
        "Relationship Strength": st.column_config.TextColumn(
            "Relationship",
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
        "Last Activity": st.column_config.DateColumn(
            "Last Activity",
            format="DD MMM YY",
            width="small",
        ),
    },
)


# =========================================================
# ROW 1 — ENGAGEMENT DEPTH + MANAGEMENT INTELLIGENCE
# =========================================================
left, right = st.columns(
    [2.25, 1.0],
    gap="medium",
)

with left:
    with st.container(border=True):
        card_header(
            "Most Engaged Institutions",
            "Top institutions ranked by activity frequency in the selected view.",
        )

        institution_rank = (
            f["Institution / Event Name"]
            .dropna()
            .value_counts()
            .rename_axis("Institution")
            .reset_index(name="Activities")
            .head(10)
            .sort_values("Activities")
        )

        if institution_rank.empty:
            st.info(
                "Institution engagement data available nahi hai."
            )
        else:
            fig = px.bar(
                institution_rank,
                x="Activities",
                y="Institution",
                orientation="h",
                text="Activities",
            )

            fig.update_traces(
                marker_color="#2468B4",
                textposition="outside",
                textfont=dict(size=9),
                marker_line_width=0,
                cliponaxis=False,
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
                    255,
                    legend=False,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )

            top_activity_count = int(
                institution_rank["Activities"].max()
            )

            tied_top = (
                institution_rank.loc[
                    institution_rank["Activities"].eq(
                        top_activity_count
                    ),
                    "Institution",
                ]
                .astype(str)
                .sort_values()
                .tolist()
            )

            shown_top = tied_top[:3]
            extra_top = max(
                0,
                len(tied_top) - len(shown_top),
            )

            if len(shown_top) == 1:
                leader_names = shown_top[0]
                leader_phrase = "has"
            elif len(shown_top) == 2:
                leader_names = (
                    f"{shown_top[0]} and {shown_top[1]}"
                )
                leader_phrase = "jointly have"
            else:
                leader_names = (
                    ", ".join(shown_top[:-1])
                    + f", and {shown_top[-1]}"
                )
                leader_phrase = "jointly have"

            if extra_top > 0:
                leader_names += (
                    f" and {extra_top} more"
                )

            share_each = (
                round(
                    top_activity_count
                    / len(f)
                    * 100,
                    1,
                )
                if len(f) > 0
                else 0
            )

            action_note(
                "Institution Engagement Insight",
                (
                    f"{leader_names} {leader_phrase} the highest activity frequency "
                    f"with {top_activity_count} activities each "
                    f"({share_each}% of all selected outreach records per institution). "
                    f"{repeat_institutions} institutions currently have repeat engagement."
                ),
                "blue",
            )


with right:
    with st.container(border=True):
        card_header(
            "Institution Intelligence",
            "Management-ready institution coverage summary.",
        )

        if institution_activity_count.empty:
            top_institution_display = "N/A"
            top_institution_count = 0
            top_institution_note = "No institution activity available."
        else:
            top_institution_count = int(
                institution_activity_count.iloc[0]
            )

            tied_institutions = (
                institution_activity_count[
                    institution_activity_count.eq(
                        top_institution_count
                    )
                ]
                .index.astype(str)
                .tolist()
            )

            shown_tied = tied_institutions[:3]
            extra_tied = max(
                0,
                len(tied_institutions) - len(shown_tied),
            )

            top_institution_display = ", ".join(
                shown_tied
            )

            if extra_tied > 0:
                top_institution_display += (
                    f" +{extra_tied} more"
                )

            top_institution_note = (
                f"{top_institution_count} outreach activities each"
                if len(tied_institutions) > 1
                else f"{top_institution_count} outreach activities"
            )

        institution_insight(
            "Most engaged institution",
            top_institution_display,
            top_institution_note,
        )

        institution_insight(
            "Repeat engagement",
            f"{repeat_institutions}",
            (
                f"{repeat_institutions} of {unique_institutions} institutions "
                f"have more than one outreach activity."
            ),
        )

        if (
            "Relationship Strength" in f.columns
            and f["Relationship Strength"].notna().any()
        ):
            relationship_counts = (
                f["Relationship Strength"]
                .dropna()
                .value_counts()
            )

            dominant_relationship = (
                relationship_counts.index[0]
            )

            dominant_relationship_count = int(
                relationship_counts.iloc[0]
            )

            relationship_share = round(
                dominant_relationship_count
                / int(relationship_counts.sum())
                * 100,
                1,
            )

            institution_insight(
                "Dominant relationship",
                str(dominant_relationship),
                (
                    f"{relationship_share}% of captured relationship values "
                    f"are {dominant_relationship}."
                ),
            )
        else:
            institution_insight(
                "Dominant relationship",
                "N/A",
                "Relationship Strength is not captured in the selected view.",
            )

        if (
            "State" in f.columns
            and f["State"].notna().any()
        ):
            state_counts = (
                f["State"]
                .dropna()
                .value_counts()
            )

            top_state = state_counts.index[0]
            top_state_count = int(
                state_counts.iloc[0]
            )

            institution_insight(
                "Highest state concentration",
                str(top_state),
                f"{top_state_count} outreach records",
            )


# =========================================================
# ROW 2 — CAMPUS COVERAGE + RELATIONSHIP STRENGTH
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

        campus_coverage = (
            f.groupby("Campus")[
                "Institution / Event Name"
            ]
            .nunique()
            .rename("Institutions")
            .reset_index()
            .sort_values("Institutions")
            if "Campus" in f.columns
            else pd.DataFrame()
        )

        if campus_coverage.empty:
            st.info(
                "Campus-wise institution coverage available nahi hai."
            )
        else:
            fig = px.bar(
                campus_coverage,
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
                cliponaxis=False,
            )

            fig.update_xaxes(
                title="Institutions",
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

            top_campus = (
                campus_coverage
                .sort_values(
                    "Institutions",
                    ascending=False,
                )
                .iloc[0]
            )

            action_note(
                "Campus Coverage Insight",
                (
                    f'{top_campus["Campus"]} currently covers the highest number '
                    f'of unique institutions ({int(top_campus["Institutions"])}). '
                    f'Compare this with repeat engagement to separate breadth from depth.'
                ),
                "violet",
            )


with c2:
    with st.container(border=True):
        card_header(
            "Relationship Strength",
            "Distribution of captured institution relationship strength.",
        )

        if (
            "Relationship Strength" not in f.columns
            or not f["Relationship Strength"].notna().any()
        ):
            st.info(
                "Relationship Strength data available nahi hai."
            )
        else:
            relationship_df = (
                f["Relationship Strength"]
                .dropna()
                .value_counts()
                .rename_axis("Relationship Strength")
                .reset_index(name="Activities")
            )

            relationship_color_map = {
                "Strong": "#238A57",
                "Medium": "#D98B16",
                "Weak": "#D9534F",
                "New": "#2D6CDF",
            }

            fig = px.bar(
                relationship_df,
                x="Relationship Strength",
                y="Activities",
                text="Activities",
                color="Relationship Strength",
                color_discrete_map=relationship_color_map,
            )

            fig.update_traces(
                textposition="outside",
                textfont=dict(size=9),
                marker_line_width=0,
                cliponaxis=False,
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
                    legend=False,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )

            dominant = (
                relationship_df
                .sort_values(
                    "Activities",
                    ascending=False,
                )
                .iloc[0]
            )

            captured_total = int(
                relationship_df["Activities"]
                .sum()
            )

            captured_share = (
                round(
                    int(dominant["Activities"])
                    / captured_total
                    * 100,
                    1,
                )
                if captured_total > 0
                else 0
            )

            action_note(
                "Relationship Insight",
                (
                    f'{dominant["Relationship Strength"]} is the dominant captured '
                    f'relationship level with {int(dominant["Activities"])} records '
                    f'({captured_share}% of captured relationship data).'
                ),
                "teal",
            )


# =========================================================
# ROW 3 — REACH + STATE FOOTPRINT
# =========================================================
r1, r2 = st.columns(
    2,
    gap="medium",
)

with r1:
    with st.container(border=True):
        card_header(
            "Planned vs Actual Reach — Institutions",
            "Top institutions by known planned reach; actual shown only when entered.",
        )

        if "Planned Student Reach" not in f.columns:
            st.info(
                "Planned Student Reach column available nahi hai."
            )
        else:
            reach_inst = (
                f.groupby(
                    "Institution / Event Name",
                    dropna=False,
                )
                .agg(
                    Planned=(
                        "Planned Student Reach",
                        lambda s: s.sum(min_count=1),
                    ),
                    Actual=(
                        "Actual Student Reach",
                        lambda s: s.sum(min_count=1),
                    )
                    if "Actual Student Reach" in f.columns
                    else (
                        "Planned Student Reach",
                        lambda s: pd.NA,
                    ),
                )
                .reset_index()
            )

            known_planned = (
                reach_inst.dropna(
                    subset=["Planned"]
                )
                .sort_values(
                    "Planned",
                    ascending=False,
                )
                .head(8)
            )

            if known_planned.empty:
                st.info(
                    "Institution-level planned reach available nahi hai."
                )
            else:
                reach_long = (
                    known_planned.melt(
                        id_vars="Institution / Event Name",
                        value_vars=[
                            "Planned",
                            "Actual",
                        ],
                        var_name="Reach Type",
                        value_name="Students",
                    )
                    .dropna(
                        subset=["Students"]
                    )
                )

                fig = px.bar(
                    reach_long,
                    x="Students",
                    y="Institution / Event Name",
                    orientation="h",
                    color="Reach Type",
                    barmode="group",
                    text="Students",
                    color_discrete_map={
                        "Planned": "#2D6CDF",
                        "Actual": "#18A999",
                    },
                )

                fig.update_traces(
                    textposition="outside",
                    textfont=dict(size=9),
                    marker_line_width=0,
                    cliponaxis=False,
                )

                fig.update_xaxes(
                    title="Students",
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
                        255,
                    ),
                    width="stretch",
                    config=CHART_CONFIG,
                )

                missing_actual = int(
                    known_planned["Actual"]
                    .isna()
                    .sum()
                )

                top_planned = known_planned.iloc[0]

                action_note(
                    "Institution Reach Insight",
                    (
                        f'{top_planned["Institution / Event Name"]} has the highest '
                        f'known planned reach ({int(top_planned["Planned"]):,}). '
                        f'Actual reach is missing for {missing_actual} of the '
                        f'top planned-reach institutions shown, so blanks are '
                        f'not interpreted as zero.'
                    ),
                    "teal",
                )


with r2:
    with st.container(border=True):
        card_header(
            "State Footprint",
            "Institution outreach activity concentration by state.",
        )

        if (
            "State" not in f.columns
            or not f["State"].notna().any()
        ):
            st.info(
                "State data available nahi hai."
            )
        else:
            state_df = (
                f["State"]
                .dropna()
                .value_counts()
                .rename_axis("State")
                .reset_index(name="Activities")
                .sort_values("Activities")
            )

            fig = px.bar(
                state_df,
                x="Activities",
                y="State",
                orientation="h",
                text="Activities",
            )

            fig.update_traces(
                marker_color="#159E8C",
                textposition="outside",
                textfont=dict(size=9),
                marker_line_width=0,
                cliponaxis=False,
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
                    255,
                    legend=False,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )

            top_state_row = (
                state_df
                .sort_values(
                    "Activities",
                    ascending=False,
                )
                .iloc[0]
            )

            state_share = (
                round(
                    int(top_state_row["Activities"])
                    / int(state_df["Activities"].sum())
                    * 100,
                    1,
                )
                if int(state_df["Activities"].sum()) > 0
                else 0
            )

            action_note(
                "State Coverage Insight",
                (
                    f'{top_state_row["State"]} has the highest current institution '
                    f'activity concentration with {int(top_state_row["Activities"])} '
                    f'records ({state_share}% of the selected outreach activity).'
                ),
                "violet",
            )


# =========================================================
# INSTITUTION MANAGEMENT CARDS
# =========================================================
st.markdown(
    '<div class="table-heading">Institution Management Insight</div>'
    '<div class="table-subheading">'
    'Top institutions summarised using activity frequency and latest available engagement details.'
    '</div>',
    unsafe_allow_html=True,
)

top_management = (
    inst.sort_values(
        [
            "Activities",
            "Institution / Event Name",
        ],
        ascending=[
            False,
            True,
        ],
    )
    .head(4)
    .reset_index(drop=True)
)

if not top_management.empty:
    insight_cols = st.columns(
        min(
            4,
            len(top_management),
        ),
        gap="small",
    )

    for idx, row in top_management.iterrows():
        with insight_cols[idx]:
            campus_value = (
                str(row["Campus"])
                if "Campus" in row and pd.notna(row["Campus"])
                else "Campus N/A"
            )

            city_value = (
                str(row["City"])
                if "City" in row and pd.notna(row["City"])
                else "City N/A"
            )

            relation_value = (
                str(row["Relationship Strength"])
                if "Relationship Strength" in row
                and pd.notna(row["Relationship Strength"])
                else "Relationship N/A"
            )

            institution_management_insight(
                str(row["Institution / Event Name"]),
                f'{int(row["Activities"])} activities',
                (
                    f"{campus_value} • {city_value} • {relation_value}"
                ),
            )


# =========================================================
# FINAL RECOMMENDATION
# =========================================================
if unique_institutions > 0:
    repeat_rate = round(
        repeat_institutions
        / unique_institutions
        * 100,
        1,
    )
else:
    repeat_rate = 0

if repeat_rate < 30:
    repeat_message = (
        f"Repeat-engagement rate is {repeat_rate}%. Institution strategy is "
        f"currently more breadth-led than depth-led."
    )
else:
    repeat_message = (
        f"Repeat-engagement rate is {repeat_rate}%, indicating meaningful "
        f"repeat interaction with the institution base."
    )

action_note(
    "Institution Coverage Recommendation",
    (
        repeat_message
        + " Use activity frequency, relationship strength, campus coverage, "
          "geographic concentration and entered reach together before deciding "
          "which institutions should receive deeper follow-up or repeat visits."
    ),
    "blue",
)
