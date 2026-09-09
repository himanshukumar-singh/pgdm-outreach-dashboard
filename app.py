import html
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
page_config("Overview")
inject_css()
sidebar_nav()


# =========================================================
# OVERVIEW UI
# =========================================================
st.markdown(
    """
<style>
/* ---------- Main canvas ---------- */
.block-container {
    max-width: none !important;
    padding-top: 0.05rem !important;
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

/* ---------- Narrower sidebar ---------- */
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
    animation: brandMotion 3.8s ease-in-out infinite alternate;
}

[data-testid="stSidebar"] .brand-sub {
    animation-delay: .18s;
    color: #A9C9EF !important;
    font-size: .72rem !important;
    line-height: 1.35 !important;
}

@keyframes brandMotion {
    from { transform: translateX(-6px); }
    to   { transform: translateX(24px); }
}

[data-testid="stSidebar"] .stPageLink a {
    padding: .56rem .62rem !important;
    margin-bottom: .14rem !important;
    font-size: .90rem !important;
}

/* ---------- Header ---------- */
.overview-header {
    transform: translateY(-14px);
    margin-bottom: -8px;
}

.overview-eyebrow {
    color: #2B6DE8;
    font-size: .67rem;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
    margin-bottom: .05rem;
}

.overview-title-row {
    position: relative;
    width: 100%;
    padding-right: 11.3rem;
}

.overview-title-wrap {
    position: relative;
    width: 100%;
    height: 1.70rem;
    overflow: hidden;
    white-space: nowrap;
}

.overview-title {
    position: absolute;
    top: 0;
    width: max-content;
    color: #0F2A45;
    font-size: 1.28rem;
    font-weight: 850;
    letter-spacing: -.02em;
    line-height: 1.02;
    white-space: nowrap;
    animation: titleShuttle 6.5s linear infinite alternate;
}

@keyframes titleShuttle {
    0% {
        left: 0%;
        transform: translateX(-105%);
    }
    100% {
        left: 100%;
        transform: translateX(4%);
    }
}

.live-badge-custom {
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

.overview-subtitle {
    color: #71839A;
    font-size: .86rem;
    margin-top: .02rem;
}

.overview-accent {
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
.pro-kpi {
    position: relative;
    overflow: hidden;
    min-height: 94px;
    border-radius: 14px;
    padding: .64rem .72rem .60rem .72rem;
    background: linear-gradient(145deg, #FFF 0%, var(--wash) 100%);
    border: 1px solid var(--border);
    box-shadow: 0 6px 18px rgba(15,42,69,.045);
    animation: kpiFloat 2.05s ease-in-out infinite;
}

.pro-kpi::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 0;
    width: 4px;
    background: linear-gradient(180deg, var(--accent), var(--accent2));
}

.pro-kpi::after {
    content: "";
    position: absolute;
    width: 82px;
    height: 82px;
    border-radius: 50%;
    right: -32px;
    top: -34px;
    background: radial-gradient(circle, var(--bubble) 0%, rgba(255,255,255,0) 72%);
}

.pro-kpi .icon {
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

.pro-kpi .label {
    position: relative;
    z-index: 2;
    color: #60758C;
    font-size: .55rem;
    font-weight: 850;
    white-space: nowrap;
}

.pro-kpi .value {
    position: relative;
    z-index: 2;
    color: #0F2A45;
    font-size: 1.72rem;
    font-weight: 900;
    line-height: 1;
    margin-top: .18rem;
}

.pro-kpi .sub {
    position: relative;
    z-index: 2;
    color: #8293A8;
    font-size: .55rem;
    margin-top: .17rem;
}

.pro-kpi .mini-line {
    position: absolute;
    left: .72rem;
    right: .72rem;
    bottom: .36rem;
    height: 2px;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: .18;
}

@keyframes kpiFloat {
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

/* ---------- Professional chart cards ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid #DFE7F0 !important;
    border-radius: 14px !important;
    box-shadow: 0 6px 20px rgba(15,42,69,.035);
}

.chart-title {
    color: #0F2A45;
    font-size: 1.02rem;
    font-weight: 850;
    margin-bottom: .05rem;
}

.chart-subtitle {
    color: #7D8FA5;
    font-size: .74rem;
    margin-bottom: .28rem;
}

.chart-insight {
    margin-top: .10rem;
    padding: .66rem .72rem;
    border-radius: 10px;
    background: linear-gradient(90deg, #F2F7FF 0%, #F8FBFF 100%);
    border: 1px solid #DDE8F7;
    border-left: 4px solid #2B6DE8;
}

.chart-insight.teal {
    background: linear-gradient(90deg, #EFFBF8 0%, #F8FDFC 100%);
    border-color: #D5F0E9;
    border-left-color: #159E8C;
}

.chart-insight.violet {
    background: linear-gradient(90deg, #F6F2FF 0%, #FBF9FF 100%);
    border-color: #E5DBFF;
    border-left-color: #7C3AED;
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
    font-size: .72rem;
    line-height: 1.42;
}

/* ---------- Mini insight cards ---------- */
.mini-insight {
    min-height: 76px;
    background: #FFFFFF;
    border: 1px solid #DFE7F0;
    border-radius: 11px;
    padding: .62rem .68rem;
    box-shadow: 0 4px 12px rgba(15,42,69,.025);
}

.mini-insight .label {
    color: #74879D;
    font-size: .56rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .04em;
}

.mini-insight .value {
    color: #0F2A45;
    font-size: 1.06rem;
    font-weight: 900;
    margin-top: .14rem;
}

.mini-insight .note {
    color: #8A9AAD;
    font-size: .61rem;
    margin-top: .10rem;
}

/* ---------- Table ---------- */
.table-title {
    color: #0F2A45;
    font-size: 1.03rem;
    font-weight: 850;
    margin-top: .15rem;
}

.table-subtitle {
    color: #7D8FA5;
    font-size: .74rem;
    margin-bottom: .40rem;
}

/* Professional upcoming outreach table */
.upcoming-table-shell {
    border: 1px solid #DCE5EF;
    border-radius: 14px;
    background: #FFFFFF;
    box-shadow: 0 7px 22px rgba(15,42,69,.045);
    overflow: hidden;
}

.upcoming-table-scroll {
    width: 100%;
    max-height: 300px;
    overflow: auto;
    scrollbar-width: thin;
    scrollbar-color: #C7D4E2 transparent;
}

.upcoming-pro-table {
    width: 100%;
    min-width: 1040px;
    border-collapse: separate;
    border-spacing: 0;
    font-family: Arial, sans-serif;
}

.upcoming-pro-table thead th {
    position: sticky;
    top: 0;
    z-index: 4;
    padding: .40rem .44rem;
    background: linear-gradient(180deg, #F2F6FB 0%, #EAF1F8 100%);
    color: #415A73;
    border-bottom: 1px solid #DCE5EF;
    border-right: 1px solid #E5ECF4;
    font-size: .56rem;
    font-weight: 850;
    letter-spacing: .035em;
    text-transform: uppercase;
    white-space: nowrap;
    text-align: left;
}

.upcoming-pro-table tbody td {
    padding: .33rem .44rem;
    color: #334B63;
    border-bottom: 1px solid #E8EEF5;
    border-right: 1px solid #EEF2F7;
    font-size: .55rem;
    line-height: 1.18;
    vertical-align: middle;
    background: #FFFFFF;
    white-space: nowrap;
}

.upcoming-pro-table tbody tr:nth-child(even) td {
    background: #FBFCFE;
}

.upcoming-pro-table tbody tr:hover td {
    background: #EEF5FC;
}

.upcoming-pro-table thead th:last-child,
.upcoming-pro-table tbody td:last-child {
    border-right: none;
}

.upcoming-pro-table tbody tr:last-child td {
    border-bottom: none;
}

.upcoming-pro-table .institution-cell {
    min-width: 165px;
    max-width: 235px;
    white-space: normal;
    font-weight: 650;
    color: #153A5F;
}

.upcoming-pro-table .owner-cell {
    min-width: 105px;
    font-weight: 600;
}

.upcoming-pro-table .numeric-cell {
    text-align: right;
    font-variant-numeric: tabular-nums;
    font-weight: 650;
}

.upcoming-pro-table .date-cell {
    font-variant-numeric: tabular-nums;
    font-weight: 750;
    color: #234766;
}

.table-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 42px;
    padding: .16rem .34rem;
    border-radius: 999px;
    font-size: .53rem;
    font-weight: 850;
    border: 1px solid transparent;
    white-space: nowrap;
}

.badge-high {
    color: #245E9A;
    background: #EEF5FC;
    border-color: #D1E2F4;
}

.badge-medium {
    color: #9B620B;
    background: #FFF6E6;
    border-color: #F2D6A2;
}

.badge-low {
    color: #B4232C;
    background: #FFF0F1;
    border-color: #F4CDD0;
}

.badge-confirmed,
.badge-completed {
    color: #146844;
    background: #EDF9F3;
    border-color: #C8EBD8;
}

.badge-planned {
    color: #245E9A;
    background: #EEF5FC;
    border-color: #D1E2F4;
}

.badge-cancelled {
    color: #A8323C;
    background: #FFF1F2;
    border-color: #F2CFD2;
}

.badge-rescheduled {
    color: #95610A;
    background: #FFF7E7;
    border-color: #F0DDAE;
}

.badge-neutral {
    color: #53697F;
    background: #F2F5F8;
    border-color: #DDE5ED;
}

.upcoming-table-footer {
    display: flex;
    justify-content: space-between;
    gap: .8rem;
    padding: .36rem .50rem;
    background: #FAFCFE;
    border-top: 1px solid #E3EAF2;
    color: #7A8DA3;
    font-size: .55rem;
}

.upcoming-table-footer strong {
    color: #36526F;
    font-weight: 850;
}

/* Pull sections closer */
[data-testid="stVerticalBlock"] {
    gap: .55rem;
}

@media (prefers-reduced-motion: reduce) {
    .overview-title,
    .pro-kpi,
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
def professional_kpi(label, value, subtitle, icon, css_class):
    st.markdown(
        (
            f'<div class="pro-kpi {css_class}">'
            f'<div class="icon">{icon}</div>'
            f'<div class="label">{label}</div>'
            f'<div class="value">{value}</div>'
            f'<div class="sub">{subtitle}</div>'
            f'<div class="mini-line"></div>'
            f'</div>'
        ),
        unsafe_allow_html=True,
    )


def chart_header(title, subtitle):
    st.markdown(
        f'<div class="chart-title">{title}</div>'
        f'<div class="chart-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )


def chart_insight(title, text, tone="blue"):
    tone_class = "" if tone == "blue" else tone
    st.markdown(
        (
            f'<div class="chart-insight {tone_class}">'
            f'<div class="ititle">{title}</div>'
            f'<div class="ibody">{text}</div>'
            f'</div>'
        ),
        unsafe_allow_html=True,
    )


def mini_insight(label, value, note):
    st.markdown(
        (
            '<div class="mini-insight">'
            f'<div class="label">{label}</div>'
            f'<div class="value">{value}</div>'
            f'<div class="note">{note}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def _safe_text(value):
    if pd.isna(value):
        return "—"
    return html.escape(str(value).strip())


def _badge(value):
    label = _safe_text(value)

    if label == "—":
        return '<span class="table-badge badge-neutral">—</span>'

    css_value = str(value).strip().lower()

    badge_classes = {
        "high": "badge-high",
        "medium": "badge-medium",
        "low": "badge-low",
        "confirmed": "badge-confirmed",
        "planned": "badge-planned",
        "completed": "badge-completed",
        "cancelled": "badge-cancelled",
        "rescheduled": "badge-rescheduled",
    }

    css_class = badge_classes.get(
        css_value,
        "badge-neutral",
    )

    return (
        f'<span class="table-badge {css_class}">'
        f'{label}'
        f'</span>'
    )


def render_upcoming_table(frame, columns):
    labels = {
        "Activity Date": "Date",
        "Campus": "Campus",
        "Institution / Event Name": "Institution / Event",
        "City": "City",
        "Activity Type": "Activity Type",
        "Activity Owner": "Owner",
        "Priority": "Priority",
        "Status": "Status",
        "Planned Student Reach": "Planned Reach",
        "Actual Student Reach": "Actual Reach",
    }

    header_html = "".join(
        f"<th>{html.escape(labels.get(col, col))}</th>"
        for col in columns
    )

    rows = []

    for _, row in frame[columns].iterrows():
        cells = []

        for col in columns:
            value = row[col]

            if col == "Activity Date":
                if pd.isna(value):
                    cell = '<td class="date-cell">—</td>'
                else:
                    cell = (
                        '<td class="date-cell">'
                        f'{pd.Timestamp(value).strftime("%d %b %y")}'
                        '</td>'
                    )

            elif col == "Institution / Event Name":
                cell = (
                    '<td class="institution-cell">'
                    f'{_safe_text(value)}'
                    '</td>'
                )

            elif col == "Activity Owner":
                cell = (
                    '<td class="owner-cell">'
                    f'{_safe_text(value)}'
                    '</td>'
                )

            elif col in {"Priority", "Status"}:
                cell = f"<td>{_badge(value)}</td>"

            elif col in {
                "Planned Student Reach",
                "Actual Student Reach",
            }:
                numeric = pd.to_numeric(
                    pd.Series([value]),
                    errors="coerce",
                ).iloc[0]

                display_value = (
                    "—"
                    if pd.isna(numeric)
                    else f"{int(numeric):,}"
                )

                cell = (
                    '<td class="numeric-cell">'
                    f'{display_value}'
                    '</td>'
                )

            else:
                cell = f"<td>{_safe_text(value)}</td>"

            cells.append(cell)

        rows.append(
            "<tr>" + "".join(cells) + "</tr>"
        )

    high_count = (
        int(frame["Priority"].eq("High").sum())
        if "Priority" in frame.columns
        else 0
    )

    table_html = (
        '<div class="upcoming-table-shell">'
        '<div class="upcoming-table-scroll">'
        '<table class="upcoming-pro-table">'
        f'<thead><tr>{header_html}</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody>'
        '</table>'
        '</div>'
        '<div class="upcoming-table-footer">'
        f'<span><strong>{len(frame)}</strong> upcoming activities</span>'
        f'<span><strong>{high_count}</strong> high priority</span>'
        '</div>'
        '</div>'
    )

    st.markdown(
        table_html,
        unsafe_allow_html=True,
    )


def professional_chart(fig, height=275, legend=True):
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=10, t=10, b=8),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial, sans-serif",
            size=11,
            color="#61758C",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10),
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
        tickfont=dict(size=10, color="#71839A"),
        title_font=dict(size=10, color="#61758C"),
        automargin=True,
    )

    fig.update_yaxes(
        gridcolor="#E9EEF5",
        zeroline=False,
        linecolor="#E6EDF5",
        tickfont=dict(size=10, color="#71839A"),
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
    '<div class="overview-header">'
    '<div class="overview-eyebrow">PGDM Outreach Intelligence</div>'
    '<div class="overview-title-row">'
    '<div class="overview-title-wrap">'
    '<div class="overview-title">Outreach Overview</div>'
    '</div>'
    '<div class="live-badge-custom">● LIVE GOOGLE SHEET</div>'
    '</div>'
    '<div class="overview-subtitle">'
    'Campus outreach planning, execution, coverage and student-reach intelligence.'
    '</div>'
    '<div class="overview-accent"></div>'
    '</div>'
)

st.markdown(header_html, unsafe_allow_html=True)


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
    campus_filter = st.selectbox("Campus", campus_values)

with f2:
    activity_values = (
        ["All"] + sorted(df["Activity Type"].dropna().unique().tolist())
        if "Activity Type" in df.columns else ["All"]
    )
    activity_filter = st.selectbox("Activity Type", activity_values)

with f3:
    segment_values = (
        ["All"] + sorted(df["Target Segment"].dropna().unique().tolist())
        if "Target Segment" in df.columns else ["All"]
    )
    segment_filter = st.selectbox("Target Segment", segment_values)

with f4:
    owner_values = (
        ["All"] + sorted(df["Activity Owner"].dropna().unique().tolist())
        if "Activity Owner" in df.columns else ["All"]
    )
    owner_filter = st.selectbox("Owner", owner_values)

with f5:
    status_values = (
        ["All"] + sorted(df["Status"].dropna().unique().tolist())
        if "Status" in df.columns else ["All"]
    )
    status_filter = st.selectbox("Status", status_values)

with f6:
    priority_values = (
        ["All"] + sorted(df["Priority"].dropna().unique().tolist())
        if "Priority" in df.columns else ["All"]
    )
    priority_filter = st.selectbox("Priority", priority_values)

date_range = None
with f7:
    if "Activity Date" in df.columns and df["Activity Date"].notna().any():
        min_date = df["Activity Date"].min().date()
        max_date = df["Activity Date"].max().date()
        date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
    else:
        st.text_input("Date Range", value="", disabled=True)


# =========================================================
# APPLY FILTERS
# =========================================================
filtered = df.copy()

if campus_filter != "All" and "Campus" in filtered.columns:
    filtered = filtered[filtered["Campus"] == campus_filter]

if activity_filter != "All" and "Activity Type" in filtered.columns:
    filtered = filtered[filtered["Activity Type"] == activity_filter]

if segment_filter != "All" and "Target Segment" in filtered.columns:
    filtered = filtered[filtered["Target Segment"] == segment_filter]

if owner_filter != "All" and "Activity Owner" in filtered.columns:
    filtered = filtered[filtered["Activity Owner"] == owner_filter]

if status_filter != "All" and "Status" in filtered.columns:
    filtered = filtered[filtered["Status"] == status_filter]

if priority_filter != "All" and "Priority" in filtered.columns:
    filtered = filtered[filtered["Priority"] == priority_filter]

if (
    date_range
    and isinstance(date_range, (list, tuple))
    and len(date_range) == 2
    and "Activity Date" in filtered.columns
):
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)

    filtered = filtered[
        (filtered["Activity Date"] >= start_date)
        & (filtered["Activity Date"] < end_date)
    ]

if filtered.empty:
    st.warning("Selected filters ke liye koi outreach data available nahi hai.")
    st.stop()


# =========================================================
# KPI CALCULATIONS
# =========================================================
today = pd.Timestamp.today().normalize()

total_activities = len(filtered)

upcoming_mask = (
    filtered["Activity Date"].ge(today)
    if "Activity Date" in filtered.columns
    else pd.Series(False, index=filtered.index)
)

if "Status" in filtered.columns:
    upcoming_mask &= ~filtered["Status"].isin(CLOSED_STATUSES)

upcoming_count = int(upcoming_mask.sum())

institutions = (
    int(filtered["Institution / Event Name"].dropna().nunique())
    if "Institution / Event Name" in filtered.columns else 0
)

cities = (
    int(filtered["City"].dropna().nunique())
    if "City" in filtered.columns else 0
)

planned_reach = (
    filtered["Planned Student Reach"].sum(min_count=1)
    if "Planned Student Reach" in filtered.columns else 0
)

actual_reach = (
    filtered["Actual Student Reach"].sum(min_count=1)
    if "Actual Student Reach" in filtered.columns else 0
)

planned_reach = 0 if pd.isna(planned_reach) else int(planned_reach)
actual_reach = 0 if pd.isna(actual_reach) else int(actual_reach)


# =========================================================
# KPI ROW
# =========================================================
k1, k2, k3, k4, k5, k6 = st.columns(6, gap="small")

with k1:
    professional_kpi(
        "Total Activities",
        f"{total_activities:,}",
        "All outreach activities",
        "●",
        "kpi-blue",
    )

with k2:
    professional_kpi(
        "Upcoming",
        f"{upcoming_count:,}",
        "Today onwards",
        "↗",
        "kpi-cyan",
    )

with k3:
    professional_kpi(
        "Institutions",
        f"{institutions:,}",
        "Unique institutions",
        "◆",
        "kpi-violet",
    )

with k4:
    professional_kpi(
        "Cities Covered",
        f"{cities:,}",
        "Outreach footprint",
        "⌖",
        "kpi-teal",
    )

with k5:
    professional_kpi(
        "Planned Reach",
        f"{planned_reach:,}",
        "Planned student reach",
        "◎",
        "kpi-amber",
    )

with k6:
    professional_kpi(
        "Actual Reach",
        f"{actual_reach:,}",
        "Entered actual reach",
        "✓",
        "kpi-green",
    )


# =========================================================
# CHART 1 — CAMPUS STATUS + MATCHED INSIGHT
# =========================================================
row1_left, row1_right = st.columns([2.35, 1.0], gap="medium")

with row1_left:
    with st.container(border=True):
        chart_header(
            "Campus Activity Status",
            "Activity volume and current execution status by campus.",
        )

        status_data = pd.DataFrame()

        if {"Campus", "Status"}.issubset(filtered.columns):
            status_data = (
                filtered.dropna(subset=["Campus", "Status"])
                .groupby(["Campus", "Status"])
                .size()
                .reset_index(name="Activities")
            )

        if not status_data.empty:
            status_colors = {
                "Confirmed": "#2F6FBC",
                "Planned": "#8FC2E8",
                "Completed": "#2F9B6B",
                "Cancelled": "#D65A63",
                "Rescheduled": "#D99A32",
            }

            fig = px.bar(
                status_data,
                x="Campus",
                y="Activities",
                color="Status",
                barmode="stack",
                text="Activities",
                color_discrete_map=status_colors,
                category_orders={
                    "Campus": ["Lucknow", "Noida", "Jaipur", "Indore"]
                },
            )

            fig.update_traces(
                textposition="inside",
                texttemplate="%{text}",
                textfont=dict(size=9),
                insidetextorientation="horizontal",
                marker_line_width=0,
                cliponaxis=False,
            )

            status_max = int(
                status_data.groupby("Campus")["Activities"]
                .sum()
                .max()
            )

            fig.update_xaxes(title="")
            fig.update_yaxes(
                title="Activities",
                range=[
                    0,
                    max(1, status_max * 1.15),
                ],
                showticklabels=False,
                ticks="",
                showgrid=False,
                zeroline=False,
            )

            st.plotly_chart(
                professional_chart(fig, 270),
                width="stretch",
                config=CHART_CONFIG,
            )

            campus_totals = (
                status_data.groupby("Campus")["Activities"]
                .sum()
                .sort_values(ascending=False)
            )
            top_campus = campus_totals.index[0]
            top_campus_count = int(campus_totals.iloc[0])

            confirmed_count = int(
                status_data.loc[
                    status_data["Status"].eq("Confirmed"),
                    "Activities",
                ].sum()
            )
            planned_count = int(
                status_data.loc[
                    status_data["Status"].eq("Planned"),
                    "Activities",
                ].sum()
            )

            chart_insight(
                "Campus Status Insight",
                (
                    f"{top_campus} has the highest outreach load with "
                    f"{top_campus_count} activities. In the selected view, "
                    f"{confirmed_count} activities are confirmed and "
                    f"{planned_count} are still planned."
                ),
                "blue",
            )

with row1_right:
    with st.container(border=True):
        chart_header(
            "Status Snapshot",
            "Management-ready summary from the same campus-status view.",
        )

        if not status_data.empty:
            campus_totals = (
                status_data.groupby("Campus")["Activities"]
                .sum()
                .sort_values(ascending=False)
            )

            top_campus = campus_totals.index[0]
            top_value = int(campus_totals.iloc[0])

            confirmed_total = int(
                status_data.loc[
                    status_data["Status"].eq("Confirmed"),
                    "Activities",
                ].sum()
            )
            planned_total = int(
                status_data.loc[
                    status_data["Status"].eq("Planned"),
                    "Activities",
                ].sum()
            )

            mini_insight(
                "Top campus",
                top_campus,
                f"{top_value} outreach activities",
            )
            mini_insight(
                "Confirmed",
                f"{confirmed_total}",
                "Current confirmed activities",
            )
            mini_insight(
                "Still planned",
                f"{planned_total}",
                "Needs execution follow-through",
            )


# =========================================================
# CHART ROW 2 — REACH + ACTIVITY MIX, EACH WITH INSIGHT
# =========================================================
c1, c2 = st.columns(2, gap="medium")

with c1:
    with st.container(border=True):
        chart_header(
            "Planned vs Actual Student Reach",
            "Campus-wise reach comparison; blank actual values remain missing.",
        )

        if {
            "Campus",
            "Planned Student Reach",
            "Actual Student Reach",
        }.issubset(filtered.columns):

            reach = (
                filtered.groupby("Campus", as_index=False)
                .agg(
                    Planned=(
                        "Planned Student Reach",
                        lambda s: s.sum(min_count=1),
                    ),
                    Actual=(
                        "Actual Student Reach",
                        lambda s: s.sum(min_count=1),
                    ),
                )
            )

            long = (
                reach.melt(
                    "Campus",
                    var_name="Reach Type",
                    value_name="Students",
                )
                .dropna(subset=["Students"])
            )

            if not long.empty:
                fig = px.bar(
                    long,
                    x="Campus",
                    y="Students",
                    color="Reach Type",
                    barmode="group",
                    text="Students",
                    color_discrete_map={
                        "Planned": "#3169C6",
                        "Actual": "#22A58C",
                    },
                    category_orders={
                        "Campus": ["Lucknow", "Noida", "Jaipur", "Indore"]
                    },
                )

                fig.update_traces(
                    textposition="outside",
                    texttemplate="%{y:,.0f}",
                    textfont=dict(size=9),
                    marker_line_width=0,
                    cliponaxis=False,
                )

                max_reach_value = float(
                    long["Students"].max()
                )

                fig.update_xaxes(title="")
                fig.update_yaxes(
                    title="Students",
                    range=[
                        0,
                        max(
                            1,
                            max_reach_value * 1.18,
                        ),
                    ],
                    showticklabels=False,
                    ticks="",
                    showgrid=False,
                    zeroline=False,
                )

                st.plotly_chart(
                    professional_chart(fig, 260),
                    width="stretch",
                    config=CHART_CONFIG,
                )

                planned_known = reach.dropna(subset=["Planned"])
                actual_known = reach.dropna(subset=["Actual"])

                top_planned_text = "No planned reach available"
                if not planned_known.empty:
                    top_row = planned_known.loc[
                        planned_known["Planned"].idxmax()
                    ]
                    top_planned_text = (
                        f'{top_row["Campus"]} has the highest planned reach '
                        f'({int(top_row["Planned"]):,}).'
                    )

                missing_actual = int(reach["Actual"].isna().sum())

                chart_insight(
                    "Reach Insight",
                    (
                        f"{top_planned_text} Actual reach is currently missing "
                        f"for {missing_actual} campus(es) in this view, so blanks "
                        f"are not interpreted as zero performance."
                    ),
                    "teal",
                )


with c2:
    with st.container(border=True):
        chart_header(
            "Outreach Activity Mix",
            "Relative use of workshops, visits and other outreach formats.",
        )

        if "Activity Type" in filtered.columns:
            mix = (
                filtered["Activity Type"]
                .dropna()
                .value_counts()
                .rename_axis("Activity Type")
                .reset_index(name="Activities")
                .sort_values("Activities")
            )

            if not mix.empty:
                professional_blues = [
                    "#D7E7F4",
                    "#C1D9ED",
                    "#A8CAE6",
                    "#88B6DB",
                    "#679FCF",
                    "#4C88C4",
                    "#3371B4",
                    "#245E9F",
                    "#194B83",
                    "#123B69",
                ]

                if len(mix) == 1:
                    colors = ["#245E9F"]
                else:
                    colors = [
                        professional_blues[
                            round(
                                i
                                * (len(professional_blues) - 1)
                                / (len(mix) - 1)
                            )
                        ]
                        for i in range(len(mix))
                    ]

                fig = px.bar(
                    mix,
                    x="Activities",
                    y="Activity Type",
                    orientation="h",
                    text="Activities",
                )
                fig.update_traces(
                    marker_color=colors,
                    textposition="outside",
                    texttemplate="%{x:,.0f}",
                    textfont=dict(size=9),
                    marker_line_width=0,
                    cliponaxis=False,
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Activities: %{x:,.0f}"
                        "<extra></extra>"
                    ),
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
                    tickfont=dict(
                        size=9,
                        color="#5F748B",
                    ),
                    automargin=True,
                )

                activity_mix_height = min(
                    max(
                        255,
                        120 + len(mix) * 34,
                    ),
                    430,
                )

                st.plotly_chart(
                    professional_chart(
                        fig,
                        activity_mix_height,
                        legend=False,
                    ),
                    width="stretch",
                    config=CHART_CONFIG,
                )

                mix_desc = mix.sort_values(
                    "Activities",
                    ascending=False,
                )
                top_type = mix_desc.iloc[0]["Activity Type"]
                top_count = int(mix_desc.iloc[0]["Activities"])
                mix_total = int(mix_desc["Activities"].sum())
                share = (
                    round(top_count / mix_total * 100, 1)
                    if mix_total else 0
                )

                chart_insight(
                    "Activity Mix Insight",
                    (
                        f"{top_type} is the dominant outreach format with "
                        f"{top_count} activities ({share}% of the selected mix). "
                        f"The current plan uses {len(mix_desc)} distinct activity types."
                    ),
                    "violet",
                )


# =========================================================
# UPCOMING ACTIVITIES — INSIGHTS + COMPACT TABLE
# =========================================================
st.markdown(
    '<div class="table-title">Upcoming Outreach Activities</div>'
    '<div class="table-subtitle">'
    'Next scheduled field actions from the live Google Sheet.'
    '</div>',
    unsafe_allow_html=True,
)

upcoming_df = pd.DataFrame()

if "Activity Date" in filtered.columns:
    upcoming_df = filtered[
        filtered["Activity Date"].ge(today)
    ].copy()

    if "Status" in upcoming_df.columns:
        upcoming_df = upcoming_df[
            ~upcoming_df["Status"].isin(CLOSED_STATUSES)
        ]

    upcoming_df = upcoming_df.sort_values("Activity Date")


# ---------- Table-level insights ----------
t1, t2, t3, t4 = st.columns(4, gap="small")

if not upcoming_df.empty:
    next_date = upcoming_df["Activity Date"].min()

    next7_count = int(
        upcoming_df[
            upcoming_df["Activity Date"].le(
                today + pd.Timedelta(days=7)
            )
        ].shape[0]
    )

    high_priority_count = (
        int(upcoming_df["Priority"].eq("High").sum())
        if "Priority" in upcoming_df.columns
        else 0
    )

    top_owner = "N/A"
    if (
        "Activity Owner" in upcoming_df.columns
        and upcoming_df["Activity Owner"].notna().any()
    ):
        top_owner = (
            upcoming_df["Activity Owner"]
            .value_counts()
            .idxmax()
        )

    with t1:
        mini_insight(
            "Next activity",
            next_date.strftime("%d %b"),
            next_date.strftime("%Y"),
        )

    with t2:
        mini_insight(
            "Next 7 days",
            f"{next7_count}",
            "Scheduled outreach activities",
        )

    with t3:
        mini_insight(
            "High priority",
            f"{high_priority_count}",
            "Upcoming high-priority actions",
        )

    with t4:
        mini_insight(
            "Most loaded owner",
            top_owner,
            "Based on upcoming activity count",
        )


if upcoming_df.empty:
    st.info(
        "Selected filters ke liye koi upcoming outreach activity nahi hai."
    )
else:
    display_columns = [
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

    display_columns = [
        col for col in display_columns
        if col in upcoming_df.columns
    ]

    render_upcoming_table(
        upcoming_df,
        display_columns,
    )

    chart_insight(
        "Upcoming Activity Insight",
        (
            f"{len(upcoming_df)} upcoming activities are visible for the selected "
            f"filters. {high_priority_count} are High priority and {next7_count} "
            f"fall within the next 7 days. Use this table as the immediate "
            f"execution checklist for campus outreach teams."
        ),
        "amber",
    )
