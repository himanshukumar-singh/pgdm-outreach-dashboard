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
page_config("Team & Resources")
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
    animation: teamBrandMotion 3.8s ease-in-out infinite alternate;
}

[data-testid="stSidebar"] .brand-sub {
    animation-delay: .18s;
    color: #A9C9EF !important;
    font-size: .72rem !important;
    line-height: 1.35 !important;
}

@keyframes teamBrandMotion {
    from { transform: translateX(-6px); }
    to   { transform: translateX(24px); }
}

[data-testid="stSidebar"] .stPageLink a {
    padding: .56rem .62rem !important;
    margin-bottom: .14rem !important;
    font-size: .90rem !important;
}

/* ---------- Moving title ---------- */
.team-header {
    transform: translateY(-13px);
    margin-bottom: -8px;
}

.team-eyebrow {
    color: #2B6DE8;
    font-size: .67rem;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
    margin-bottom: .05rem;
}

.team-title-row {
    position: relative;
    width: 100%;
    padding-right: 10.8rem;
}

.team-title-wrap {
    position: relative;
    width: 100%;
    height: 1.72rem;
    overflow: hidden;
    white-space: nowrap;
}

.team-title {
    position: absolute;
    top: 0;
    width: max-content;
    color: #0F2A45;
    font-size: 1.28rem;
    font-weight: 850;
    letter-spacing: -.02em;
    line-height: 1.02;
    white-space: nowrap;
    animation: teamTitleShuttle 6.3s linear infinite alternate;
}

@keyframes teamTitleShuttle {
    0% {
        left: 0%;
        transform: translateX(-105%);
    }
    100% {
        left: 100%;
        transform: translateX(4%);
    }
}

