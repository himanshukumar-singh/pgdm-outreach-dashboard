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
page_config("Outreach Calendar")
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
    padding-bottom: 5.0rem !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 92% 2%, rgba(43,109,232,.055), transparent 28%),
        linear-gradient(180deg, #F7F9FC 0%, #F3F6FA 100%) !important;
}

header[data-testid="stHeader"] {
    background: rgba(247,249,252,.92) !important;
}

/* ---------- Narrow sidebar + moving Jaipuria block ---------- */
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
    animation: calendarBrandMotion 3.8s ease-in-out infinite alternate;
}

[data-testid="stSidebar"] .brand-sub {
    animation-delay: .18s;
    color: #A9C9EF !important;
    font-size: .72rem !important;
    line-height: 1.35 !important;
}

@keyframes calendarBrandMotion {
    from { transform: translateX(-6px); }
    to   { transform: translateX(24px); }
}

[data-testid="stSidebar"] .stPageLink a {
    padding: .56rem .62rem !important;
    margin-bottom: .14rem !important;
    font-size: .90rem !important;
}

/* ---------- Moving page title ---------- */
.calendar-header {
    transform: translateY(-13px);
    margin-bottom: -8px;
}

.calendar-eyebrow {
    color: #2B6DE8;
    font-size: .67rem;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
    margin-bottom: .05rem;
}

.calendar-title-row {
    position: relative;
    width: 100%;
    padding-right: 10.8rem;
}

.calendar-title-wrap {
    position: relative;
    width: 100%;
    height: 1.72rem;
    overflow: hidden;
    white-space: nowrap;
}

.calendar-title {
    position: absolute;
    top: 0;
    width: max-content;
    color: #0F2A45;
    font-size: 1.28rem;
    font-weight: 850;
    letter-spacing: -.02em;
    line-height: 1.02;
    white-space: nowrap;
    animation: calendarTitleShuttle 6.3s linear infinite alternate;
}

@keyframes calendarTitleShuttle {
    0% {
        left: 0%;
        transform: translateX(-105%);
    }
    100% {
        left: 100%;
        transform: translateX(4%);
    }
}

