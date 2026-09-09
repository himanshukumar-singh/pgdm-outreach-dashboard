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
page_config("Action Center")
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
    animation: actionBrandMotion 3.8s ease-in-out infinite alternate;
}

[data-testid="stSidebar"] .brand-sub {
    animation-delay: .18s;
    color: #A9C9EF !important;
    font-size: .72rem !important;
    line-height: 1.35 !important;
}

@keyframes actionBrandMotion {
    from { transform: translateX(-6px); }
    to   { transform: translateX(24px); }
}

[data-testid="stSidebar"] .stPageLink a {
    padding: .56rem .62rem !important;
    margin-bottom: .14rem !important;
    font-size: .90rem !important;
}

/* ---------- Moving page title ---------- */
.action-header {
    transform: translateY(-13px);
    margin-bottom: -8px;
}

.action-eyebrow {
    color: #2B6DE8;
    font-size: .67rem;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
    margin-bottom: .05rem;
}

.action-title-row {
    position: relative;
    width: 100%;
    padding-right: 10.8rem;
}

.action-title-wrap {
    position: relative;
    width: 100%;
    height: 1.72rem;
    overflow: hidden;
    white-space: nowrap;
}

.action-title {
    position: absolute;
    top: 0;
    width: max-content;
    color: #0F2A45;
    font-size: 1.28rem;
    font-weight: 850;
    letter-spacing: -.02em;
    line-height: 1.02;
    white-space: nowrap;
    animation: actionTitleShuttle 6.3s linear infinite alternate;
}

@keyframes actionTitleShuttle {
    0% {
        left: 0%;
        transform: translateX(-105%);
    }
    100% {
        left: 100%;
        transform: translateX(4%);
    }
}

