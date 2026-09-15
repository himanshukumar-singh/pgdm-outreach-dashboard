import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    transform: translateY(-27px);
    margin-bottom: -20px;
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
    padding-right: 0;
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
    top: -0.95rem;
    padding: .20rem .40rem;
    border-radius: 999px;
    background: #EAF8F0;
    color: #17784A;
    border: 1px solid #C6EBD6;
    font-size: .55rem;
    font-weight: 800;

    display: inline-flex;
    align-items: center;
    gap: 5px;
    white-space: nowrap;

    /* LIVE GOOGLE SHEET text color changes in sync with the dot */
    animation: liveTextColors 5s linear infinite;
}

/* ---------- Animated live status dot ---------- */
.live-dot {
    width: 7px;
    height: 7px;
    min-width: 7px;
    min-height: 7px;
    display: inline-block;
    border-radius: 50%;
    flex-shrink: 0;

    background: #22C55E;
    box-shadow: 0 0 8px rgba(34, 197, 94, .70);

    animation:
        liveDotColors 5s linear infinite,
        liveDotPulse 1.25s ease-in-out infinite;
}

@keyframes liveDotColors {
    0% {
        background: #22C55E;
        box-shadow: 0 0 8px rgba(34, 197, 94, .75);
    }
    10% {
        background: #3B82F6;
        box-shadow: 0 0 8px rgba(59, 130, 246, .75);
    }
    20% {
        background: #8B5CF6;
        box-shadow: 0 0 8px rgba(139, 92, 246, .75);
    }
    30% {
        background: #EC4899;
        box-shadow: 0 0 8px rgba(236, 72, 153, .75);
    }
    40% {
        background: #EF4444;
        box-shadow: 0 0 8px rgba(239, 68, 68, .75);
    }
    50% {
        background: #F97316;
        box-shadow: 0 0 8px rgba(249, 115, 22, .75);
    }
    60% {
        background: #EAB308;
        box-shadow: 0 0 8px rgba(234, 179, 8, .75);
    }
    70% {
        background: #14B8A6;
        box-shadow: 0 0 8px rgba(20, 184, 166, .75);
    }
    80% {
        background: #06B6D4;
        box-shadow: 0 0 8px rgba(6, 182, 212, .75);
    }
    90% {
        background: #6366F1;
        box-shadow: 0 0 8px rgba(99, 102, 241, .75);
    }
    100% {
        background: #22C55E;
        box-shadow: 0 0 8px rgba(34, 197, 94, .75);
    }
}