.calendar-live {
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

.calendar-subtitle {
    color: #71839A;
    font-size: .86rem;
    margin-top: .02rem;
}

.calendar-accent {
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

/* ---------- Calendar KPI cards ---------- */
.cal-kpi {
    position: relative;
    overflow: hidden;
    min-height: 94px;
    border-radius: 14px;
    padding: .64rem .72rem .60rem .72rem;
    background: linear-gradient(145deg, #FFF 0%, var(--wash) 100%);
    border: 1px solid var(--border);
    box-shadow: 0 6px 18px rgba(15,42,69,.045);
    animation: calFloat 2.15s ease-in-out infinite;
}

.cal-kpi::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 0;
    width: 4px;
    background: linear-gradient(180deg, var(--accent), var(--accent2));
}

.cal-kpi::after {
    content: "";
    position: absolute;
    width: 82px;
    height: 82px;
    border-radius: 50%;
    right: -32px;
    top: -34px;
    background: radial-gradient(circle, var(--bubble) 0%, rgba(255,255,255,0) 72%);
}

.cal-kpi .icon {
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

.cal-kpi .label {
    position: relative;
    z-index: 2;
    color: #60758C;
    font-size: .66rem;
    font-weight: 850;
    white-space: nowrap;
}

.cal-kpi .value {
    position: relative;
    z-index: 2;
    color: #0F2A45;
    font-size: 1.72rem;
    font-weight: 900;
    line-height: 1;
    margin-top: .18rem;
}

.cal-kpi .sub {
    position: relative;
    z-index: 2;
    color: #8293A8;
    font-size: .60rem;
    margin-top: .17rem;
}

.cal-kpi .mini-line {
    position: absolute;
    left: .72rem;
    right: .72rem;
    bottom: .36rem;
    height: 2px;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: .18;
}

@keyframes calFloat {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-5px); }
}

.kpi-red {
    --accent:#C9404B; --accent2:#F07A83; --wash:#FFF5F6;
    --border:#F4DADC; --bubble:#FBE4E6; --iconbg:#FFF0F1;
}
.kpi-cyan {
    --accent:#0891B2; --accent2:#22D3EE; --wash:#F0FBFD;
    --border:#D2F0F6; --bubble:#D8F5FA; --iconbg:#E6F9FC;
}
.kpi-violet {
    --accent:#7C3AED; --accent2:#A78BFA; --wash:#F7F3FF;
    --border:#E6DBFF; --bubble:#E9DEFF; --iconbg:#F0E9FF;
}
.kpi-amber {
    --accent:#D98B16; --accent2:#FBBF24; --wash:#FFF9EE;
    --border:#F6E6C4; --bubble:#FFF0CF; --iconbg:#FFF5DF;
}
.kpi-green {
    --accent:#238A57; --accent2:#4ADE80; --wash:#F2FAF5;
    --border:#D6EFDF; --bubble:#DCF4E4; --iconbg:#EAF8EF;
}

/* ---------- Section/card styling ---------- */
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

/* ---------- Insight cards ---------- */
.cal-insight {
    min-height: 96px;
    padding: .58rem .64rem;
    border-radius: 11px;
    border: 1px solid #DFE7F0;
    background: #FFFFFF;
    box-shadow: 0 4px 12px rgba(15,42,69,.025);
    margin-bottom: .16rem;
}

.cal-insight .label {
    font-size: .64rem;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: .04em;
    color: #74879D;
}

.cal-insight .value {
    font-size: .88rem;
    font-weight: 900;
    color: #0F2A45;
    margin-top: .12rem;
}

.cal-insight .note {
    color: #7E90A6;
    font-size: .62rem;
    line-height: 1.42;
    margin-top: .18rem;
}

.cal-action {
    margin-top: .25rem;
    padding: .68rem .74rem;
    border-radius: 10px;
    background: linear-gradient(90deg, #FFF7EA 0%, #FFFDFC 100%);
    border: 1px solid #F3E0BB;
    border-left: 4px solid #D98B16;
}

.cal-action .title {
    color: #6C4A16;
    font-size: .69rem;
    font-weight: 850;
}

.cal-action .body {
    color: #796B55;
    font-size: .70rem;
    line-height: 1.42;
    margin-top: .18rem;
    overflow-wrap: anywhere;
}
/* =====================================================
   Overview-style equal chart insights
   Same pattern used on the working Overview page
   ===================================================== */

.chart-insight {
    margin-top: .10rem;
    padding: .48rem .58rem;
    border-radius: 10px;
    background: linear-gradient(90deg, #F2F7FF 0%, #F8FBFF 100%);
    border: 1px solid #DDE8F7;
    border-left: 4px solid #2B6DE8;
    min-height: 64px;
}

.chart-insight.amber {
    background: linear-gradient(90deg, #FFF8EB 0%, #FFFDFC 100%);
    border-color: #F4E2BF;
    border-left-color: #D98B16;
}

.chart-insight .ititle {
    color: #153A5F;
    font-size: .70rem;
    font-weight: 850;
    margin-bottom: .18rem;
}

.chart-insight .ibody {
    color: #60758C;
    font-size: .64rem;
    line-height: 1.34;
}

/* Exact equal-height insight pattern from Overview */
.chart-insight.status-equal {
    height: 86px;
    min-height: 86px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

/* Upper summary row — exact Overview-style alignment */
.calendar-pair-marker {
    display: none;
}

/* Same row-stretch technique used by the working Overview status section */
div[data-testid="stHorizontalBlock"]:has(.calendar-pair-marker) {
    align-items: stretch !important;
}

/* Both outer bordered cards share the same baseline */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.calendar-pair-marker) {
    min-height: 460px !important;
    height: auto !important;
    overflow: visible !important;
    padding-bottom: .50rem !important;
}

/* Card content becomes a vertical flex column */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.calendar-pair-marker)
> div[data-testid="stVerticalBlock"] {
    min-height: 444px !important;
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: visible !important;
    padding-bottom: 0 !important;
}

/* Insight stays at the bottom of each bordered card */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.calendar-pair-marker)
div[data-testid="stElementContainer"]:has(.calendar-bottom-insight) {
    margin-top: auto !important;
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.calendar-pair-marker)
.calendar-bottom-insight {
    margin-bottom: 0 !important;
}

.calendar-bottom-safe-space {
    height: 8px;
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
    border: 1px solid #D8E2EE !important;
    border-radius: 12px !important;
    overflow: hidden;
    background: #FFFFFF !important;
    box-shadow: 0 6px 18px rgba(15,42,69,.04);
}

/* Compact professional Activity Schedule table */
[data-testid="stDataFrame"] [role="columnheader"] {
    background: #F3F7FC !important;
    color: #405B77 !important;
    font-size: .67rem !important;
    font-weight: 800 !important;
    letter-spacing: .015em !important;
}

[data-testid="stDataFrame"] [role="gridcell"] {
    color: #29445F !important;
    font-size: .65rem !important;
}

/* ---------- Tabs ---------- */
button[data-baseweb="tab"] {
    font-size: .75rem !important;
    font-weight: 750 !important;
    padding-top: .45rem !important;
    padding-bottom: .45rem !important;
}

/* ---------- Reduce vertical gaps ---------- */
[data-testid="stVerticalBlock"] {
    gap: .55rem;
}

@media (prefers-reduced-motion: reduce) {
    .calendar-title,
    .cal-kpi,
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
def calendar_kpi(label, value, subtitle, icon, css_class):
    st.markdown(
        (
            f'<div class="cal-kpi {css_class}">'
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


def calendar_insight(label, value, note):
    st.markdown(
        (
            '<div class="cal-insight">'
            f'<div class="label">{label}</div>'
            f'<div class="value">{value}</div>'
            f'<div class="note">{note}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def action_note(title, body):
    st.markdown(
        (
            '<div class="cal-action">'
            f'<div class="title">{title}</div>'
            f'<div class="body">{body}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def paired_action_note(title, body):
    st.markdown(
        (
            '<div class="cal-action calendar-bottom-insight">'
            f'<div class="title">{title}</div>'
            f'<div class="body">{body}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def status_equal_insight(title, text, tone="blue"):
    tone_class = "" if tone == "blue" else tone
    st.markdown(
        (
            f'<div class="chart-insight status-equal {tone_class}">'
            f'<div class="ititle">{title}</div>'
            f'<div class="ibody">{text}</div>'
            f'</div>'
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


def readiness_score(frame):
    if frame.empty:
        return None, 0

    preferred_fields = [
        "Institution / Event Name",
        "City",
        "Activity Type",
        "Activity Owner",
        "Priority",
        "Planned Student Reach",
    ]

    available_fields = [
        col for col in preferred_fields
        if col in frame.columns
    ]

    if not available_fields:
        return None, 0

    row_scores = (
        frame[available_fields]
        .notna()
        .mean(axis=1)
        .mul(100)
    )

    avg_score = round(float(row_scores.mean()), 1)
    low_readiness = int((row_scores < 75).sum())

    return avg_score, low_readiness


def show_schedule_table(frame, height=305):
    if frame.empty:
        st.info("Is view ke liye koi activity available nahi hai.")
        return

    visible_rows = min(
        max(len(frame), 1),
        10,
    )

    calculated_height = 40 + (
        visible_rows * 28
    )

    height = max(
        height,
        calculated_height,
    )

    columns = [
        "Activity Date",
        "Campus",
        "Institution / Event Name",
        "City",
        "Activity Type",
        "Activity Owner",
        "Priority",
        "Status",
        "Planned Student Reach",
        "Actual Student Reach",
    ]

    columns = [
        col for col in columns
        if col in frame.columns
    ]

    st.dataframe(
        frame[columns],
        width="stretch",
        hide_index=True,
        height=height,
        row_height=28,
        column_config={
            "Activity Date": st.column_config.DateColumn(
                "Date",
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
            "City": st.column_config.TextColumn(
                "City",
                width="small",
            ),
            "Activity Type": st.column_config.TextColumn(
                "Activity Type",
                width="medium",
            ),
            "Activity Owner": st.column_config.TextColumn(
                "Owner",
                width="medium",
            ),
            "Priority": st.column_config.TextColumn(
                "Priority",
                width="small",
            ),
            "Status": st.column_config.TextColumn(
                "Status",
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
        },
    )


# =========================================================
# LOAD DATA
# =========================================================
df = load_data()


# =========================================================
# HEADER
# =========================================================
header_html = (
    '<div class="calendar-header">'
    '<div class="calendar-eyebrow">PGDM Outreach Intelligence</div>'
    '<div class="calendar-title-row">'
    '<div class="calendar-title-wrap">'
    '<div class="calendar-title">Outreach Calendar</div>'
    '</div>'
    '<div class="calendar-live">● LIVE GOOGLE SHEET</div>'
    '</div>'
    '<div class="calendar-subtitle">'
    'Upcoming, overdue and scheduled outreach activity management.'
    '</div>'
    '<div class="calendar-accent"></div>'
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
        key="cal_campus",
    )

with f2:
    activity_values = (
        ["All"] + sorted(df["Activity Type"].dropna().unique().tolist())
        if "Activity Type" in df.columns else ["All"]
    )
    activity_filter = st.selectbox(
        "Activity Type",
        activity_values,
        key="cal_activity",
    )

with f3:
    segment_values = (
        ["All"] + sorted(df["Target Segment"].dropna().unique().tolist())
        if "Target Segment" in df.columns else ["All"]
    )
    segment_filter = st.selectbox(
        "Target Segment",
        segment_values,
        key="cal_segment",
    )

with f4:
    owner_values = (
        ["All"] + sorted(df["Activity Owner"].dropna().unique().tolist())
        if "Activity Owner" in df.columns else ["All"]
    )
    owner_filter = st.selectbox(
        "Owner",
        owner_values,
        key="cal_owner",
    )

with f5:
    status_values = (
        ["All"] + sorted(df["Status"].dropna().unique().tolist())
        if "Status" in df.columns else ["All"]
    )
    status_filter = st.selectbox(
        "Status",
        status_values,
        key="cal_status",
    )

with f6:
    priority_values = (
        ["All"] + sorted(df["Priority"].dropna().unique().tolist())
        if "Priority" in df.columns else ["All"]
    )
    priority_filter = st.selectbox(
        "Priority",
        priority_values,
        key="cal_priority",
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
            key="cal_date_range",
        )
    else:
        st.text_input(
            "Date Range",
            value="",
            disabled=True,
            key="cal_date_range_text",
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
        "No data is available for the selected filters."
    )
    st.stop()

if "Activity Date" not in f.columns:
    st.info("Activity Date column available nahi hai.")
    st.stop()


# =========================================================
# CALENDAR LOGIC — PRECISE DATE WINDOWS
# =========================================================
today = pd.Timestamp.today().normalize()

dated_mask = f["Activity Date"].notna()

if "Status" in f.columns:
    open_mask = ~f["Status"].isin(CLOSED_STATUSES)
else:
    open_mask = pd.Series(True, index=f.index)

overdue = f[
    dated_mask
    & open_mask
    & f["Activity Date"].lt(today)
].copy()

# "Next 7 Days" = today + next 6 dates (7 calendar days total)
next7_end = today + pd.Timedelta(days=6)

next7 = f[
    dated_mask
    & open_mask
    & f["Activity Date"].between(
        today,
        next7_end,
        inclusive="both",
    )
].copy()

# "Next 30 Days" = today + next 29 dates (30 calendar days total)
next30_end = today + pd.Timedelta(days=29)

next30 = f[
    dated_mask
    & open_mask
    & f["Activity Date"].between(
        today,
        next30_end,
        inclusive="both",
    )
].copy()

upcoming = f[
    dated_mask
    & open_mask
    & f["Activity Date"].ge(today)
].copy()

full_schedule = f[
    dated_mask
].copy()

high_priority_upcoming = (
    int(upcoming["Priority"].eq("High").sum())
    if "Priority" in upcoming.columns
    else 0
)

total_scheduled = int(dated_mask.sum())

avg_readiness, low_readiness_count = readiness_score(next30)


# =========================================================
# KPI ROW
# =========================================================
k1, k2, k3, k4, k5 = st.columns(5, gap="small")

with k1:
    calendar_kpi(
        "Past Due",
        f"{len(overdue):,}",
        "Open past-date activities",
        "!",
        "kpi-red",
    )

with k2:
    calendar_kpi(
        "Next 7 Days",
        f"{len(next7):,}",
        "7 calendar days incl. today",
        "7",
        "kpi-cyan",
    )

with k3:
    calendar_kpi(
        "Next 30 Days",
        f"{len(next30):,}",
        "30 calendar days incl. today",
        "30",
        "kpi-violet",
    )

with k4:
    calendar_kpi(
        "High Priority",
        f"{high_priority_upcoming:,}",
        "Upcoming high-priority actions",
        "★",
        "kpi-amber",
    )

with k5:
    calendar_kpi(
        "Total Scheduled",
        f"{total_scheduled:,}",
        "Dated activities in selection",
        "✓",
        "kpi-green",
    )


# =========================================================
# MANAGEMENT SUMMARY
# =========================================================
summary_left, summary_right = st.columns(
    [2.0, 1.15],
    gap="medium",
    vertical_alignment="top",
)

with summary_left:
    with st.container(border=True):
        st.markdown(
            '<span class="calendar-pair-marker"></span>',
            unsafe_allow_html=True,
        )
        card_header(
            "30-Day Outreach Load",
            "Open outreach activities scheduled during the next 30 calendar days.",
        )

        if next30.empty:
            st.info("Next 30 days me koi open activity available nahi hai.")
        else:
            daily_load = (
                next30.groupby("Activity Date")
                .size()
                .reset_index(name="Activities")
                .sort_values("Activity Date")
            )

            daily_load["Date Label"] = (
                daily_load["Activity Date"]
                .dt.strftime("%d %b")
            )

            fig = px.bar(
                daily_load,
                x="Date Label",
                y="Activities",
                text="Activities",
            )

            fig.update_traces(
                marker_color="#316FC4",
                textposition="outside",
                textfont=dict(size=9),
                marker_line_width=0,
            )

            daily_max = int(
                daily_load["Activities"].max()
            )

            fig.update_xaxes(
                title="",
                categoryorder="array",
                categoryarray=daily_load["Date Label"].tolist(),
                tickfont=dict(size=8.5),
            )

            fig.update_yaxes(
                title="Activities",
                range=[
                    0,
                    max(1, daily_max * 1.18),
                ],
                showticklabels=False,
                ticks="",
                showgrid=False,
                zeroline=False,
            )

            fig.update_layout(
                bargap=0.30,
            )

            st.plotly_chart(
                clean_chart(fig, 205, legend=False),
                width="stretch",
                config=CHART_CONFIG,
            )

            peak_row = daily_load.loc[
                daily_load["Activities"].idxmax()
            ]

            paired_action_note(
                "30-Day Load Insight",
                (
                    f'Peak scheduled day is {peak_row["Date Label"]} with '
                    f'{int(peak_row["Activities"])} open activities. '
                    f'{len(next30)} activities require execution during '
                    f'the next 30 calendar days.'
                ),
            )


with summary_right:
    with st.container(border=True):
        st.markdown(
            '<span class="calendar-pair-marker"></span>',
            unsafe_allow_html=True,
        )
        card_header(
            "Calendar Intelligence",
            "Immediate management actions from the selected calendar.",
        )

        # Resolve all four management metrics first.
        if upcoming.empty:
            next_activity_value = "No upcoming activity"
            next_activity_note = "No future open activity in the selected view."
        else:
            next_activity = (
                upcoming.sort_values("Activity Date")
                .iloc[0]
            )

            institution = next_activity.get(
                "Institution / Event Name",
                "Institution not captured",
            )

            campus = next_activity.get(
                "Campus",
                "Campus not captured",
            )

            next_activity_value = (
                next_activity["Activity Date"]
                .strftime("%d %b %Y")
            )
            next_activity_note = (
                f"{campus} • {institution}"
            )

        if (
            not next30.empty
            and "Campus" in next30.columns
            and next30["Campus"].notna().any()
        ):
            campus_load = (
                next30["Campus"]
                .value_counts()
            )

            busiest_campus = str(
                campus_load.index[0]
            )
            busiest_count = int(
                campus_load.iloc[0]
            )
            busiest_note = (
                f"{busiest_count} scheduled open activities"
            )
        else:
            busiest_campus = "N/A"
            busiest_note = "No campus activity in this window."

        if avg_readiness is None:
            readiness_value = "N/A"
            readiness_note = "Required planning fields are unavailable."
        else:
            readiness_value = (
                f"{avg_readiness:.1f}%"
            )
            readiness_note = (
                f"{low_readiness_count} next-30 activities below 75% completeness."
            )

        if overdue.empty:
            overdue_value = "None"
            overdue_note = "No open past-date activity."
        else:
            oldest_date = overdue[
                "Activity Date"
            ].min()

            overdue_days = int(
                (today - oldest_date).days
            )

            overdue_value = (
                f"{overdue_days} days"
            )
            overdue_note = (
                f'Oldest unresolved: '
                f'{oldest_date.strftime("%d %b %Y")}'
            )

        ci1, ci2 = st.columns(
            2,
            gap="small",
        )

        with ci1:
            calendar_insight(
                "Next activity",
                next_activity_value,
                next_activity_note,
            )

        with ci2:
            calendar_insight(
                "Busiest campus — next 30 days",
                busiest_campus,
                busiest_note,
            )

        ci3, ci4 = st.columns(
            2,
            gap="small",
        )

        with ci3:
            calendar_insight(
                "Planning readiness",
                readiness_value,
                readiness_note,
            )

        with ci4:
            calendar_insight(
                "Oldest overdue",
                overdue_value,
                overdue_note,
            )
        paired_action_note(
            "Calendar Intelligence Insight",
            (
                f"Next activity: {next_activity_value}. "
                f"{busiest_campus} carries the highest next-30-day open load. "
                + (
                    f"Planning readiness is {avg_readiness:.1f}%. "
                    if avg_readiness is not None
                    else ""
                )
                + (
                    f"Oldest unresolved activity is {overdue_value} overdue."
                    if not overdue.empty
                    else "There is currently no overdue open activity."
                )
            ),
        )


# =========================================================
# CAMPUS LOAD + PRIORITY MIX
# =========================================================
chart1, chart2 = st.columns(2, gap="medium")

with chart1:
    with st.container(border=True):
        card_header(
            "Campus Load — Next 30 Days",
            "Upcoming open activity volume by campus.",
        )

        if (
            next30.empty
            or "Campus" not in next30.columns
        ):
            st.info("Next 30 days ka campus load available nahi hai.")
        else:
            campus_load_df = (
                next30["Campus"]
                .dropna()
                .value_counts()
                .rename_axis("Campus")
                .reset_index(name="Activities")
                .sort_values("Activities")
            )

            if campus_load_df.empty:
                st.info("Campus data available nahi hai.")
            else:
                fig = px.bar(
                    campus_load_df,
                    x="Activities",
                    y="Campus",
                    orientation="h",
                    text="Activities",
                )

                fig.update_traces(
                    marker_color="#2C73B9",
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

                fig.update_yaxes(
                    title="",
                    tickfont=dict(size=9),
                )

                fig.update_layout(
                    bargap=0.34,
                )

                st.plotly_chart(
                    clean_chart(fig, 220, legend=False),
                    width="stretch",
                    config=CHART_CONFIG,
                )

                top_row = campus_load_df.iloc[-1]

                status_equal_insight(
                    "Campus Load Insight",
                    (
                        f'{top_row["Campus"]} carries the highest next-30-day '
                        f'field load with {int(top_row["Activities"])} activities.'
                    ),
                    "amber",
                )


with chart2:
    with st.container(border=True):
        card_header(
            "Priority Mix — Upcoming",
            "Upcoming open activities by priority.",
        )

        if (
            upcoming.empty
            or "Priority" not in upcoming.columns
        ):
            st.info("Upcoming priority data available nahi hai.")
        else:
            priority_df = (
                upcoming["Priority"]
                .fillna("Not Captured")
                .value_counts()
                .rename_axis("Priority")
                .reset_index(name="Activities")
            )

            priority_order = [
                "High",
                "Medium",
                "Low",
                "Not Captured",
            ]

            priority_df["Priority"] = pd.Categorical(
                priority_df["Priority"],
                categories=priority_order,
                ordered=True,
            )

            priority_df = (
                priority_df.sort_values("Priority")
                .dropna(subset=["Priority"])
            )

            color_map = {
                "High": "#D9534F",
                "Medium": "#E5A13A",
                "Low": "#2F9B68",
                "Not Captured": "#8A97A8",
            }

            if priority_df.empty:
                st.info("Priority values available nahi hain.")
            else:
                fig = px.bar(
                    priority_df,
                    x="Activities",
                    y="Priority",
                    orientation="h",
                    text="Activities",
                    color="Priority",
                    color_discrete_map=color_map,
                    category_orders={
                        "Priority": priority_order,
                    },
                )

                fig.update_traces(
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

                fig.update_yaxes(
                    title="",
                    categoryorder="array",
                    categoryarray=priority_order,
                    autorange="reversed",
                    tickfont=dict(size=9),
                )

                fig.update_layout(
                    bargap=0.34,
                )

                st.plotly_chart(
                    clean_chart(fig, 220, legend=False),
                    width="stretch",
                    config=CHART_CONFIG,
                )

                high_count = int(
                    upcoming["Priority"]
                    .eq("High")
                    .sum()
                )

                status_equal_insight(
                    "Priority Insight",
                    (
                        f"{high_count} upcoming activities are marked High priority. "
                        f"These should be checked first for owner, institution, "
                        f"planned reach and execution readiness."
                    ),
                    "amber",
                )


# =========================================================
# PROFESSIONAL SCHEDULE TABLE
# =========================================================
st.markdown(
    '<div class="table-heading">Activity Schedule</div>'
    '<div class="table-subheading">'
    'Use the tabs below to separate immediate execution, overdue follow-up and the complete dated schedule.'
    '</div>',
    unsafe_allow_html=True,
)

upcoming_sorted = upcoming.sort_values(
    "Activity Date"
).copy()

overdue_sorted = overdue.sort_values(
    "Activity Date"
).copy()

full_sorted = full_schedule.sort_values(
    "Activity Date"
).copy()

tab_upcoming, tab_overdue, tab_all = st.tabs(
    [
        f"Upcoming Open ({len(upcoming_sorted)})",
        f"Overdue ({len(overdue_sorted)})",
        f"Full Schedule ({len(full_sorted)})",
    ]
)

with tab_upcoming:
    show_schedule_table(
        upcoming_sorted,
        height=330,
    )

with tab_overdue:
    show_schedule_table(
        overdue_sorted,
        height=330,
    )

with tab_all:
    show_schedule_table(
        full_sorted,
        height=330,
    )


# =========================================================
# FINAL ACTION INSIGHT
# =========================================================
if overdue.empty:
    overdue_message = (
        "No open past-date activity currently needs status correction."
    )
else:
    overdue_message = (
        f"{len(overdue)} open activities have a past activity date and "
        f"need status/outcome updates."
    )

if avg_readiness is None:
    readiness_message = ""
else:
    readiness_message = (
        f" Next-30-day planning readiness is {avg_readiness:.1f}%."
    )

action_note(
    "Calendar Management Recommendation",
    (
        overdue_message
        + readiness_message
        + " Prioritise overdue closure first, then validate the next 7 days "
          "for owner availability, event details and planned student reach."
    ),
)

st.markdown(
    '<div class="calendar-bottom-safe-space"></div>',
    unsafe_allow_html=True,
)