.team-live {
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

.team-subtitle {
    color: #71839A;
    font-size: .86rem;
    margin-top: .02rem;
}

.team-accent {
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
.team-kpi {
    position: relative;
    overflow: hidden;
    min-height: 94px;
    border-radius: 14px;
    padding: .64rem .72rem .60rem .72rem;
    background: linear-gradient(145deg, #FFF 0%, var(--wash) 100%);
    border: 1px solid var(--border);
    box-shadow: 0 6px 18px rgba(15,42,69,.045);
    animation: teamFloat 2.15s ease-in-out infinite;
}

.team-kpi::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 0;
    width: 4px;
    background: linear-gradient(180deg, var(--accent), var(--accent2));
}

.team-kpi::after {
    content: "";
    position: absolute;
    width: 82px;
    height: 82px;
    border-radius: 50%;
    right: -32px;
    top: -34px;
    background: radial-gradient(circle, var(--bubble) 0%, rgba(255,255,255,0) 72%);
}

.team-kpi .icon {
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

.team-kpi .label {
    position: relative;
    z-index: 2;
    color: #60758C;
    font-size: .66rem;
    font-weight: 850;
    white-space: nowrap;
}

.team-kpi .value {
    position: relative;
    z-index: 2;
    color: #0F2A45;
    font-size: 1.72rem;
    font-weight: 900;
    line-height: 1;
    margin-top: .18rem;
}

.team-kpi .sub {
    position: relative;
    z-index: 2;
    color: #8293A8;
    font-size: .60rem;
    margin-top: .17rem;
}

.team-kpi .mini-line {
    position: absolute;
    left: .72rem;
    right: .72rem;
    bottom: .36rem;
    height: 2px;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: .18;
}

@keyframes teamFloat {
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
.team-insight {
    padding: .70rem .76rem;
    border-radius: 10px;
    border: 1px solid #DFE7F0;
    background: #FFFFFF;
    box-shadow: 0 4px 12px rgba(15,42,69,.025);
    margin-bottom: .48rem;
}

.team-insight .label {
    font-size: .64rem;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: .04em;
    color: #74879D;
}

.team-insight .value {
    font-size: .96rem;
    font-weight: 900;
    color: #0F2A45;
    margin-top: .12rem;
}

.team-insight .note {
    color: #7E90A6;
    font-size: .68rem;
    line-height: 1.42;
    margin-top: .18rem;
}

.team-action {
    margin-top: .25rem;
    padding: .68rem .74rem;
    border-radius: 10px;
    background: linear-gradient(90deg, #EFF6FF 0%, #FBFDFF 100%);
    border: 1px solid #D9E7FA;
    border-left: 4px solid #2B6DE8;
}

.team-action.teal {
    background: linear-gradient(90deg, #EFFBF8 0%, #FBFEFD 100%);
    border-color: #D6EFEA;
    border-left-color: #159E8C;
}

.team-action.violet {
    background: linear-gradient(90deg, #F6F2FF 0%, #FCFAFF 100%);
    border-color: #E6DCFF;
    border-left-color: #7C3AED;
}

.team-action.amber {
    background: linear-gradient(90deg, #FFF8EC 0%, #FFFDFB 100%);
    border-color: #F2E0BE;
    border-left-color: #D98B16;
}

.team-action .title {
    color: #173A61;
    font-size: .69rem;
    font-weight: 850;
}

.team-action .body {
    color: #6C7E91;
    font-size: .70rem;
    line-height: 1.42;
    margin-top: .18rem;
}

/* ---------- Tables ---------- */
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
    .team-title,
    .team-kpi,
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
def team_kpi(label, value, subtitle, icon, css_class):
    st.markdown(
        (
            f'<div class="team-kpi {css_class}">'
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


def team_insight(label, value, note):
    st.markdown(
        (
            '<div class="team-insight">'
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
            f'<div class="team-action {tone_class}">'
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


def split_people(value):
    if pd.isna(value):
        return []

    text = str(value).strip()
    if not text:
        return []

    for sep in [";", "|", "\n"]:
        text = text.replace(sep, ",")

    return [
        item.strip()
        for item in text.split(",")
        if item.strip()
    ]


def make_people_usage(frame, column_name, role_name):
    if column_name not in frame.columns:
        return pd.DataFrame(
            columns=[
                "Person",
                "Activities",
                "Role",
            ]
        )

    rows = []

    for _, row in frame[[column_name]].iterrows():
        for person in split_people(row[column_name]):
            rows.append(
                {
                    "Person": person,
                    "Role": role_name,
                }
            )

    if not rows:
        return pd.DataFrame(
            columns=[
                "Person",
                "Activities",
                "Role",
            ]
        )

    out = pd.DataFrame(rows)

    return (
        out.groupby(
            [
                "Person",
                "Role",
            ],
            as_index=False,
        )
        .size()
        .rename(
            columns={
                "size": "Activities",
            }
        )
    )


# =========================================================
# LOAD DATA
# =========================================================
df = load_data()


# =========================================================
# HEADER
# =========================================================
header_html = (
    '<div class="team-header">'
    '<div class="team-eyebrow">PGDM Outreach Intelligence</div>'
    '<div class="team-title-row">'
    '<div class="team-title-wrap">'
    '<div class="team-title">Team &amp; Resources</div>'
    '</div>'
    '<div class="team-live">● LIVE GOOGLE SHEET</div>'
    '</div>'
    '<div class="team-subtitle">'
    'Owner workload, supporting-team deployment and resource-person utilisation.'
    '</div>'
    '<div class="team-accent"></div>'
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
        key="team_page_campus",
    )

with f2:
    activity_values = (
        ["All"] + sorted(df["Activity Type"].dropna().unique().tolist())
        if "Activity Type" in df.columns else ["All"]
    )
    activity_filter = st.selectbox(
        "Activity Type",
        activity_values,
        key="team_page_activity",
    )

with f3:
    segment_values = (
        ["All"] + sorted(df["Target Segment"].dropna().unique().tolist())
        if "Target Segment" in df.columns else ["All"]
    )
    segment_filter = st.selectbox(
        "Target Segment",
        segment_values,
        key="team_page_segment",
    )

with f4:
    owner_values = (
        ["All"] + sorted(df["Activity Owner"].dropna().unique().tolist())
        if "Activity Owner" in df.columns else ["All"]
    )
    owner_filter = st.selectbox(
        "Owner",
        owner_values,
        key="team_page_owner",
    )

with f5:
    status_values = (
        ["All"] + sorted(df["Status"].dropna().unique().tolist())
        if "Status" in df.columns else ["All"]
    )
    status_filter = st.selectbox(
        "Status",
        status_values,
        key="team_page_status",
    )

with f6:
    priority_values = (
        ["All"] + sorted(df["Priority"].dropna().unique().tolist())
        if "Priority" in df.columns else ["All"]
    )
    priority_filter = st.selectbox(
        "Priority",
        priority_values,
        key="team_page_priority",
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
            key="team_page_date",
        )
    else:
        st.text_input(
            "Date Range",
            value="",
            disabled=True,
            key="team_page_date_text",
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
        "Selected filters ke liye koi team/resource data available nahi hai."
    )
    st.stop()


# =========================================================
# OWNER AGGREGATION
# =========================================================
if "Activity Owner" not in f.columns:
    st.info("Activity Owner column available nahi hai.")
    st.stop()

owner_base = f[
    f["Activity Owner"].notna()
    & f["Activity Owner"].astype(str).str.strip().ne("")
].copy()

owner_group_cols = [
    col
    for col in [
        "Campus",
        "Activity Owner",
    ]
    if col in owner_base.columns
]

owner_agg = {
    "Activities": (
        "Activity Owner",
        "size",
    ),
}

if "Institution / Event Name" in owner_base.columns:
    owner_agg["Institutions"] = (
        "Institution / Event Name",
        "nunique",
    )

if "City" in owner_base.columns:
    owner_agg["Cities"] = (
        "City",
        "nunique",
    )

if "Planned Student Reach" in owner_base.columns:
    owner_agg["Planned_Reach"] = (
        "Planned Student Reach",
        lambda s: s.sum(min_count=1),
    )

if "Actual Student Reach" in owner_base.columns:
    owner_agg["Actual_Reach"] = (
        "Actual Student Reach",
        lambda s: s.sum(min_count=1),
    )

owner = (
    owner_base.groupby(
        owner_group_cols,
        dropna=False,
    )
    .agg(**owner_agg)
    .reset_index()
)

for col in [
    "Activities",
    "Institutions",
    "Cities",
]:
    if col in owner.columns:
        owner[col] = (
            pd.to_numeric(
                owner[col],
                errors="coerce",
            )
            .fillna(0)
            .astype(int)
        )


# =========================================================
# UPCOMING / OPEN / HIGH PRIORITY BY OWNER
# =========================================================
today = pd.Timestamp.today().normalize()

if "Status" in owner_base.columns:
    open_mask = ~owner_base["Status"].isin(CLOSED_STATUSES)
else:
    open_mask = pd.Series(
        True,
        index=owner_base.index,
    )

if "Activity Date" in owner_base.columns:
    upcoming_mask = (
        owner_base["Activity Date"].ge(today)
        & open_mask
    )
else:
    upcoming_mask = pd.Series(
        False,
        index=owner_base.index,
    )

upcoming_owner = (
    owner_base.loc[upcoming_mask]
    .groupby(owner_group_cols)
    .size()
    .rename("Upcoming")
    .reset_index()
)

open_owner = (
    owner_base.loc[open_mask]
    .groupby(owner_group_cols)
    .size()
    .rename("Open_Activities")
    .reset_index()
)

if "Priority" in owner_base.columns:
    high_owner = (
        owner_base.loc[
            owner_base["Priority"].eq("High")
        ]
        .groupby(owner_group_cols)
        .size()
        .rename("High_Priority")
        .reset_index()
    )
else:
    high_owner = pd.DataFrame(
        columns=owner_group_cols + ["High_Priority"]
    )

owner = owner.merge(
    upcoming_owner,
    on=owner_group_cols,
    how="left",
)

owner = owner.merge(
    open_owner,
    on=owner_group_cols,
    how="left",
)

owner = owner.merge(
    high_owner,
    on=owner_group_cols,
    how="left",
)

for col in [
    "Upcoming",
    "Open_Activities",
    "High_Priority",
]:
    owner[col] = (
        owner[col]
        .fillna(0)
        .astype(int)
    )


# =========================================================
# RESOURCE UTILISATION
# =========================================================
support_candidates = [
    "Supporting Team Member",
    "Supporting Team Members",
    "Supporting Team",
]

resource_candidates = [
    "Resource Person",
    "Resource Persons",
]

support_col = next(
    (
        col
        for col in support_candidates
        if col in f.columns
    ),
    None,
)

resource_col = next(
    (
        col
        for col in resource_candidates
        if col in f.columns
    ),
    None,
)

support_usage = (
    make_people_usage(
        f,
        support_col,
        "Supporting Team",
    )
    if support_col
    else pd.DataFrame(
        columns=[
            "Person",
            "Activities",
            "Role",
        ]
    )
)

resource_usage = (
    make_people_usage(
        f,
        resource_col,
        "Resource Person",
    )
    if resource_col
    else pd.DataFrame(
        columns=[
            "Person",
            "Activities",
            "Role",
        ]
    )
)

resource_utilisation = pd.concat(
    [
        support_usage,
        resource_usage,
    ],
    ignore_index=True,
)

if not resource_utilisation.empty:
    resource_utilisation = (
        resource_utilisation.groupby(
            [
                "Person",
                "Role",
            ],
            as_index=False,
        )["Activities"]
        .sum()
        .sort_values(
            [
                "Activities",
                "Person",
            ],
            ascending=[
                False,
                True,
            ],
        )
    )


# =========================================================
# KPI CALCULATIONS
# =========================================================
unique_owners = int(
    owner_base["Activity Owner"]
    .dropna()
    .nunique()
)

total_activities = int(
    len(owner_base)
)

upcoming_total = int(
    upcoming_mask.sum()
)

high_priority_total = (
    int(
        owner_base["Priority"]
        .eq("High")
        .sum()
    )
    if "Priority" in owner_base.columns
    else 0
)

support_people_count = (
    int(
        support_usage["Person"]
        .nunique()
    )
    if not support_usage.empty
    else 0
)

resource_people_count = (
    int(
        resource_usage["Person"]
        .nunique()
    )
    if not resource_usage.empty
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
    team_kpi(
        "Owners",
        f"{unique_owners:,}",
        "Unique activity owners",
        "●",
        "kpi-blue",
    )

with k2:
    team_kpi(
        "Activities",
        f"{total_activities:,}",
        "Owner-linked activities",
        "◆",
        "kpi-cyan",
    )

with k3:
    team_kpi(
        "Upcoming",
        f"{upcoming_total:,}",
        "Future open activities",
        "↗",
        "kpi-violet",
    )

with k4:
    team_kpi(
        "High Priority",
        f"{high_priority_total:,}",
        "High-priority workload",
        "!",
        "kpi-amber",
    )

with k5:
    team_kpi(
        "Supporting Team",
        f"{support_people_count:,}",
        "Unique support people",
        "＋",
        "kpi-teal",
    )

with k6:
    team_kpi(
        "Resource Persons",
        f"{resource_people_count:,}",
        "Unique resource people",
        "✓",
        "kpi-green",
    )


# =========================================================
# OWNER WORKLOAD SCORECARD
# =========================================================
st.markdown(
    '<div class="table-heading">Owner Workload Scorecard</div>'
    '<div class="table-subheading">'
    'Compact owner-level workload, institution coverage and execution-pressure view.'
    '</div>',
    unsafe_allow_html=True,
)

owner_scorecard = owner.rename(
    columns={
        "Planned_Reach": "Planned Reach",
        "Actual_Reach": "Actual Reach",
        "Open_Activities": "Open",
        "High_Priority": "High Priority",
    }
).copy()

owner_display_cols = [
    "Campus",
    "Activity Owner",
    "Activities",
    "Institutions",
    "Cities",
    "Upcoming",
    "Open",
    "High Priority",
    "Planned Reach",
    "Actual Reach",
]

owner_display_cols = [
    col
    for col in owner_display_cols
    if col in owner_scorecard.columns
]

st.dataframe(
    owner_scorecard[
        owner_display_cols
    ].sort_values(
        [
            "Activities",
            "Activity Owner",
        ],
        ascending=[
            False,
            True,
        ],
    ),
    width="stretch",
    hide_index=True,
    height=270,
    row_height=30,
    column_config={
        "Campus": st.column_config.TextColumn(
            "Campus",
            width="small",
        ),
        "Activity Owner": st.column_config.TextColumn(
            "Activity Owner",
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
        "Open": st.column_config.NumberColumn(
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
    },
)


# =========================================================
# ROW 1 — OWNER WORKLOAD + MANAGEMENT INTELLIGENCE
# =========================================================
left, right = st.columns(
    [2.25, 1.0],
    gap="medium",
)

with left:
    with st.container(border=True):
        card_header(
            "Owner Workload",
            "Outreach activity volume handled by each owner.",
        )

        owner_chart = (
            owner.groupby(
                "Activity Owner",
                as_index=False,
            )["Activities"]
            .sum()
            .sort_values("Activities")
        )

        fig = px.bar(
            owner_chart,
            x="Activities",
            y="Activity Owner",
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
                250,
                legend=False,
            ),
            width="stretch",
            config=CHART_CONFIG,
        )

        top_owner_row = (
            owner_chart.sort_values(
                "Activities",
                ascending=False,
            )
            .iloc[0]
        )

        owner_share = (
            round(
                int(top_owner_row["Activities"])
                / total_activities
                * 100,
                1,
            )
            if total_activities > 0
            else 0
        )

        action_note(
            "Owner Workload Insight",
            (
                f'{top_owner_row["Activity Owner"]} has the highest owner workload '
                f'with {int(top_owner_row["Activities"])} activities '
                f'({owner_share}% of owner-linked activity volume).'
            ),
            "blue",
        )


with right:
    with st.container(border=True):
        card_header(
            "Team Intelligence",
            "Management-ready workload and deployment summary.",
        )

        team_insight(
            "Highest workload owner",
            str(top_owner_row["Activity Owner"]),
            f'{int(top_owner_row["Activities"])} activities',
        )

        upcoming_by_owner = (
            owner.groupby(
                "Activity Owner",
                as_index=False,
            )["Upcoming"]
            .sum()
            .sort_values(
                "Upcoming",
                ascending=False,
            )
        )

        top_upcoming = upcoming_by_owner.iloc[0]

        team_insight(
            "Highest upcoming load",
            str(top_upcoming["Activity Owner"]),
            f'{int(top_upcoming["Upcoming"])} future open activities',
        )

        high_by_owner = (
            owner.groupby(
                "Activity Owner",
                as_index=False,
            )["High_Priority"]
            .sum()
            .sort_values(
                "High_Priority",
                ascending=False,
            )
        )

        top_high = high_by_owner.iloc[0]

        team_insight(
            "Highest High-priority load",
            str(top_high["Activity Owner"]),
            f'{int(top_high["High_Priority"])} High-priority activities',
        )

        if resource_utilisation.empty:
            team_insight(
                "Most utilised resource",
                "N/A",
                "Supporting Team / Resource Person data is not available.",
            )
        else:
            top_resource = (
                resource_utilisation
                .sort_values(
                    "Activities",
                    ascending=False,
                )
                .iloc[0]
            )

            team_insight(
                "Most utilised resource",
                str(top_resource["Person"]),
                (
                    f'{int(top_resource["Activities"])} activities • '
                    f'{top_resource["Role"]}'
                ),
            )


# =========================================================
# ROW 2 — INSTITUTION COVERAGE + EXECUTION PRESSURE
# =========================================================
c1, c2 = st.columns(
    2,
    gap="medium",
)

with c1:
    with st.container(border=True):
        card_header(
            "Institution Coverage by Owner",
            "Unique institutions assigned across outreach owners.",
        )

        if "Institutions" not in owner.columns:
            st.info(
                "Institution coverage data available nahi hai."
            )
        else:
            owner_inst = (
                owner.groupby(
                    "Activity Owner",
                    as_index=False,
                )["Institutions"]
                .sum()
                .sort_values("Institutions")
            )

            fig = px.bar(
                owner_inst,
                x="Institutions",
                y="Activity Owner",
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
                    230,
                    legend=False,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )

            top_inst_owner = (
                owner_inst.sort_values(
                    "Institutions",
                    ascending=False,
                )
                .iloc[0]
            )

            action_note(
                "Institution Coverage Insight",
                (
                    f'{top_inst_owner["Activity Owner"]} currently covers the '
                    f'highest number of institutions '
                    f'({int(top_inst_owner["Institutions"])}). '
                    f'Compare this with workload before assigning additional accounts.'
                ),
                "violet",
            )


with c2:
    with st.container(border=True):
        card_header(
            "Upcoming vs High-Priority Load",
            "Execution pressure by owner.",
        )

        pressure = (
            owner.groupby(
                "Activity Owner",
                as_index=False,
            )[[
                "Upcoming",
                "High_Priority",
            ]]
            .sum()
        )

        pressure_long = (
            pressure.melt(
                id_vars="Activity Owner",
                var_name="Load Type",
                value_name="Activities",
            )
        )

        pressure_long["Load Type"] = (
            pressure_long["Load Type"]
            .replace(
                {
                    "Upcoming": "Upcoming",
                    "High_Priority": "High Priority",
                }
            )
        )

        fig = px.bar(
            pressure_long,
            x="Activity Owner",
            y="Activities",
            color="Load Type",
            barmode="group",
            text="Activities",
            color_discrete_map={
                "Upcoming": "#5B8FD6",
                "High Priority": "#D9534F",
            },
        )

        fig.update_traces(
            textposition="outside",
            textfont=dict(size=9),
            marker_line_width=0,
        )

        fig.update_xaxes(
            title="",
            tickangle=-20,
        )

        fig.update_yaxes(
            title="Activities",
            dtick=1,
            rangemode="tozero",
        )

        st.plotly_chart(
            clean_chart(
                fig,
                230,
                legend=True,
            ),
            width="stretch",
            config=CHART_CONFIG,
        )

        action_note(
            "Execution Pressure Insight",
            (
                f'{top_upcoming["Activity Owner"]} has the highest upcoming load '
                f'({int(top_upcoming["Upcoming"])}), while '
                f'{top_high["Activity Owner"]} has the highest High-priority load '
                f'({int(top_high["High_Priority"])}).'
            ),
            "amber",
        )


# =========================================================
# ROW 3 — CAMPUS OWNER DISTRIBUTION + RESOURCE UTILISATION
# =========================================================
r1, r2 = st.columns(
    2,
    gap="medium",
)

with r1:
    with st.container(border=True):
        card_header(
            "Owner Distribution by Campus",
            "How owner activity volume is distributed across campuses.",
        )

        if "Campus" not in owner_base.columns:
            st.info(
                "Campus data available nahi hai."
            )
        else:
            campus_owner = (
                owner_base.groupby(
                    [
                        "Campus",
                        "Activity Owner",
                    ]
                )
                .size()
                .reset_index(name="Activities")
            )

            fig = px.bar(
                campus_owner,
                x="Campus",
                y="Activities",
                color="Activity Owner",
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
                dtick=1,
                rangemode="tozero",
            )

            st.plotly_chart(
                clean_chart(
                    fig,
                    235,
                    legend=True,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )

            owner_per_campus = (
                owner_base.groupby("Campus")[
                    "Activity Owner"
                ]
                .nunique()
                .sort_values(
                    ascending=False
                )
            )

            top_campus = owner_per_campus.index[0]
            top_owner_count = int(
                owner_per_campus.iloc[0]
            )

            action_note(
                "Campus Team Insight",
                (
                    f'{top_campus} has the broadest owner deployment with '
                    f'{top_owner_count} distinct activity owners in the selected view.'
                ),
                "teal",
            )


with r2:
    with st.container(border=True):
        card_header(
            "Resource Utilisation",
            "Supporting Team and Resource Person activity usage.",
        )

        if resource_utilisation.empty:
            st.info(
                "Supporting Team Member / Resource Person data available nahi hai."
            )
        else:
            resource_chart = (
                resource_utilisation
                .sort_values(
                    "Activities",
                    ascending=True,
                )
                .tail(12)
            )

            fig = px.bar(
                resource_chart,
                x="Activities",
                y="Person",
                orientation="h",
                color="Role",
                text="Activities",
                color_discrete_map={
                    "Supporting Team": "#159E8C",
                    "Resource Person": "#D98B16",
                },
            )

            fig.update_traces(
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
                    legend=True,
                ),
                width="stretch",
                config=CHART_CONFIG,
            )

            top_resource = (
                resource_utilisation
                .sort_values(
                    "Activities",
                    ascending=False,
                )
                .iloc[0]
            )

            action_note(
                "Resource Utilisation Insight",
                (
                    f'{top_resource["Person"]} is the most frequently deployed '
                    f'resource with {int(top_resource["Activities"])} activities '
                    f'({top_resource["Role"]}).'
                ),
                "teal",
            )


# =========================================================
# RESOURCE UTILISATION TABLE
# =========================================================
st.markdown(
    '<div class="table-heading">Resource Utilisation Scorecard</div>'
    '<div class="table-subheading">'
    'Supporting-team and resource-person usage based on captured activity assignments.'
    '</div>',
    unsafe_allow_html=True,
)

if resource_utilisation.empty:
    st.info(
        "Supporting Team Member / Resource Person assignments are not available in the selected data."
    )
else:
    st.dataframe(
        resource_utilisation[
            [
                "Person",
                "Activities",
                "Role",
            ]
        ],
        width="stretch",
        hide_index=True,
        height=245,
        row_height=30,
        column_config={
            "Person": st.column_config.TextColumn(
                "Person",
                width="large",
            ),
            "Activities": st.column_config.NumberColumn(
                "Activities",
                format="%d",
                width="small",
            ),
            "Role": st.column_config.TextColumn(
                "Role",
                width="medium",
            ),
        },
    )


# =========================================================
# TEAM MANAGEMENT INSIGHT CARDS
# =========================================================
st.markdown(
    '<div class="table-heading">Team Management Insight</div>'
    '<div class="table-subheading">'
    'Top owners summarised using activity load, institution coverage and near-term execution pressure.'
    '</div>',
    unsafe_allow_html=True,
)

owner_management = (
    owner.groupby(
        "Activity Owner",
        as_index=False,
    )
    .agg(
        Activities=("Activities", "sum"),
        Upcoming=("Upcoming", "sum"),
        High_Priority=("High_Priority", "sum"),
        Institutions=(
            "Institutions",
            "sum",
        )
        if "Institutions" in owner.columns
        else (
            "Activities",
            lambda s: 0,
        ),
    )
    .sort_values(
        [
            "Activities",
            "Activity Owner",
        ],
        ascending=[
            False,
            True,
        ],
    )
    .head(4)
    .reset_index(drop=True)
)

if not owner_management.empty:
    insight_cols = st.columns(
        min(
            4,
            len(owner_management),
        ),
        gap="small",
    )

    for idx, row in owner_management.iterrows():
        with insight_cols[idx]:
            team_insight(
                str(row["Activity Owner"]),
                f'{int(row["Activities"])} activities',
                (
                    f'{int(row["Institutions"])} institutions • '
                    f'{int(row["Upcoming"])} upcoming • '
                    f'{int(row["High_Priority"])} High priority'
                ),
            )


# =========================================================
# FINAL MANAGEMENT RECOMMENDATION
# =========================================================
if len(owner_management) > 1:
    max_load = int(
        owner_management["Activities"].max()
    )
    min_load = int(
        owner_management["Activities"].min()
    )
    load_gap = max_load - min_load
else:
    load_gap = 0

if load_gap > 0:
    load_message = (
        f"The activity-load gap among the top visible owners is "
        f"{load_gap} activities."
    )
else:
    load_message = (
        "Visible owner activity loads are currently balanced."
    )

action_note(
    "Team & Resource Recommendation",
    (
        load_message
        + " Before reallocating work, compare total activity volume with "
          "institution coverage, upcoming activity pressure, High-priority load "
          "and supporting/resource-person deployment. Missing resource assignments "
          "should be completed so utilisation analysis remains reliable."
    ),
    "blue",
)