@keyframes liveTextColors {
    0%   { color: #15803D; }
    10%  { color: #2563EB; }
    20%  { color: #7C3AED; }
    30%  { color: #DB2777; }
    40%  { color: #DC2626; }
    50%  { color: #EA580C; }
    60%  { color: #A16207; }
    70%  { color: #0F766E; }
    80%  { color: #0891B2; }
    90%  { color: #4F46E5; }
    100% { color: #15803D; }
}

@keyframes liveDotPulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.22);
    }
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
    font-size: .69rem !important;
    font-weight: 760 !important;
    margin-bottom: .12rem !important;
}

div[data-baseweb="select"] > div,
div[data-testid="stDateInput"] input {
    min-height: 2.34rem !important;
    height: 2.34rem !important;
    background: #FFFFFF !important;
    border: 1px solid #DFE7F0 !important;
    border-radius: 9px !important;
    box-shadow: 0 2px 8px rgba(15,42,69,.025);
    font-size: .71rem !important;
}

/* Compact one-line Overview filters */
div[data-testid="stSelectbox"] {
    margin-bottom: 0 !important;
}

div[data-testid="stDateInput"] {
    margin-bottom: 0 !important;
}

div[data-testid="stButton"] button {
    min-height: 2.34rem !important;
    height: 2.34rem !important;
}

.overview-filter-reset-spacer {
    height: 1.46rem;
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
    font-size: .52rem;
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
    position: relative;
    overflow: hidden;
    margin-top: .10rem;
    padding: .48rem .58rem;
    border-radius: 10px;
    background: linear-gradient(90deg, #F2F7FF 0%, #F8FBFF 100%);
    border: 1px solid #DDE8F7;
    border-left: 4px solid #2B6DE8;
    box-shadow: 0 4px 14px rgba(15,42,69,.025);
    animation: insightFloat 3.8s ease-in-out infinite;
    transition:
        transform .22s ease,
        box-shadow .22s ease;
}

/* Soft professional light sweep; does not change card size/alignment */
.chart-insight::after {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: -38%;
    width: 28%;
    pointer-events: none;
    background: linear-gradient(
        105deg,
        rgba(255,255,255,0) 0%,
        rgba(255,255,255,.18) 35%,
        rgba(255,255,255,.72) 50%,
        rgba(255,255,255,.18) 65%,
        rgba(255,255,255,0) 100%
    );
    transform: skewX(-18deg);
    animation: insightSheen 5.6s ease-in-out infinite;
}

.chart-insight:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(15,42,69,.065);
}

/* Slightly stagger each tone so all cards do not move together */
.chart-insight.teal {
    animation-delay: .28s;
}

.chart-insight.violet {
    animation-delay: .56s;
}

.chart-insight.amber {
    animation-delay: .84s;
}

/* Insight title gets a subtle moving brand-color treatment */
.chart-insight .ititle {
    position: relative;
    z-index: 2;
    background: linear-gradient(
        90deg,
        #153A5F,
        #2563EB,
        #0F9F8F,
        #7C3AED,
        #D98B16,
        #153A5F
    );
    background-size: 240% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: #153A5F;
    animation: insightTitleFlow 6s linear infinite;
}

.chart-insight .ibody {
    position: relative;
    z-index: 2;
}

@keyframes insightFloat {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-2px);
    }
}

@keyframes insightSheen {
    0%, 18% {
        left: -38%;
        opacity: 0;
    }
    28% {
        opacity: .88;
    }
    48% {
        left: 112%;
        opacity: 0;
    }
    100% {
        left: 112%;
        opacity: 0;
    }
}

@keyframes insightTitleFlow {
    0% {
        background-position: 0% 50%;
    }
    100% {
        background-position: 240% 50%;
    }
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
    font-size: .64rem;
    line-height: 1.34;
}

/* Exact status-row layout:
   keep insight flush near the bottom border without dead space below it */
.status-card-marker {
    display: none;
}

.status-insight-pin {
    margin: 0 !important;
}

/* Only Status Snapshot Insight:
   slightly smaller so a clean gap appears above it */
.status-insight-pin.teal {
    min-height: 54px !important;
    padding: .34rem .50rem !important;
    margin-top: 10px !important;
}

.status-insight-pin.teal .ititle {
    font-size: .66rem !important;
    margin-bottom: .12rem !important;
}

.status-insight-pin.teal .ibody {
    font-size: .59rem !important;
    line-height: 1.24 !important;
}

/* Status row: no internal scrollbar, border retained */
div[data-testid="stHorizontalBlock"]:has(.status-card-marker) {
    align-items: stretch !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.status-card-marker) {
    min-height: 460px !important;
    height: auto !important;
    overflow: visible !important;
    padding-bottom: .50rem !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.status-card-marker)
> div[data-testid="stVerticalBlock"] {
    min-height: 444px !important;
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: visible !important;
    padding-bottom: 0 !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.status-card-marker)
div[data-testid="stElementContainer"]:has(.status-insight-pin) {
    margin-top: auto !important;
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.status-card-marker)
.status-insight-pin {
    margin-bottom: 0 !important;
}

.chart-insight {
    min-height: 64px;
}

.chart-insight.status-equal {
    height: 86px;
    min-height: 86px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

/* ---------- Upcoming activity mini cards ---------- */
.mini-upcoming {
    position: relative;
    overflow: hidden;
    min-height: 94px;
    box-sizing: border-box;
    border-radius: 14px;
    padding: .64rem .72rem .60rem .72rem;
    background: linear-gradient(145deg, #FFFFFF 0%, var(--wash) 100%);
    border: 1px solid var(--border);
    box-shadow: 0 6px 18px rgba(15,42,69,.045);
    animation: upcomingFloat 2.4s ease-in-out infinite;
    transition: transform .22s ease, box-shadow .22s ease;
}

.mini-upcoming:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(15,42,69,.08);
}

.mini-upcoming::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 0;
    width: 4px;
    background: linear-gradient(180deg, var(--accent), var(--accent2));
}

.mini-upcoming::after {
    content: "";
    position: absolute;
    width: 82px;
    height: 82px;
    border-radius: 50%;
    right: -32px;
    top: -34px;
    background: radial-gradient(circle, var(--bubble) 0%, rgba(255,255,255,0) 72%);
}

.mini-upcoming .icon {
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

.mini-upcoming .label {
    position: relative;
    z-index: 2;
    color: #60758C;
    font-size: .52rem;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: .04em;
    margin-bottom: .18rem;
}

.mini-upcoming .value {
    position: relative;
    z-index: 2;
    color: #0F2A45;
    font-size: 1.42rem;
    font-weight: 900;
    line-height: 1.05;
    margin-bottom: .18rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.mini-upcoming .note {
    position: relative;
    z-index: 2;
    color: #8293A8;
    font-size: .55rem;
    line-height: 1.20;
    margin-top: .17rem;
}

.mini-upcoming .mini-line {
    position: absolute;
    left: .72rem;
    right: .72rem;
    bottom: .36rem;
    height: 2px;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: .20;
}

@keyframes upcomingFloat {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-4px); }
}

.mini-blue {
    --accent:#2563EB; --accent2:#60A5FA; --wash:#F2F7FF;
    --border:#D7E5FF; --bubble:#DCE9FF; --iconbg:#EAF2FF;
}
.mini-cyan {
    --accent:#0891B2; --accent2:#22D3EE; --wash:#F0FBFD;
    --border:#D2F0F6; --bubble:#D8F5FA; --iconbg:#E6F9FC;
}
.mini-amber {
    --accent:#D98B16; --accent2:#FBBF24; --wash:#FFF9EE;
    --border:#F6E6C4; --bubble:#FFF0CF; --iconbg:#FFF5DF;
}
.mini-violet {
    --accent:#7C3AED; --accent2:#A78BFA; --wash:#F7F3FF;
    --border:#E6DBFF; --bubble:#E9DEFF; --iconbg:#F0E9FF;
}

/* Status Snapshot: compact executive rows */
.status-mini {
    height: 69px;
    box-sizing: border-box;
    background: linear-gradient(145deg, #FFFFFF 0%, #F9FBFE 100%);
    border: 1px solid #DDE6F0;
    border-radius: 10px;
    padding: .34rem .52rem;
    box-shadow: 0 3px 10px rgba(15,42,69,.022);
    overflow: hidden;
}

.status-mini .label {
    color: #74879D;
    font-size: .55rem;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: .045em;
}

.status-mini .value {
    color: #0F2A45;
    font-size: .94rem;
    font-weight: 900;
    margin-top: .07rem;
    line-height: 1.05;
}

.status-mini .note {
    color: #8798AB;
    font-size: .54rem;
    margin-top: .06rem;
    line-height: 1.20;
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
    .live-badge-custom,
    .live-dot,
    .pro-kpi,
    .chart-insight,
    .chart-insight::after,
    .chart-insight .ititle,
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


def pinned_status_insight(title, text, tone="blue"):
    tone_class = "" if tone == "blue" else tone
    st.markdown(
        (
            f'<div class="chart-insight status-insight-pin {tone_class}">'
            f'<div class="ititle">{title}</div>'
            f'<div class="ibody">{text}</div>'
            f'</div>'
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


def mini_insight(label, value, note, icon, css_class):
    st.markdown(
        (
            f'<div class="mini-upcoming {css_class}">'
            f'<div class="icon">{icon}</div>'
            f'<div class="label">{label}</div>'
            f'<div class="value">{value}</div>'
            f'<div class="note">{note}</div>'
            f'<div class="mini-line"></div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def status_mini(label, value, note):
    st.markdown(
        (
            '<div class="status-mini">'
            f'<div class="label">{label}</div>'
            f'<div class="value">{value}</div>'
            f'<div class="note">{note}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def status_snapshot_stack(items):
    cards = "".join(
        (
            '<div class="status-mini">'
            f'<div class="label">{label}</div>'
            f'<div class="value">{value}</div>'
            f'<div class="note">{note}</div>'
            '</div>'
        )
        for label, value, note in items
    )

    st.markdown(
        (
            '<div style="display:grid;grid-template-columns:1fr;'
            'gap:6px;margin-top:2px;">'
            f'{cards}'
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
# LOAD + OVERVIEW-SPECIFIC NORMALIZATION
# =========================================================
df = load_data().copy()

# Google Sheet headers are trimmed in common.clean_data(), but keep this page
# defensive because the source workbook can be updated by different campuses.
df.columns = df.columns.astype(str).str.strip()

# Normalize Event values locally. The workbook header may appear as "Event ".
if "Event" in df.columns:
    df["Event"] = (
        df["Event"]
        .astype("string")
        .str.strip()
        .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA})
    )

# Lucknow currently uses a slightly different reach header. Combine aliases
# into the canonical dashboard fields without changing the Google Sheet.
reach_aliases = {
    "Planned Student Reach": [
        "Planned Student / faculty Reach",
        "Planned Student / Faculty Reach",
    ],
    "Actual Student Reach": [
        "Actual Student / Faculty Reach",
        "Actual Student / faculty Reach",
    ],
}

for canonical, aliases in reach_aliases.items():
    if canonical in df.columns:
        df[canonical] = pd.to_numeric(df[canonical], errors="coerce")
    else:
        df[canonical] = pd.Series(pd.NA, index=df.index, dtype="Float64")

    for alias in aliases:
        if alias in df.columns:
            alias_values = pd.to_numeric(df[alias], errors="coerce")
            df[canonical] = df[canonical].combine_first(alias_values)

# Normalize fields needed by the Overview intelligence layer.
for text_col in [
    "Campus",
    "Activity Type",
    "Status",
    "Target Segment",
    "Activity Owner",
    "Priority",
    "Follow-up Required",
    "Relationship Strength",
    "Month",
]:
    if text_col in df.columns:
        df[text_col] = (
            df[text_col]
            .astype("string")
            .str.strip()
            .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA})
        )

for title_col in ["Status", "Priority", "Relationship Strength", "Month"]:
    if title_col in df.columns:
        df[title_col] = df[title_col].str.title()

for date_col in ["Activity Date", "Event Date", "Next Follow-up Date"]:
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce")


# =========================================================
# OVERVIEW-ONLY DESIGN ADDITIONS
# Existing title/sidebar/live-dot/KPI/insight animations remain untouched.
# =========================================================
st.markdown(
    """
    <style>
    .overview-section-kicker {
        margin-top: .32rem;
        margin-bottom: .04rem;
        color: #2B6DE8;
        font-size: .63rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: .10em;
    }

    .overview-section-title {
        color: #102A43;
        font-size: 1.06rem;
        font-weight: 900;
        letter-spacing: -.01em;
        margin-bottom: .04rem;
    }

    .overview-section-sub {
        color: #7B8DA3;
        font-size: .72rem;
        line-height: 1.35;
        margin-bottom: .34rem;
    }

    .overview-divider {
        height: 1px;
        width: 100%;
        margin: .18rem 0 .46rem 0;
        background: linear-gradient(90deg, #D7E4F4 0%, #EDF2F7 58%, rgba(237,242,247,0) 100%);
    }

    .ems-chip {
        display: inline-block;
        padding: .12rem .36rem;
        margin-right: .28rem;
        border-radius: 999px;
        background: #EAF2FF;
        border: 1px solid #D6E5FF;
        color: #245EBA;
        font-size: .55rem;
        font-weight: 900;
        letter-spacing: .025em;
        text-transform: uppercase;
    }

    .filter-note {
        color: #8495A9;
        font-size: .60rem;
        margin-top: -.10rem;
        margin-bottom: .08rem;
    }

    div[data-testid="stButton"] button {
        min-height: 2.34rem !important;
        height: 2.34rem !important;
        border-radius: 10px !important;
        border: 1px solid #DCE6F1 !important;
        color: #245EBA !important;
        background: linear-gradient(145deg,#FFFFFF 0%,#F5F8FC 100%) !important;
        font-size: .73rem !important;
        font-weight: 850 !important;
        box-shadow: 0 3px 10px rgba(15,42,69,.035) !important;
        transition: transform .20s ease, box-shadow .20s ease !important;
    }

    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 18px rgba(37,99,235,.11) !important;
        border-color: #C7D9F5 !important;
    }

    .action-strip-title {
        color: #102A43;
        font-size: .98rem;
        font-weight: 850;
        margin-top: .10rem;
        margin-bottom: .05rem;
    }

    .action-strip-sub {
        color: #7D8FA5;
        font-size: .69rem;
        margin-bottom: .28rem;
    }

    @media (max-width: 1050px) {
        .pro-kpi .value { font-size: 1.18rem !important; }
        .mini-upcoming .value { font-size: 1.18rem !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# OVERVIEW HELPERS
# =========================================================
def _options(frame, column):
    if column not in frame.columns:
        return ["All"]

    values = (
        frame[column]
        .dropna()
        .astype(str)
        .str.strip()
    )
    values = values[values.ne("")]
    return ["All"] + sorted(values.unique().tolist(), key=lambda x: x.lower())


def _reset_overview_filters():
    for key in [
        "ov_campus",
        "ov_activity",
        "ov_event",
        "ov_status",
        "ov_segment",
        "ov_owner",
        "ov_priority",
        "ov_date",
    ]:
        st.session_state.pop(key, None)


def _safe_name(value, fallback="N/A"):
    if value is None or pd.isna(value):
        return fallback
    value = str(value).strip()
    return html.escape(value) if value else fallback


def _pct(num, den):
    return (float(num) / float(den) * 100.0) if den else 0.0


def overview_section(kicker, title, subtitle):
    st.markdown(
        (
            f'<div class="overview-section-kicker">{html.escape(kicker)}</div>'
            f'<div class="overview-section-title">{html.escape(title)}</div>'
            f'<div class="overview-section-sub">{html.escape(subtitle)}</div>'
            '<div class="overview-divider"></div>'
        ),
        unsafe_allow_html=True,
    )


def ems_insight(title, finding, impact, action, tone="blue"):
    body = (
        '<span class="ems-chip">Finding</span>' + html.escape(str(finding)) + '<br>'
        '<span class="ems-chip">Impact</span>' + html.escape(str(impact)) + '<br>'
        '<span class="ems-chip">Action</span>' + html.escape(str(action))
    )
    chart_insight(title, body, tone)


def _status_color_map():
    return {
        "Completed": "#2F9B6B",
        "Confirmed": "#2F6FBC",
        "Planned": "#8FC2E8",
        "Cancelled": "#D65A63",
        "Rescheduled": "#D99A32",
    }


# =========================================================
# HEADER — preserve existing title motion and styling
# =========================================================
header_html = (
    '<div class="overview-header">'
    '<div class="overview-eyebrow">PGDM Outreach Intelligence</div>'
    '<div class="overview-title-row">'
    '<div class="overview-title-wrap">'
    '<div class="overview-title">Outreach Overview</div>'
    '</div>'
    '</div>'
    '<div class="overview-subtitle">'
    'Campus outreach planning, event execution, reach performance and management intelligence.'
    '</div>'
    '<div class="overview-accent"></div>'
    '</div>'
)
st.markdown(header_html, unsafe_allow_html=True)


# =========================================================
# FILTERS
# Order locked: Campus → Activity Type → Event → Status →
# Target Segment → Owner → Priority → Date Range → Reset
# =========================================================
st.markdown('<div class="filter-panel-title">Filters</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="filter-note">All charts, KPIs and EMS insights respond to the selected filters.</div>',
    unsafe_allow_html=True,
)

filter_cols = st.columns(
    [0.86, 1.06, 0.84, 0.86, 1.10, 0.96, 0.76, 1.34, 0.60],
    gap="small",
)

with filter_cols[0]:
    campus_filter = st.selectbox(
        "Campus",
        _options(df, "Campus"),
        key="ov_campus",
    )

with filter_cols[1]:
    activity_filter = st.selectbox(
        "Activity Type",
        _options(df, "Activity Type"),
        key="ov_activity",
    )

with filter_cols[2]:
    event_filter = st.selectbox(
        "Event",
        _options(df, "Event"),
        key="ov_event",
    )

with filter_cols[3]:
    status_filter = st.selectbox(
        "Status",
        _options(df, "Status"),
        key="ov_status",
    )

with filter_cols[4]:
    segment_filter = st.selectbox(
        "Target Segment",
        _options(df, "Target Segment"),
        key="ov_segment",
    )

with filter_cols[5]:
    owner_filter = st.selectbox(
        "Owner",
        _options(df, "Activity Owner"),
        key="ov_owner",
    )

with filter_cols[6]:
    priority_filter = st.selectbox(
        "Priority",
        _options(df, "Priority"),
        key="ov_priority",
    )

with filter_cols[7]:
    date_range = None
    if "Activity Date" in df.columns and df["Activity Date"].notna().any():
        min_date = df["Activity Date"].min().date()
        max_date = df["Activity Date"].max().date()
        date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="ov_date",
        )
    else:
        st.text_input("Date Range", value="", disabled=True)

with filter_cols[8]:
    st.markdown(
        '<div class="overview-filter-reset-spacer">&nbsp;</div>',
        unsafe_allow_html=True,
    )
    if st.button("↻ Reset", width="stretch", key="ov_reset"):
        _reset_overview_filters()
        st.rerun()


# =========================================================
# APPLY FILTERS
# =========================================================
filtered = df.copy()

filter_map = [
    ("Campus", campus_filter),
    ("Activity Type", activity_filter),
    ("Event", event_filter),
    ("Status", status_filter),
    ("Target Segment", segment_filter),
    ("Activity Owner", owner_filter),
    ("Priority", priority_filter),
]

for column, selected in filter_map:
    if selected != "All" and column in filtered.columns:
        filtered = filtered[filtered[column].eq(selected)]

if (
    date_range
    and isinstance(date_range, (list, tuple))
    and len(date_range) == 2
    and "Activity Date" in filtered.columns
):
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)
    filtered = filtered[
        filtered["Activity Date"].ge(start_date)
        & filtered["Activity Date"].lt(end_date)
    ]

if filtered.empty:
    st.warning("No outreach data is available for the selected filters.")
    st.stop()


# =========================================================
# SHARED METRICS / EVENT SUBSET
# =========================================================
today = pd.Timestamp.today().normalize()

event_mask = (
    filtered["Event"].notna()
    if "Event" in filtered.columns
    else pd.Series(False, index=filtered.index)
)
event_df = filtered[event_mask].copy()

total_activities = int(len(filtered))
total_events = int(len(event_df))

institutions = (
    int(filtered["Institution / Event Name"].dropna().nunique())
    if "Institution / Event Name" in filtered.columns
    else 0
)

cities = (
    int(filtered["City"].dropna().nunique())
    if "City" in filtered.columns
    else 0
)

planned_reach_value = pd.to_numeric(
    filtered.get("Planned Student Reach", pd.Series(index=filtered.index, dtype=float)),
    errors="coerce",
).sum(min_count=1)

actual_reach_value = pd.to_numeric(
    filtered.get("Actual Student Reach", pd.Series(index=filtered.index, dtype=float)),
    errors="coerce",
).sum(min_count=1)

planned_reach = 0 if pd.isna(planned_reach_value) else int(planned_reach_value)
actual_reach = 0 if pd.isna(actual_reach_value) else int(actual_reach_value)
reach_achievement = _pct(actual_reach, planned_reach)


# =========================================================
# EXECUTIVE SNAPSHOT
# =========================================================
overview_section(
    "Executive Snapshot",
    "Outreach Performance at a Glance",
    "Core volume, event coverage and student-reach indicators for the current filter selection.",
)

k1, k2, k3, k4, k5, k6 = st.columns(6, gap="small")

with k1:
    professional_kpi(
        "Total Activities",
        f"{total_activities:,}",
        "Filtered outreach activity volume",
        "●",
        "kpi-blue",
    )

with k2:
    professional_kpi(
        "Total Events",
        f"{total_events:,}",
        "Records with Event populated",
        "✦",
        "kpi-cyan",
    )

with k3:
    professional_kpi(
        "Institutions",
        f"{institutions:,}",
        "Unique institutions / event names",
        "◆",
        "kpi-violet",
    )

with k4:
    professional_kpi(
        "Cities Covered",
        f"{cities:,}",
        "Current outreach footprint",
        "⌖",
        "kpi-teal",
    )

with k5:
    professional_kpi(
        "Planned Reach",
        f"{planned_reach:,}",
        "Planned student / faculty reach",
        "◎",
        "kpi-amber",
    )

with k6:
    professional_kpi(
        "Actual Reach",
        f"{actual_reach:,}",
        f"{reach_achievement:.1f}% of planned reach" if planned_reach else "Actual reach entered",
        "✓",
        "kpi-green",
    )


# =========================================================
# Q1 — CAMPUS ACTIVITY PORTFOLIO
# =========================================================
overview_section(
    "Q1 · Activity Portfolio",
    "Campus-wise Activities + Activity Type",
    "Compare campus workload and identify which activity formats are driving the outreach plan.",
)

with st.container(border=True):
    chart_header(
        "Campus Activity Portfolio",
        "Horizontal stacked bars show activity volume and the mix of Activity Type within each campus.",
    )

    activity_mix = pd.DataFrame()
    if {"Campus", "Activity Type"}.issubset(filtered.columns):
        activity_mix = (
            filtered.dropna(subset=["Campus", "Activity Type"])
            .groupby(["Campus", "Activity Type"], observed=True)
            .size()
            .reset_index(name="Activities")
        )

    if activity_mix.empty:
        st.info("No campus/activity-type data is available for the selected filters.")
    else:
        campus_totals = (
            activity_mix.groupby("Campus", observed=True)["Activities"]
            .sum()
            .sort_values(ascending=False)
        )
        campus_order = campus_totals.index.tolist()

        fig = px.bar(
            activity_mix,
            x="Activities",
            y="Campus",
            color="Activity Type",
            orientation="h",
            barmode="stack",
            text="Activities",
            category_orders={"Campus": campus_order},
        )
        fig.update_traces(
            textposition="inside",
            textfont=dict(size=9),
            marker_line_width=0,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Activity Type: %{fullData.name}<br>"
                "Activities: %{x:.0f}<extra></extra>"
            ),
        )
        fig.update_xaxes(title="Activity Count", rangemode="tozero", dtick=1)
        fig.update_yaxes(
            title="",
            categoryorder="array",
            categoryarray=campus_order,
            autorange="reversed",
        )
        fig = professional_chart(fig, 330, legend=True)
        fig.update_layout(legend_title_text="Activity Type", bargap=.28)

        st.plotly_chart(fig, width="stretch", config=CHART_CONFIG)

        leader_campus = campus_totals.index[0]
        leader_count = int(campus_totals.iloc[0])
        leader_mix = (
            activity_mix[activity_mix["Campus"].eq(leader_campus)]
            .sort_values("Activities", ascending=False)
        )
        leader_type = str(leader_mix.iloc[0]["Activity Type"])
        leader_type_count = int(leader_mix.iloc[0]["Activities"])
        leader_share = _pct(leader_type_count, leader_count)

        campus_avg = float(campus_totals.mean()) if len(campus_totals) else 0
        activity_gap = leader_count - campus_avg

        ems_insight(
            "EMS · Campus Activity Insight",
            f"{leader_campus} leads the selected portfolio with {leader_count} activities; {leader_type} is its largest activity type ({leader_type_count}, {leader_share:.1f}%).",
            f"The leading campus is {activity_gap:.1f} activities above the current campus average, showing where execution capacity is most concentrated.",
            f"Validate whether {leader_type} is producing adequate reach/outcomes; replicate the strongest activity mix only where campus audience and capacity are comparable.",
            "blue",
        )


# =========================================================
# Q2 — CAMPUS EVENT INTELLIGENCE
# =========================================================
overview_section(
    "Q2 · Event Intelligence",
    "Campus-wise Events + Event Type + Status",
    "Separate event portfolio volume from event execution health so management can see both scale and readiness.",
)

q2_left, q2_right = st.columns([1.05, .95], gap="medium", vertical_alignment="top")

with q2_left:
    with st.container(border=True):
        chart_header(
            "Event Portfolio by Campus",
            "Event-filled records segmented by Event type.",
        )

        event_mix = pd.DataFrame()
        if not event_df.empty and {"Campus", "Event"}.issubset(event_df.columns):
            event_mix = (
                event_df.dropna(subset=["Campus", "Event"])
                .groupby(["Campus", "Event"], observed=True)
                .size()
                .reset_index(name="Events")
            )

        if event_mix.empty:
            st.info("No Event values are available for the selected filters.")
        else:
            event_totals = (
                event_mix.groupby("Campus", observed=True)["Events"]
                .sum()
                .sort_values(ascending=False)
            )
            event_campus_order = event_totals.index.tolist()

            fig = px.bar(
                event_mix,
                x="Events",
                y="Campus",
                color="Event",
                orientation="h",
                barmode="stack",
                text="Events",
                category_orders={"Campus": event_campus_order},
            )
            fig.update_traces(
                textposition="inside",
                textfont=dict(size=9),
                marker_line_width=0,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Event Type: %{fullData.name}<br>"
                    "Events: %{x:.0f}<extra></extra>"
                ),
            )
            fig.update_xaxes(title="Event Count", dtick=1, rangemode="tozero")
            fig.update_yaxes(
                title="",
                categoryorder="array",
                categoryarray=event_campus_order,
                autorange="reversed",
            )
            fig = professional_chart(fig, 310, legend=True)
            fig.update_layout(legend_title_text="Event")
            st.plotly_chart(fig, width="stretch", config=CHART_CONFIG)

with q2_right:
    with st.container(border=True):
        chart_header(
            "Event Execution Status",
            "100% status mix by campus; hover shows underlying event counts.",
        )

        event_status = pd.DataFrame()
        if not event_df.empty and {"Campus", "Status"}.issubset(event_df.columns):
            event_status = (
                event_df.dropna(subset=["Campus", "Status"])
                .groupby(["Campus", "Status"], observed=True)
                .size()
                .reset_index(name="Event Count")
            )
            if not event_status.empty:
                event_status["Campus Total"] = event_status.groupby("Campus")["Event Count"].transform("sum")
                event_status["Share %"] = (
                    event_status["Event Count"]
                    / event_status["Campus Total"].replace(0, pd.NA)
                    * 100
                ).fillna(0)
                event_status["Label"] = event_status["Share %"].map(lambda x: f"{x:.0f}%" if x >= 8 else "")

        if event_status.empty:
            st.info("No event status data is available for the selected filters.")
        else:
            status_campus_order = (
                event_status.groupby("Campus", observed=True)["Event Count"]
                .sum()
                .sort_values(ascending=False)
                .index.tolist()
            )

            fig = px.bar(
                event_status,
                x="Share %",
                y="Campus",
                color="Status",
                orientation="h",
                barmode="stack",
                text="Label",
                custom_data=["Event Count", "Campus Total"],
                color_discrete_map=_status_color_map(),
                category_orders={"Campus": status_campus_order},
            )
            fig.update_traces(
                textposition="inside",
                textfont=dict(size=9),
                marker_line_width=0,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Status: %{fullData.name}<br>"
                    "Events: %{customdata[0]:.0f}<br>"
                    "Campus Events: %{customdata[1]:.0f}<br>"
                    "Share: %{x:.1f}%<extra></extra>"
                ),
            )
            fig.update_xaxes(title="Status Share", range=[0, 100], ticksuffix="%")
            fig.update_yaxes(
                title="",
                categoryorder="array",
                categoryarray=status_campus_order,
                autorange="reversed",
            )
            fig = professional_chart(fig, 310, legend=True)
            fig.update_layout(legend_title_text="Status")
            st.plotly_chart(fig, width="stretch", config=CHART_CONFIG)

if event_df.empty:
    ems_insight(
        "EMS · Event Execution Insight",
        "No Event records are visible under the current filter selection.",
        "Event-volume and readiness comparisons cannot be assessed for this selection.",
        "Clear the Event/Status filters or complete the Event field in the source sheet before using event-level management decisions.",
        "amber",
    )
else:
    event_by_campus = (
        event_df.dropna(subset=["Campus"])
        .groupby("Campus", observed=True)
        .size()
        .sort_values(ascending=False)
        if "Campus" in event_df.columns
        else pd.Series(dtype=int)
    )
    event_leader = str(event_by_campus.index[0]) if not event_by_campus.empty else "N/A"
    event_leader_count = int(event_by_campus.iloc[0]) if not event_by_campus.empty else total_events

    event_type_counts = event_df["Event"].value_counts() if "Event" in event_df.columns else pd.Series(dtype=int)
    top_event_type = str(event_type_counts.index[0]) if not event_type_counts.empty else "N/A"

    completed_events = int(event_df["Status"].eq("Completed").sum()) if "Status" in event_df.columns else 0
    confirmed_events = int(event_df["Status"].eq("Confirmed").sum()) if "Status" in event_df.columns else 0
    planned_events = int(event_df["Status"].eq("Planned").sum()) if "Status" in event_df.columns else 0
    event_completion = _pct(completed_events, total_events)
    forward_load = confirmed_events + planned_events
    forward_share = _pct(forward_load, total_events)

    ems_insight(
        "EMS · Event Execution Insight",
        f"{event_leader} has the highest visible event volume ({event_leader_count}); {top_event_type} is the most common Event type. Completed events represent {event_completion:.1f}% of visible events.",
        f"{forward_load} events ({forward_share:.1f}%) are still Confirmed/Planned, which indicates the forward execution load that needs owner and resource readiness.",
        f"Prioritize the Confirmed/Planned event queue for {event_leader}; verify owners, resource persons and dates before adding more event volume.",
        "teal",
    )


# =========================================================
# Q3 — MONTHLY ACTIVITY + EVENT MOMENTUM
# =========================================================
overview_section(
    "Q3 · Monthly Momentum",
    "Monthly Activity Count + Event Count",
    "Track seasonality and whether event execution is moving at the same pace as the overall outreach plan.",
)

with st.container(border=True):
    chart_header(
        "Monthly Outreach Momentum",
        "Columns = all activities; line = records where Event is populated.",
    )

    monthly = pd.DataFrame()
    if "Activity Date" in filtered.columns and filtered["Activity Date"].notna().any():
        monthly_base = filtered.dropna(subset=["Activity Date"]).copy()
        monthly_base["Month Start"] = monthly_base["Activity Date"].dt.to_period("M").dt.to_timestamp()

        activity_month = (
            monthly_base.groupby("Month Start", observed=True)
            .size()
            .rename("Activities")
        )

        event_month = (
            monthly_base[monthly_base["Event"].notna()]
            .groupby("Month Start", observed=True)
            .size()
            .rename("Events")
            if "Event" in monthly_base.columns
            else pd.Series(dtype=int, name="Events")
        )

        monthly = (
            pd.concat([activity_month, event_month], axis=1)
            .fillna(0)
            .reset_index()
            .sort_values("Month Start")
        )
        monthly["Activities"] = monthly["Activities"].astype(int)
        monthly["Events"] = monthly["Events"].astype(int)
        monthly["Month"] = monthly["Month Start"].dt.strftime("%b %Y")

    if monthly.empty:
        st.info("Monthly trend cannot be calculated because Activity Date is unavailable for this selection.")
    else:
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=monthly["Month"],
                y=monthly["Activities"],
                name="Activities",
                marker_color="#2F6FBC",
                opacity=.88,
                text=monthly["Activities"],
                textposition="outside",
                textfont=dict(size=9),
                hovertemplate="<b>%{x}</b><br>Activities: %{y:.0f}<extra></extra>",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=monthly["Month"],
                y=monthly["Events"],
                name="Events",
                mode="lines+markers+text",
                line=dict(color="#7C3AED", width=3),
                marker=dict(size=8, color="#7C3AED", line=dict(color="#FFFFFF", width=1.5)),
                text=monthly["Events"],
                textposition="top center",
                textfont=dict(size=9, color="#6D43C5"),
                hovertemplate="<b>%{x}</b><br>Events: %{y:.0f}<extra></extra>",
            )
        )
        fig.update_xaxes(title="", showgrid=False)
        fig.update_yaxes(title="Count", rangemode="tozero", dtick=1)
        fig = professional_chart(fig, 335, legend=True)
        fig.update_layout(bargap=.42)
        st.plotly_chart(fig, width="stretch", config=CHART_CONFIG)

        peak_activity_row = monthly.loc[monthly["Activities"].idxmax()]
        peak_event_row = monthly.loc[monthly["Events"].idxmax()]
        latest_row = monthly.iloc[-1]
        previous_row = monthly.iloc[-2] if len(monthly) > 1 else None

        if previous_row is not None and previous_row["Activities"]:
            momentum_change = (latest_row["Activities"] - previous_row["Activities"]) / previous_row["Activities"] * 100
            direction = "increased" if momentum_change >= 0 else "decreased"
            momentum_sentence = f"Latest monthly activity volume has {direction} by {abs(momentum_change):.1f}% versus the previous visible month."
        else:
            momentum_sentence = "Only one comparable month is visible under the current filters."

        ems_insight(
            "EMS · Monthly Momentum Insight",
            f"{peak_activity_row['Month']} is the peak activity month with {int(peak_activity_row['Activities'])} activities; {peak_event_row['Month']} has the highest event count ({int(peak_event_row['Events'])}).",
            momentum_sentence,
            "Use the peak-month activity mix as the capacity baseline; if event growth lags activity growth, review whether the added activity volume is generating sufficiently high-impact engagement.",
            "violet",
        )


# =========================================================
# REACH PERFORMANCE
# =========================================================
overview_section(
    "Reach Performance",
    "Campus Planned vs Actual Reach",
    "A bullet-style comparison shows whether outreach execution is translating into the intended student/faculty reach.",
)

with st.container(border=True):
    chart_header(
        "Campus Reach Achievement",
        "Wide bar = Planned Reach; overlay = Actual Reach. Percentage label shows achievement against plan.",
    )

    reach_data = pd.DataFrame()
    if "Campus" in filtered.columns:
        reach_base = filtered.copy()
        reach_base["Planned Student Reach"] = pd.to_numeric(reach_base["Planned Student Reach"], errors="coerce")
        reach_base["Actual Student Reach"] = pd.to_numeric(reach_base["Actual Student Reach"], errors="coerce")

        reach_data = (
            reach_base.groupby("Campus", observed=True)[["Planned Student Reach", "Actual Student Reach"]]
            .sum(min_count=1)
            .reset_index()
            .rename(columns={
                "Planned Student Reach": "Planned Reach",
                "Actual Student Reach": "Actual Reach",
            })
        )
        reach_data = reach_data[
            reach_data[["Planned Reach", "Actual Reach"]].notna().any(axis=1)
        ].copy()
        reach_data[["Planned Reach", "Actual Reach"]] = reach_data[["Planned Reach", "Actual Reach"]].fillna(0)
        reach_data["Achievement %"] = reach_data.apply(
            lambda r: _pct(r["Actual Reach"], r["Planned Reach"]), axis=1
        )
        reach_data = reach_data.sort_values(["Planned Reach", "Actual Reach"], ascending=False)

    if reach_data.empty or reach_data[["Planned Reach", "Actual Reach"]].sum().sum() == 0:
        st.info("No Planned/Actual Reach values are available for the selected filters.")
    else:
        campus_order = reach_data["Campus"].tolist()
        actual_text = [
            f"{int(v):,}  ·  {p:.0f}%"
            for v, p in zip(reach_data["Actual Reach"], reach_data["Achievement %"])
        ]

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=reach_data["Planned Reach"],
                y=reach_data["Campus"],
                name="Planned Reach",
                orientation="h",
                width=.64,
                marker_color="#D9E6F4",
                hovertemplate="<b>%{y}</b><br>Planned Reach: %{x:,.0f}<extra></extra>",
            )
        )
        fig.add_trace(
            go.Bar(
                x=reach_data["Actual Reach"],
                y=reach_data["Campus"],
                name="Actual Reach",
                orientation="h",
                width=.34,
                marker_color="#0F9F8F",
                text=actual_text,
                textposition="outside",
                textfont=dict(size=9, color="#0C776C"),
                customdata=reach_data[["Planned Reach", "Achievement %"]].values,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Actual Reach: %{x:,.0f}<br>"
                    "Planned Reach: %{customdata[0]:,.0f}<br>"
                    "Achievement: %{customdata[1]:.1f}%<extra></extra>"
                ),
            )
        )
        fig.update_layout(barmode="overlay")
        fig.update_xaxes(title="Reach", rangemode="tozero")
        fig.update_yaxes(
            title="",
            categoryorder="array",
            categoryarray=campus_order,
            autorange="reversed",
        )
        fig = professional_chart(fig, 320, legend=True)
        st.plotly_chart(fig, width="stretch", config=CHART_CONFIG)

        reliable_reach = reach_data[reach_data["Planned Reach"] > 0].copy()
        if not reliable_reach.empty:
            best_reach_row = reliable_reach.sort_values(["Achievement %", "Actual Reach"], ascending=False).iloc[0]
            weakest_reach_row = reliable_reach.sort_values(["Achievement %", "Planned Reach"], ascending=[True, False]).iloc[0]

            best_campus = str(best_reach_row["Campus"])
            best_pct = float(best_reach_row["Achievement %"])
            weak_campus = str(weakest_reach_row["Campus"])
            weak_pct = float(weakest_reach_row["Achievement %"])

            ems_insight(
                "EMS · Reach Efficiency Insight",
                f"{best_campus} has the strongest visible reach achievement at {best_pct:.1f}% of plan; {weak_campus} is currently lowest at {weak_pct:.1f}%.",
                f"The gap between the best and lowest campus is {best_pct - weak_pct:.1f} percentage points, indicating different execution efficiency or data-completion levels.",
                f"Review activity type, audience quality and actual-reach data capture for {weak_campus} before increasing its planned volume.",
                "teal",
            )


# =========================================================
# EXECUTION & ACTION HEALTH
# =========================================================
overview_section(
    "Execution & Action Health",
    "Immediate Operational Signals",
    "Compact operational indicators surface current execution load, follow-up risk and near-term event readiness.",
)

status_series = filtered["Status"] if "Status" in filtered.columns else pd.Series(index=filtered.index, dtype="string")
completed_count = int(status_series.eq("Completed").sum())
confirmed_count = int(status_series.eq("Confirmed").sum())
planned_count = int(status_series.eq("Planned").sum())

open_mask = ~status_series.isin(CLOSED_STATUSES) if "Status" in filtered.columns else pd.Series(True, index=filtered.index)
high_priority_open = (
    int((filtered["Priority"].eq("High") & open_mask).sum())
    if "Priority" in filtered.columns
    else 0
)

followup_required = (
    int(filtered["Follow-up Required"].str.casefold().eq("yes").sum())
    if "Follow-up Required" in filtered.columns
    else 0
)

overdue_followup = 0
if "Next Follow-up Date" in filtered.columns:
    overdue_followup = int(
        (
            filtered["Next Follow-up Date"].notna()
            & filtered["Next Follow-up Date"].lt(today)
            & open_mask
        ).sum()
    )

upcoming_event_count = 0
if not event_df.empty:
    event_dates = (
        event_df["Event Date"].combine_first(event_df["Activity Date"])
        if {"Event Date", "Activity Date"}.issubset(event_df.columns)
        else event_df["Event Date"] if "Event Date" in event_df.columns
        else event_df["Activity Date"] if "Activity Date" in event_df.columns
        else pd.Series(pd.NaT, index=event_df.index)
    )
    event_open = (
        ~event_df["Status"].isin(CLOSED_STATUSES)
        if "Status" in event_df.columns
        else pd.Series(True, index=event_df.index)
    )
    upcoming_event_count = int(
        (
            event_dates.ge(today)
            & event_dates.le(today + pd.Timedelta(days=30))
            & event_open
        ).sum()
    )

ah1, ah2, ah3, ah4, ah5, ah6 = st.columns(6, gap="small")
with ah1:
    mini_insight("Completed", f"{completed_count:,}", "Executed activities", "✓", "mini-blue")
with ah2:
    mini_insight("Confirmed", f"{confirmed_count:,}", "Ready / committed", "●", "mini-cyan")
with ah3:
    mini_insight("Planned", f"{planned_count:,}", "Future planned load", "↗", "mini-violet")
with ah4:
    mini_insight("High Priority Open", f"{high_priority_open:,}", "Needs active ownership", "!", "mini-amber")
with ah5:
    mini_insight("Follow-up Required", f"{followup_required:,}", "Marked Yes in source", "↻", "mini-blue")
with ah6:
    mini_insight("Upcoming Events", f"{upcoming_event_count:,}", "Next 30 days", "✦", "mini-cyan")

completion_rate = _pct(completed_count, total_activities)
open_count = int(open_mask.sum()) if len(open_mask) else 0

if overdue_followup > 0:
    ops_action = f"Escalate {overdue_followup} overdue follow-up(s) first, then lock ownership for high-priority open activities."
elif high_priority_open > 0:
    ops_action = f"Review the {high_priority_open} high-priority open activities and confirm next action/date for each owner."
elif upcoming_event_count > 0:
    ops_action = f"Protect execution quality for the {upcoming_event_count} event(s) scheduled in the next 30 days."
else:
    ops_action = "No immediate follow-up risk is visible; focus on improving reach capture and closing planned activities."

ems_insight(
    "EMS · Execution Health Insight",
    f"{completed_count} of {total_activities} activities are Completed ({completion_rate:.1f}%); {open_count} records remain outside the closed-status set.",
    f"There are {high_priority_open} high-priority open activities, {followup_required} records marked for follow-up and {overdue_followup} overdue follow-up dates.",
    ops_action,
    "amber",
)


# =========================================================
# MANAGEMENT INTELLIGENCE
# =========================================================
overview_section(
    "Management Intelligence",
    "Executive Signals & Next Best Action",
    "Four management cards convert the filtered report into concise decision signals.",
)

# Activity leader
activity_leader = "N/A"
activity_leader_count = 0
if "Campus" in filtered.columns and filtered["Campus"].notna().any():
    activity_leader_series = filtered["Campus"].value_counts()
    activity_leader = str(activity_leader_series.index[0])
    activity_leader_count = int(activity_leader_series.iloc[0])

# Event leader
event_leader_card = "N/A"
event_leader_card_count = 0
if not event_df.empty and "Campus" in event_df.columns and event_df["Campus"].notna().any():
    event_leader_series = event_df["Campus"].value_counts()
    event_leader_card = str(event_leader_series.index[0])
    event_leader_card_count = int(event_leader_series.iloc[0])

# Best reach campus
best_reach_card = "N/A"
best_reach_card_pct = 0.0
if "reach_data" in locals() and not reach_data.empty:
    valid_reach_card = reach_data[reach_data["Planned Reach"] > 0]
    if not valid_reach_card.empty:
        rr = valid_reach_card.sort_values(["Achievement %", "Actual Reach"], ascending=False).iloc[0]
        best_reach_card = str(rr["Campus"])
        best_reach_card_pct = float(rr["Achievement %"])

# Immediate action label
if overdue_followup > 0:
    immediate_action_label = "Follow-up Escalation"
    immediate_action_note = f"{overdue_followup} overdue follow-up(s)"
elif high_priority_open > 0:
    immediate_action_label = "High Priority Queue"
    immediate_action_note = f"{high_priority_open} open high-priority activities"
elif upcoming_event_count > 0:
    immediate_action_label = "Upcoming Event Readiness"
    immediate_action_note = f"{upcoming_event_count} event(s) in next 30 days"
else:
    immediate_action_label = "Reach Optimisation"
    immediate_action_note = "Improve actual-reach capture / efficiency"

m1, m2, m3, m4 = st.columns(4, gap="small")
with m1:
    mini_insight(
        "Activity Leader",
        activity_leader,
        f"{activity_leader_count} filtered activities",
        "🏆",
        "mini-blue",
    )
with m2:
    mini_insight(
        "Event Leader",
        event_leader_card,
        f"{event_leader_card_count} visible events",
        "✦",
        "mini-violet",
    )
with m3:
    mini_insight(
        "Best Reach Achievement",
        best_reach_card,
        f"{best_reach_card_pct:.1f}% of planned reach" if best_reach_card != "N/A" else "Reach data unavailable",
        "◎",
        "mini-cyan",
    )
with m4:
    mini_insight(
        "Immediate Action",
        immediate_action_label,
        immediate_action_note,
        "⚡",
        "mini-amber",
    )

chart_insight(
    "Executive Management Summary",
    (
        f"<b>Activity:</b> {_safe_name(activity_leader)} leads volume with {activity_leader_count} activities. "
        f"<b>Events:</b> {_safe_name(event_leader_card)} leads event volume with {event_leader_card_count}. "
        f"<b>Reach:</b> {_safe_name(best_reach_card)} is the strongest visible reach-achievement campus "
        f"({best_reach_card_pct:.1f}%). <b>Next action:</b> {html.escape(immediate_action_label)} — "
        f"{html.escape(immediate_action_note)}."
    ),
    "violet",
)