.action-live {
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

.action-subtitle {
    color: #71839A;
    font-size: .86rem;
    margin-top: .02rem;
}

.action-accent {
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
.action-kpi {
    position: relative;
    overflow: hidden;
    min-height: 94px;
    border-radius: 14px;
    padding: .64rem .72rem .60rem .72rem;
    background: linear-gradient(145deg, #FFF 0%, var(--wash) 100%);
    border: 1px solid var(--border);
    box-shadow: 0 6px 18px rgba(15,42,69,.045);
    animation: actionFloat 2.15s ease-in-out infinite;
}

.action-kpi::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 0;
    width: 4px;
    background: linear-gradient(180deg, var(--accent), var(--accent2));
}

.action-kpi::after {
    content: "";
    position: absolute;
    width: 82px;
    height: 82px;
    border-radius: 50%;
    right: -32px;
    top: -34px;
    background: radial-gradient(circle, var(--bubble) 0%, rgba(255,255,255,0) 72%);
}

.action-kpi .icon {
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

.action-kpi .label {
    position: relative;
    z-index: 2;
    color: #60758C;
    font-size: .66rem;
    font-weight: 850;
    white-space: nowrap;
}

.action-kpi .value {
    position: relative;
    z-index: 2;
    color: #0F2A45;
    font-size: 1.72rem;
    font-weight: 900;
    line-height: 1;
    margin-top: .18rem;
}

.action-kpi .sub {
    position: relative;
    z-index: 2;
    color: #8293A8;
    font-size: .60rem;
    margin-top: .17rem;
}

.action-kpi .mini-line {
    position: absolute;
    left: .72rem;
    right: .72rem;
    bottom: .36rem;
    height: 2px;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: .18;
}

@keyframes actionFloat {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-5px); }
}

.kpi-red {
    --accent:#C9404B; --accent2:#F07A83; --wash:#FFF5F6;
    --border:#F4DADC; --bubble:#FBE4E6; --iconbg:#FFF0F1;
}
.kpi-amber {
    --accent:#D98B16; --accent2:#FBBF24; --wash:#FFF9EE;
    --border:#F6E6C4; --bubble:#FFF0CF; --iconbg:#FFF5DF;
}
.kpi-green {
    --accent:#238A57; --accent2:#4ADE80; --wash:#F2FAF5;
    --border:#D6EFDF; --bubble:#DCF4E4; --iconbg:#EAF8EF;
}
.kpi-blue {
    --accent:#2563EB; --accent2:#60A5FA; --wash:#F2F7FF;
    --border:#D7E5FF; --bubble:#DCE9FF; --iconbg:#EAF2FF;
}
.kpi-violet {
    --accent:#7C3AED; --accent2:#A78BFA; --wash:#F7F3FF;
    --border:#E6DBFF; --bubble:#E9DEFF; --iconbg:#F0E9FF;
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
.action-insight {
    padding: .70rem .76rem;
    border-radius: 10px;
    border: 1px solid #DFE7F0;
    background: #FFFFFF;
    box-shadow: 0 4px 12px rgba(15,42,69,.025);
    margin-bottom: .48rem;
}

.action-insight .label {
    font-size: .64rem;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: .04em;
    color: #74879D;
}

.action-insight .value {
    font-size: .96rem;
    font-weight: 900;
    color: #0F2A45;
    margin-top: .12rem;
}

.action-insight .note {
    color: #7E90A6;
    font-size: .68rem;
    line-height: 1.42;
    margin-top: .18rem;
}

.action-note {
    margin-top: .25rem;
    padding: .68rem .74rem;
    border-radius: 10px;
    background: linear-gradient(90deg, #EFF6FF 0%, #FBFDFF 100%);
    border: 1px solid #D9E7FA;
    border-left: 4px solid #2B6DE8;
}

.action-note.red {
    background: linear-gradient(90deg, #FFF3F4 0%, #FFFDFD 100%);
    border-color: #F2D5D8;
    border-left-color: #C9404B;
}

.action-note.amber {
    background: linear-gradient(90deg, #FFF8EC 0%, #FFFDFB 100%);
    border-color: #F2E0BE;
    border-left-color: #D98B16;
}

.action-note.green {
    background: linear-gradient(90deg, #EFFAF3 0%, #FBFEFC 100%);
    border-color: #D6EEDD;
    border-left-color: #238A57;
}

.action-note.violet {
    background: linear-gradient(90deg, #F6F2FF 0%, #FCFAFF 100%);
    border-color: #E6DCFF;
    border-left-color: #7C3AED;
}

.action-note .title {
    color: #173A61;
    font-size: .69rem;
    font-weight: 850;
}

.action-note .body {
    color: #6C7E91;
    font-size: .70rem;
    line-height: 1.42;
    margin-top: .18rem;
}

/* ---------- Control cards ---------- */
.control-card {
    min-height: 112px;
    padding: .78rem .82rem;
    border-radius: 12px;
    background: #FFFFFF;
    border: 1px solid #DFE7F0;
    border-top: 4px solid var(--control);
    box-shadow: 0 5px 16px rgba(15,42,69,.03);
}

.control-card .ctitle {
    color: #0F2A45;
    font-size: .78rem;
    font-weight: 850;
}

.control-card .cbody {
    color: #6E8197;
    font-size: .70rem;
    line-height: 1.48;
    margin-top: .34rem;
}

.control-blue { --control:#2B6DE8; }
.control-red { --control:#C9404B; }
.control-amber { --control:#D98B16; }
.control-green { --control:#238A57; }

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

button[data-baseweb="tab"] {
    font-size: .75rem !important;
    font-weight: 750 !important;
    padding-top: .45rem !important;
    padding-bottom: .45rem !important;
}

[data-testid="stVerticalBlock"] {
    gap: .55rem;
}

@media (prefers-reduced-motion: reduce) {
    .action-title,
    .action-kpi,
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
def action_kpi(label, value, subtitle, icon, css_class):
    st.markdown(
        (
            f'<div class="action-kpi {css_class}">'
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


def action_insight(label, value, note):
    st.markdown(
        (
            '<div class="action-insight">'
            f'<div class="label">{label}</div>'
            f'<div class="value">{value}</div>'
            f'<div class="note">{note}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def note_box(title, body, tone="blue"):
    tone_class = "" if tone == "blue" else tone

    st.markdown(
        (
            f'<div class="action-note {tone_class}">'
            f'<div class="title">{title}</div>'
            f'<div class="body">{body}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def control_card(title, body, css_class):
    st.markdown(
        (
            f'<div class="control-card {css_class}">'
            f'<div class="ctitle">{title}</div>'
            f'<div class="cbody">{body}</div>'
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


def blank_mask(series):
    return (
        series.isna()
        | series.astype(str).str.strip().eq("")
    )


def compact_table_height(row_count, max_visible_rows=8, row_height=30):
    visible_rows = min(
        max(int(row_count), 1),
        max_visible_rows,
    )
    return 38 + (visible_rows * row_height)


def add_issue(
    collector,
    frame,
    mask,
    priority,
    issue,
    issue_code,
):
    if mask is None or not mask.any():
        return

    cols = [
        col
        for col in [
            "Activity Date",
            "Campus",
            "Institution / Event Name",
            "City",
            "State",
            "Activity Type",
            "Activity Owner",
            "Priority",
            "Status",
            "Planned Student Reach",
            "Actual Student Reach",
            "Participation Type",
        ]
        if col in frame.columns
    ]

    temp = frame.loc[
        mask,
        cols,
    ].copy()

    temp.insert(
        0,
        "Issue Code",
        issue_code,
    )

    temp.insert(
        0,
        "Dashboard Issue",
        issue,
    )

    temp.insert(
        0,
        "Issue Priority",
        priority,
    )

    collector.append(temp)


# =========================================================
# LOAD DATA
# =========================================================
df = load_data()


# =========================================================
# HEADER
# =========================================================
header_html = (
    '<div class="action-header">'
    '<div class="action-eyebrow">PGDM Outreach Intelligence</div>'
    '<div class="action-title-row">'
    '<div class="action-title-wrap">'
    '<div class="action-title">Action Center</div>'
    '</div>'
    '<div class="action-live">● LIVE GOOGLE SHEET</div>'
    '</div>'
    '<div class="action-subtitle">'
    'Execution exceptions, missing planning information and follow-up actions.'
    '</div>'
    '<div class="action-accent"></div>'
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
        key="action_page_campus",
    )

with f2:
    activity_values = (
        ["All"] + sorted(df["Activity Type"].dropna().unique().tolist())
        if "Activity Type" in df.columns else ["All"]
    )
    activity_filter = st.selectbox(
        "Activity Type",
        activity_values,
        key="action_page_activity",
    )

with f3:
    segment_values = (
        ["All"] + sorted(df["Target Segment"].dropna().unique().tolist())
        if "Target Segment" in df.columns else ["All"]
    )
    segment_filter = st.selectbox(
        "Target Segment",
        segment_values,
        key="action_page_segment",
    )

with f4:
    owner_values = (
        ["All"] + sorted(df["Activity Owner"].dropna().unique().tolist())
        if "Activity Owner" in df.columns else ["All"]
    )
    owner_filter = st.selectbox(
        "Owner",
        owner_values,
        key="action_page_owner",
    )

with f5:
    status_values = (
        ["All"] + sorted(df["Status"].dropna().unique().tolist())
        if "Status" in df.columns else ["All"]
    )
    status_filter = st.selectbox(
        "Status",
        status_values,
        key="action_page_status",
    )

with f6:
    priority_values = (
        ["All"] + sorted(df["Priority"].dropna().unique().tolist())
        if "Priority" in df.columns else ["All"]
    )
    priority_filter = st.selectbox(
        "Priority",
        priority_values,
        key="action_page_priority",
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
            key="action_page_date",
        )
    else:
        st.text_input(
            "Date Range",
            value="",
            disabled=True,
            key="action_page_date_text",
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
        "Selected filters ke liye koi Action Center data available nahi hai."
    )
    st.stop()


# =========================================================
# EXCEPTION LOGIC
# One activity can legitimately generate multiple exceptions.
# No artificial zero-fill is used for missing planning/reach values.
# =========================================================
today = pd.Timestamp.today().normalize()
issues = []

if "Status" in f.columns:
    open_mask = ~f["Status"].isin(CLOSED_STATUSES)
else:
    open_mask = pd.Series(
        True,
        index=f.index,
    )

# HIGH: past activity date but status remains open
if "Activity Date" in f.columns:
    add_issue(
        issues,
        f,
        (
            f["Activity Date"].notna()
            & f["Activity Date"].lt(today)
            & open_mask
        ),
        "High",
        "Past activity date but status is still open",
        "PAST_DATE_OPEN",
    )

# HIGH: high-priority activity missing owner
if {
    "Priority",
    "Activity Owner",
}.issubset(f.columns):
    add_issue(
        issues,
        f,
        (
            f["Priority"].eq("High")
            & blank_mask(f["Activity Owner"])
        ),
        "High",
        "High-priority activity has no activity owner",
        "HIGH_PRIORITY_NO_OWNER",
    )

# HIGH: upcoming High priority missing institution/event
if {
    "Activity Date",
    "Priority",
    "Institution / Event Name",
}.issubset(f.columns):
    add_issue(
        issues,
        f,
        (
            f["Activity Date"].notna()
            & f["Activity Date"].ge(today)
            & f["Priority"].eq("High")
            & blank_mask(f["Institution / Event Name"])
        ),
        "High",
        "High-priority upcoming activity is missing institution/event",
        "HIGH_PRIORITY_NO_INSTITUTION",
    )

# MEDIUM: planned student reach missing
if "Planned Student Reach" in f.columns:
    add_issue(
        issues,
        f,
        blank_mask(f["Planned Student Reach"]),
        "Medium",
        "Planned student reach is missing",
        "PLANNED_REACH_MISSING",
    )

# MEDIUM: actual reach entered but status still open
if {
    "Actual Student Reach",
    "Status",
}.issubset(f.columns):
    actual_entered = (
        f["Actual Student Reach"].notna()
        & pd.to_numeric(
            f["Actual Student Reach"],
            errors="coerce",
        ).notna()
    )

    add_issue(
        issues,
        f,
        (
            actual_entered
            & open_mask
        ),
        "Medium",
        "Actual reach entered but activity status is still open",
        "ACTUAL_REACH_STATUS_OPEN",
    )

# MEDIUM: future activity missing activity owner
if {
    "Activity Date",
    "Activity Owner",
}.issubset(f.columns):
    add_issue(
        issues,
        f,
        (
            f["Activity Date"].notna()
            & f["Activity Date"].ge(today)
            & blank_mask(f["Activity Owner"])
        ),
        "Medium",
        "Upcoming activity is missing activity owner",
        "UPCOMING_OWNER_MISSING",
    )

# MEDIUM: participation type missing
if "Participation Type" in f.columns:
    add_issue(
        issues,
        f,
        blank_mask(f["Participation Type"]),
        "Medium",
        "Participation type is missing",
        "PARTICIPATION_MISSING",
    )

# LOW: priority missing
if "Priority" in f.columns:
    add_issue(
        issues,
        f,
        blank_mask(f["Priority"]),
        "Low",
        "Priority is not captured",
        "PRIORITY_MISSING",
    )

# LOW: city missing
if "City" in f.columns:
    add_issue(
        issues,
        f,
        blank_mask(f["City"]),
        "Low",
        "City is missing",
        "CITY_MISSING",
    )

# LOW: state missing
if "State" in f.columns:
    add_issue(
        issues,
        f,
        blank_mask(f["State"]),
        "Low",
        "State is missing",
        "STATE_MISSING",
    )

# LOW: activity type missing
if "Activity Type" in f.columns:
    add_issue(
        issues,
        f,
        blank_mask(f["Activity Type"]),
        "Low",
        "Activity type is missing",
        "ACTIVITY_TYPE_MISSING",
    )


if issues:
    exceptions = pd.concat(
        issues,
        ignore_index=True,
    )
else:
    exceptions = pd.DataFrame(
        columns=[
            "Issue Priority",
            "Dashboard Issue",
            "Issue Code",
        ]
    )


# =========================================================
# METRICS
# =========================================================
priority_counts = (
    exceptions["Issue Priority"]
    .value_counts()
    if not exceptions.empty
    else pd.Series(dtype=int)
)

high_count = int(
    priority_counts.get(
        "High",
        0,
    )
)

medium_count = int(
    priority_counts.get(
        "Medium",
        0,
    )
)

low_count = int(
    priority_counts.get(
        "Low",
        0,
    )
)

total_exceptions = int(
    len(exceptions)
)

affected_rows = (
    int(
        exceptions.index.nunique()
    )
    if not exceptions.empty
    else 0
)

issue_types = (
    int(
        exceptions["Issue Code"]
        .nunique()
    )
    if not exceptions.empty
    else 0
)


# =========================================================
# KPI ROW
# =========================================================
k1, k2, k3, k4, k5 = st.columns(
    5,
    gap="small",
)

with k1:
    action_kpi(
        "High Priority",
        f"{high_count:,}",
        "Immediate action exceptions",
        "!",
        "kpi-red",
    )

with k2:
    action_kpi(
        "Medium Priority",
        f"{medium_count:,}",
        "Planning / update gaps",
        "◆",
        "kpi-amber",
    )

with k3:
    action_kpi(
        "Low Priority",
        f"{low_count:,}",
        "Data-quality gaps",
        "○",
        "kpi-green",
    )

with k4:
    action_kpi(
        "Issue Types",
        f"{issue_types:,}",
        "Distinct exception rules",
        "≡",
        "kpi-violet",
    )

with k5:
    action_kpi(
        "Total Exceptions",
        f"{total_exceptions:,}",
        "One row can have multiple issues",
        "Σ",
        "kpi-blue",
    )


# =========================================================
# ROW 1 — EXCEPTION MIX + ACTION INTELLIGENCE
# =========================================================
left, right = st.columns(
    [2.25, 1.0],
    gap="medium",
)

with left:
    with st.container(border=True):
        card_header(
            "Exception Priority Mix",
            "Current Action Center exceptions by management priority.",
        )

        priority_df = pd.DataFrame(
            {
                "Priority": [
                    "High",
                    "Medium",
                    "Low",
                ],
                "Exceptions": [
                    high_count,
                    medium_count,
                    low_count,
                ],
            }
        )

        fig = px.bar(
            priority_df,
            x="Priority",
            y="Exceptions",
            color="Priority",
            text="Exceptions",
            color_discrete_map={
                "High": "#C9404B",
                "Medium": "#D98B16",
                "Low": "#238A57",
            },
            category_orders={
                "Priority": [
                    "High",
                    "Medium",
                    "Low",
                ]
            },
        )

        fig.update_traces(
            textposition="outside",
            textfont=dict(size=9),
            marker_line_width=0,
            cliponaxis=False,
        )

        fig.update_xaxes(title="")
        fig.update_yaxes(
            title="Exceptions",
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

        if total_exceptions > 0:
            high_share = round(
                high_count
                / total_exceptions
                * 100,
                1,
            )
        else:
            high_share = 0

        note_box(
            "Priority Insight",
            (
                f"{high_count} High-priority exceptions require immediate attention "
                f"({high_share}% of all exceptions). Medium issues should be fixed "
                f"before execution or closure, while Low issues are primarily data-quality gaps."
            ),
            "red",
        )


with right:
    with st.container(border=True):
        card_header(
            "Action Intelligence",
            "Fast management summary from the selected exception set.",
        )

        if exceptions.empty:
            action_insight(
                "Immediate attention",
                "0",
                "No exception generated under the current rules.",
            )
            action_insight(
                "Most common issue",
                "N/A",
                "No exception issue is available.",
            )
            action_insight(
                "Most affected campus",
                "N/A",
                "No exception campus is available.",
            )
            action_insight(
                "Most affected owner",
                "N/A",
                "No exception owner is available.",
            )
        else:
            issue_counts = (
                exceptions["Dashboard Issue"]
                .value_counts()
            )

            top_issue_count = int(
                issue_counts.iloc[0]
            )

            tied_issues = (
                issue_counts[
                    issue_counts.eq(
                        top_issue_count
                    )
                ]
                .index.astype(str)
                .tolist()
            )

            shown_issues = tied_issues[:3]
            extra_issues = max(
                0,
                len(tied_issues) - len(shown_issues),
            )

            top_issue_display = "; ".join(
                shown_issues
            )

            if extra_issues > 0:
                top_issue_display += (
                    f" +{extra_issues} more"
                )

            action_insight(
                "Immediate attention",
                f"{high_count}",
                "High-priority exception rows",
            )

            action_insight(
                "Most common issue",
                top_issue_display,
                (
                    f"{top_issue_count} exception rows each"
                    if len(tied_issues) > 1
                    else f"{top_issue_count} exception rows"
                ),
            )

            if (
                "Campus" in exceptions.columns
                and exceptions["Campus"].notna().any()
            ):
                campus_counts = (
                    exceptions["Campus"]
                    .dropna()
                    .value_counts()
                )

                top_campus_count = int(
                    campus_counts.iloc[0]
                )

                tied_campuses = (
                    campus_counts[
                        campus_counts.eq(
                            top_campus_count
                        )
                    ]
                    .index.astype(str)
                    .tolist()
                )

                shown_campuses = tied_campuses[:3]
                extra_campuses = max(
                    0,
                    len(tied_campuses) - len(shown_campuses),
                )

                campus_display = ", ".join(
                    shown_campuses
                )

                if extra_campuses > 0:
                    campus_display += (
                        f" +{extra_campuses} more"
                    )

                action_insight(
                    "Most affected campus",
                    campus_display,
                    (
                        f"{top_campus_count} exception rows each"
                        if len(tied_campuses) > 1
                        else f"{top_campus_count} exception rows"
                    ),
                )
            else:
                action_insight(
                    "Most affected campus",
                    "N/A",
                    "Campus data is not available for exceptions.",
                )

            if (
                "Activity Owner" in exceptions.columns
                and exceptions["Activity Owner"].notna().any()
            ):
                owner_counts = (
                    exceptions["Activity Owner"]
                    .dropna()
                    .value_counts()
                )

                top_owner_count = int(
                    owner_counts.iloc[0]
                )

                tied_owners = (
                    owner_counts[
                        owner_counts.eq(
                            top_owner_count
                        )
                    ]
                    .index.astype(str)
                    .tolist()
                )

                shown_owners = tied_owners[:3]
                extra_owners = max(
                    0,
                    len(tied_owners) - len(shown_owners),
                )

                owner_display = ", ".join(
                    shown_owners
                )

                if extra_owners > 0:
                    owner_display += (
                        f" +{extra_owners} more"
                    )

                action_insight(
                    "Most affected owner",
                    owner_display,
                    (
                        f"{top_owner_count} exception rows each"
                        if len(tied_owners) > 1
                        else f"{top_owner_count} exception rows"
                    ),
                )
            else:
                action_insight(
                    "Most affected owner",
                    "N/A",
                    "Owner data is not available for exceptions.",
                )


# =========================================================
# ROW 2 — ISSUE TYPE + CAMPUS
# =========================================================
c1, c2 = st.columns(
    2,
    gap="medium",
)

with c1:
    with st.container(border=True):
        card_header(
            "Exceptions by Issue Type",
            "Which control failures are generating the most Action Center rows.",
        )

        if exceptions.empty:
            st.info(
                "No exception issue types are available."
            )
        else:
            issue_type_df = (
                exceptions["Dashboard Issue"]
                .value_counts()
                .rename_axis("Issue")
                .reset_index(name="Exceptions")
                .sort_values("Exceptions")
            )

            fig = px.bar(
                issue_type_df,
                x="Exceptions",
                y="Issue",
                orientation="h",
                text="Exceptions",
            )

            fig.update_traces(
                marker_color="#7A56D8",
                textposition="outside",
                textfont=dict(size=8),
                marker_line_width=0,
                cliponaxis=False,
            )

            fig.update_xaxes(
                title="Exceptions",
                rangemode="tozero",
                showticklabels=False,
                ticks="",
                showgrid=False,
                zeroline=False,
            )

            fig.update_yaxes(title="")

            issue_chart_height = min(
                max(
                    250,
                    105 + len(issue_type_df) * 38,
                ),
                520,
            )

            st.plotly_chart(
                clean_chart(
                    fig,
                    issue_chart_height,
                    legend=False,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )

            top_issue_row = (
                issue_type_df.sort_values(
                    "Exceptions",
                    ascending=False,
                )
                .iloc[0]
            )

            note_box(
                "Issue-Type Insight",
                (
                    f'{top_issue_row["Issue"]} is currently the largest exception '
                    f'category with {int(top_issue_row["Exceptions"])} rows. '
                    f'Fixing the most common rule first will remove the largest '
                    f'block of Action Center exceptions.'
                ),
                "violet",
            )


with c2:
    with st.container(border=True):
        card_header(
            "Exceptions by Campus",
            "Exception concentration across campus teams.",
        )

        if (
            exceptions.empty
            or "Campus" not in exceptions.columns
            or not exceptions["Campus"].notna().any()
        ):
            st.info(
                "Campus exception data available nahi hai."
            )
        else:
            campus_issue_df = (
                exceptions["Campus"]
                .dropna()
                .value_counts()
                .rename_axis("Campus")
                .reset_index(name="Exceptions")
                .sort_values("Exceptions")
            )

            fig = px.bar(
                campus_issue_df,
                x="Exceptions",
                y="Campus",
                orientation="h",
                text="Exceptions",
            )

            fig.update_traces(
                marker_color="#2468B4",
                textposition="outside",
                textfont=dict(size=9),
                marker_line_width=0,
                cliponaxis=False,
            )

            fig.update_xaxes(
                title="Exceptions",
                rangemode="tozero",
                showticklabels=False,
                ticks="",
                showgrid=False,
                zeroline=False,
            )

            fig.update_yaxes(title="")

            campus_chart_height = min(
                max(
                    235,
                    115 + len(campus_issue_df) * 38,
                ),
                430,
            )

            st.plotly_chart(
                clean_chart(
                    fig,
                    campus_chart_height,
                    legend=False,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )

            top_campus_row = (
                campus_issue_df.sort_values(
                    "Exceptions",
                    ascending=False,
                )
                .iloc[0]
            )

            note_box(
                "Campus Exception Insight",
                (
                    f'{top_campus_row["Campus"]} currently has the highest exception '
                    f'volume with {int(top_campus_row["Exceptions"])} rows. '
                    f'Review whether these are concentrated in planning completeness, '
                    f'past-date closure or owner assignment.'
                ),
                "blue",
            )


# =========================================================
# ROW 3 — OWNER + PRIORITY BY CAMPUS
# =========================================================
r1, r2 = st.columns(
    2,
    gap="medium",
)

with r1:
    with st.container(border=True):
        card_header(
            "Exceptions by Owner",
            "Owner-level follow-up load from exception rows.",
        )

        if (
            exceptions.empty
            or "Activity Owner" not in exceptions.columns
            or not exceptions["Activity Owner"].notna().any()
        ):
            st.info(
                "Owner exception data available nahi hai."
            )
        else:
            owner_issue_df = (
                exceptions["Activity Owner"]
                .dropna()
                .value_counts()
                .rename_axis("Activity Owner")
                .reset_index(name="Exceptions")
                .sort_values("Exceptions")
                .tail(12)
            )

            fig = px.bar(
                owner_issue_df,
                x="Exceptions",
                y="Activity Owner",
                orientation="h",
                text="Exceptions",
            )

            fig.update_traces(
                marker_color="#159E8C",
                textposition="outside",
                textfont=dict(size=9),
                marker_line_width=0,
                cliponaxis=False,
            )

            fig.update_xaxes(
                title="Exceptions",
                rangemode="tozero",
                showticklabels=False,
                ticks="",
                showgrid=False,
                zeroline=False,
            )

            fig.update_yaxes(title="")

            owner_chart_height = min(
                max(
                    240,
                    110 + len(owner_issue_df) * 34,
                ),
                520,
            )

            st.plotly_chart(
                clean_chart(
                    fig,
                    owner_chart_height,
                    legend=False,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )

            top_owner_row = (
                owner_issue_df.sort_values(
                    "Exceptions",
                    ascending=False,
                )
                .iloc[0]
            )

            note_box(
                "Owner Follow-up Insight",
                (
                    f'{top_owner_row["Activity Owner"]} has the highest visible '
                    f'exception follow-up load with {int(top_owner_row["Exceptions"])} rows.'
                ),
                "green",
            )


with r2:
    with st.container(border=True):
        card_header(
            "Priority Mix by Campus",
            "High, Medium and Low exception pressure across campuses.",
        )

        if (
            exceptions.empty
            or "Campus" not in exceptions.columns
        ):
            st.info(
                "Campus-priority exception data available nahi hai."
            )
        else:
            campus_priority = (
                exceptions.dropna(
                    subset=["Campus"]
                )
                .groupby(
                    [
                        "Campus",
                        "Issue Priority",
                    ]
                )
                .size()
                .reset_index(name="Exceptions")
            )

            if campus_priority.empty:
                st.info(
                    "Campus-priority exception data available nahi hai."
                )
            else:
                campus_totals = (
                    campus_priority.groupby(
                        "Campus",
                        as_index=False,
                    )["Exceptions"]
                    .sum()
                    .sort_values(
                        "Exceptions",
                        ascending=False,
                    )
                )

                campus_order = (
                    campus_totals["Campus"]
                    .astype(str)
                    .tolist()
                )

                priority_chart_height = min(
                    max(
                        250,
                        120 + len(campus_order) * 42,
                    ),
                    460,
                )

                fig = px.bar(
                    campus_priority,
                    x="Exceptions",
                    y="Campus",
                    color="Issue Priority",
                    orientation="h",
                    barmode="group",
                    text="Exceptions",
                    color_discrete_map={
                        "High": "#C9404B",
                        "Medium": "#D98B16",
                        "Low": "#238A57",
                    },
                    category_orders={
                        "Issue Priority": [
                            "High",
                            "Medium",
                            "Low",
                        ]
                    },
                )

                fig.update_traces(
                    textposition="outside",
                    textfont=dict(size=9),
                    marker_line_width=0,
                    cliponaxis=False,
                )

                fig.update_xaxes(
                    title="Exceptions",
                    rangemode="tozero",
                    showticklabels=False,
                    ticks="",
                    showgrid=False,
                    zeroline=False,
                )

                fig.update_yaxes(
                    title="",
                    categoryorder="array",
                    categoryarray=campus_order,
                    autorange="reversed",
                )

                st.plotly_chart(
                    clean_chart(
                        fig,
                        priority_chart_height,
                        legend=True,
                    ),
                    width="stretch",
                    config=CHART_CONFIG,
                )

                high_campus = (
                    campus_priority[
                        campus_priority["Issue Priority"].eq("High")
                    ]
                    .sort_values(
                        "Exceptions",
                        ascending=False,
                    )
                )

                if high_campus.empty:
                    high_message = (
                        "No High-priority campus exception is currently generated."
                    )
                else:
                    highest_high_count = int(
                        high_campus["Exceptions"].max()
                    )

                    tied_high_campuses = (
                        high_campus.loc[
                            high_campus["Exceptions"].eq(
                                highest_high_count
                            ),
                            "Campus",
                        ]
                        .astype(str)
                        .tolist()
                    )

                    shown_high_campuses = tied_high_campuses[:3]
                    extra_high_campuses = max(
                        0,
                        len(tied_high_campuses)
                        - len(shown_high_campuses),
                    )

                    high_names = ", ".join(
                        shown_high_campuses
                    )

                    if extra_high_campuses > 0:
                        high_names += (
                            f" +{extra_high_campuses} more"
                        )

                    if len(tied_high_campuses) == 1:
                        high_message = (
                            f"{high_names} has the highest High-priority "
                            f"exception count ({highest_high_count})."
                        )
                    else:
                        high_message = (
                            f"{high_names} jointly have the highest High-priority "
                            f"exception count ({highest_high_count} each)."
                        )

                note_box(
                    "Campus Priority Insight",
                    high_message,
                    "red",
                )


# =========================================================
# EXECUTION EXCEPTIONS TABLE
# =========================================================
st.markdown(
    '<div class="table-heading">Execution Exceptions</div>'
    '<div class="table-subheading">'
    'Each row represents one exception rule hit. A single outreach activity can appear more than once when multiple controls fail.'
    '</div>',
    unsafe_allow_html=True,
)

if exceptions.empty:
    st.success(
        "Current filters ke liye koi Action Center exception nahi hai."
    )
else:
    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3,
    }

    exceptions["_PriorityOrder"] = (
        exceptions["Issue Priority"]
        .map(priority_order)
        .fillna(9)
    )

    sort_cols = [
        "_PriorityOrder",
    ]

    if "Activity Date" in exceptions.columns:
        sort_cols.append(
            "Activity Date"
        )

    exceptions_sorted = (
        exceptions.sort_values(
            sort_cols,
            ascending=True,
        )
        .drop(
            columns=["_PriorityOrder"]
        )
    )

    high_tab, medium_tab, low_tab, all_tab = st.tabs(
        [
            f"High ({high_count})",
            f"Medium ({medium_count})",
            f"Low ({low_count})",
            f"All Exceptions ({total_exceptions})",
        ]
    )

    display_cols = [
        "Issue Priority",
        "Dashboard Issue",
        "Activity Date",
        "Campus",
        "Institution / Event Name",
        "Activity Type",
        "Activity Owner",
        "Status",
        "Priority",
        "Planned Student Reach",
        "Actual Student Reach",
    ]

    display_cols = [
        col
        for col in display_cols
        if col in exceptions_sorted.columns
    ]

    column_config = {
        "Issue Priority": st.column_config.TextColumn(
            "Issue Priority",
            width="small",
        ),
        "Dashboard Issue": st.column_config.TextColumn(
            "Dashboard Issue",
            width="large",
        ),
        "Activity Date": st.column_config.DateColumn(
            "Activity Date",
            format="DD MMM YY",
            width="small",
        ),
        "Campus": st.column_config.TextColumn(
            "Campus",
            width="small",
        ),
        "Institution / Event Name": st.column_config.TextColumn(
            "Institution / Event",
            width="large",
        ),
        "Activity Type": st.column_config.TextColumn(
            "Activity Type",
            width="medium",
        ),
        "Activity Owner": st.column_config.TextColumn(
            "Activity Owner",
            width="medium",
        ),
        "Status": st.column_config.TextColumn(
            "Status",
            width="small",
        ),
        "Priority": st.column_config.TextColumn(
            "Activity Priority",
            width="small",
        ),
        "Planned Student Reach": st.column_config.NumberColumn(
            "Planned Reach",
            format="%d",
            width="small",
        ),
        "Actual Student Reach": st.column_config.NumberColumn(
            "Actual Reach",
            format="%d",
            width="small",
        ),
    }

    high_view = exceptions_sorted[
        exceptions_sorted["Issue Priority"].eq("High")
    ][display_cols]

    medium_view = exceptions_sorted[
        exceptions_sorted["Issue Priority"].eq("Medium")
    ][display_cols]

    low_view = exceptions_sorted[
        exceptions_sorted["Issue Priority"].eq("Low")
    ][display_cols]

    all_view = exceptions_sorted[
        display_cols
    ]

    with high_tab:
        st.dataframe(
            high_view,
            width="stretch",
            hide_index=True,
            height=compact_table_height(
                len(high_view),
                max_visible_rows=8,
            ),
            row_height=30,
            column_config=column_config,
        )

    with medium_tab:
        st.dataframe(
            medium_view,
            width="stretch",
            hide_index=True,
            height=compact_table_height(
                len(medium_view),
                max_visible_rows=8,
            ),
            row_height=30,
            column_config=column_config,
        )

    with low_tab:
        st.dataframe(
            low_view,
            width="stretch",
            hide_index=True,
            height=compact_table_height(
                len(low_view),
                max_visible_rows=8,
            ),
            row_height=30,
            column_config=column_config,
        )

    with all_tab:
        st.dataframe(
            all_view,
            width="stretch",
            hide_index=True,
            height=compact_table_height(
                len(all_view),
                max_visible_rows=9,
            ),
            row_height=30,
            column_config=column_config,
        )


# =========================================================
# RECOMMENDED OUTREACH CONTROLS
# =========================================================
st.markdown(
    '<div class="table-heading">Recommended Outreach Controls</div>'
    '<div class="table-subheading">'
    'Operational controls aligned to the Action Center exception logic.'
    '</div>',
    unsafe_allow_html=True,
)

ctrl1, ctrl2, ctrl3, ctrl4 = st.columns(
    4,
    gap="small",
)

with ctrl1:
    control_card(
        "Before Event",
        (
            "Activity date, institution/event, owner, priority and planned student "
            "reach should be captured before field execution."
        ),
        "control-blue",
    )

with ctrl2:
    control_card(
        "High-Priority Governance",
        (
            "Every High-priority activity should have an owner and institution/event "
            "clearly assigned before the activity date."
        ),
        "control-red",
    )

with ctrl3:
    control_card(
        "After Event",
        (
            "Actual reach and activity status should be updated promptly after execution "
            "so completed work does not remain open in the calendar."
        ),
        "control-green",
    )

with ctrl4:
    control_card(
        "Data Quality",
        (
            "Participation type, city, state and activity type should be completed to "
            "keep geography, segment and resource analysis reliable."
        ),
        "control-amber",
    )


# =========================================================
# FINAL MANAGEMENT RECOMMENDATION
# =========================================================
if total_exceptions == 0:
    recommendation = (
        "No exception is currently generated for the selected view. Continue enforcing "
        "the same pre-event and post-event controls."
    )
else:
    issue_counts = (
        exceptions["Dashboard Issue"]
        .value_counts()
    )

    top_issue = issue_counts.index[0]
    top_issue_count = int(
        issue_counts.iloc[0]
    )

    recommendation = (
        f"Start with {high_count} High-priority exceptions. Then address the most common "
        f"exception — '{top_issue}' ({top_issue_count} rows) — because resolving that "
        f"single control gap will remove the largest number of Action Center rows. "
        f"After that, close Medium planning/update gaps and finally clean Low-priority "
        f"data-quality fields."
    )

note_box(
    "Action Center Management Recommendation",
    recommendation,
    "blue",
)
