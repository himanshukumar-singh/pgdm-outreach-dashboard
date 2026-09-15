import html
import math
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
    transform: translateY(-43px);
    margin-bottom: -37px;
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
    font-size: .82rem;
    margin-top: -.03rem;
}

.overview-accent {
    height: 2px;
    margin-top: .28rem;
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
    font-size: .94rem;
    font-weight: 880;
    margin: -.05rem 0 .08rem 0;
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
    height: 1.34rem;
    margin: 0 !important;
    padding: 0 !important;
}

/* Overview Reset: same row + same control height */
div[data-testid="stButton"] {
    margin: 0 !important;
}

div[data-testid="stButton"] button {
    min-height: 2.34rem !important;
    height: 2.34rem !important;
    padding: 0 .42rem !important;
    font-size: .69rem !important;
    white-space: nowrap !important;
    border-radius: 9px !important;
}

/* ---------- KPI cards ---------- */
.pro-kpi {
    position: relative;
    overflow: hidden;
    min-height: 72px;
    height: 72px;
    box-sizing: border-box;
    border-radius: 13px;
    padding: .46rem .58rem .42rem .58rem;
    background:
        linear-gradient(118deg, rgba(255,255,255,.98) 0%, rgba(255,255,255,.95) 58%, var(--wash) 155%);
    border: 1px solid rgba(216,226,238,.92);
    box-shadow:
        0 8px 22px rgba(22,48,78,.055),
        inset 0 1px 0 rgba(255,255,255,.92);
    display: grid;
    grid-template-columns: 31px minmax(0,1fr);
    grid-template-rows: 15px 25px 14px;
    column-gap: .48rem;
    align-items: center;
    animation: kpiFloat 5.2s ease-in-out infinite;
    transition:
        transform .22s ease,
        box-shadow .22s ease,
        border-color .22s ease;
}

.pro-kpi:hover {
    transform: translateY(-3px) scale(1.008);
    border-color: var(--border);
    box-shadow:
        0 13px 30px rgba(20,48,82,.095),
        0 0 0 1px rgba(255,255,255,.75) inset;
}

.pro-kpi::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 72%;
    height: 2px;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--accent) 0%, var(--accent2) 48%, rgba(255,255,255,0) 100%);
    opacity: .92;
}

.pro-kpi::after {
    content: "";
    position: absolute;
    width: 76px;
    height: 76px;
    border-radius: 50%;
    right: -31px;
    bottom: -42px;
    background: radial-gradient(circle, var(--bubble) 0%, rgba(255,255,255,0) 72%);
    opacity: .72;
    pointer-events: none;
}

.pro-kpi .icon {
    position: relative;
    z-index: 2;
    grid-column: 1;
    grid-row: 1 / 4;
    width: 29px;
    height: 29px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        linear-gradient(145deg, rgba(255,255,255,.92), var(--iconbg));
    color: var(--accent);
    border: 1px solid var(--border);
    box-shadow: 0 5px 12px rgba(15,42,69,.055);
    font-size: 12px;
    font-weight: 950;
    margin: 0;
}

.pro-kpi .label {
    position: relative;
    z-index: 2;
    grid-column: 2;
    grid-row: 1;
    color: #647A91;
    font-size: .49rem;
    font-weight: 900;
    letter-spacing: .035em;
    text-transform: uppercase;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.pro-kpi .value {
    position: relative;
    z-index: 2;
    grid-column: 2;
    grid-row: 2;
    color: #102A43;
    font-size: 1.34rem;
    font-weight: 950;
    letter-spacing: -.025em;
    line-height: .98;
    margin: 0;
    white-space: nowrap;
}

.pro-kpi .sub {
    position: relative;
    z-index: 2;
    grid-column: 2;
    grid-row: 3;
    color: #8394A7;
    font-size: .46rem;
    line-height: 1.05;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.pro-kpi .mini-line {
    display: none;
}

@keyframes kpiFloat {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-1.5px); }
}

.kpi-blue {
    --accent:#2D6CDF; --accent2:#79A7F8; --wash:#EEF5FF;
    --border:#D8E6FB; --bubble:#D9E9FF; --iconbg:#EAF2FF;
}
.kpi-cyan {
    --accent:#0C8FA6; --accent2:#5BC6D4; --wash:#EDF9FB;
    --border:#D2EDF2; --bubble:#D7F3F6; --iconbg:#E7F8FA;
}
.kpi-violet {
    --accent:#7453C6; --accent2:#A98AE8; --wash:#F5F1FC;
    --border:#E5DCF6; --bubble:#E8DFFC; --iconbg:#F0EAFB;
}
.kpi-teal {
    --accent:#159786; --accent2:#5CC9B9; --wash:#EFF9F6;
    --border:#D5ECE7; --bubble:#D9F1EC; --iconbg:#E8F7F3;
}
.kpi-amber {
    --accent:#D18A24; --accent2:#F1BB58; --wash:#FFF8EC;
    --border:#F1E2C6; --bubble:#F9EBCB; --iconbg:#FFF4DE;
}
.kpi-green {
    --accent:#2A8B5A; --accent2:#6BC78F; --wash:#EFF8F2;
    --border:#D7E9DE; --bubble:#DCEFE3; --iconbg:#EAF6EE;
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
    --accent:#2D6CDF; --accent2:#79A7F8; --wash:#EEF5FF;
    --border:#D8E6FB; --bubble:#D9E9FF; --iconbg:#EAF2FF;
}
.mini-cyan {
    --accent:#0C8FA6; --accent2:#5BC6D4; --wash:#EDF9FB;
    --border:#D2EDF2; --bubble:#D7F3F6; --iconbg:#E7F8FA;
}
.mini-amber {
    --accent:#D18A24; --accent2:#F1BB58; --wash:#FFF8EC;
    --border:#F1E2C6; --bubble:#F9EBCB; --iconbg:#FFF4DE;
}
.mini-violet {
    --accent:#7453C6; --accent2:#A98AE8; --wash:#F5F1FC;
    --border:#E5DCF6; --bubble:#E8DFFC; --iconbg:#F0EAFB;
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
    gap: .40rem;
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

/* =========================================================
   Q1 — PROFESSIONAL ACTIVITY EXECUTION MATRIX
   ========================================================= */
.q1-matrix-shell {
    position: relative;
    overflow: hidden;
    margin: .04rem 0 .48rem 0;
    background:
        radial-gradient(circle at 92% 8%, rgba(37,99,235,.055), transparent 23%),
        linear-gradient(180deg, rgba(255,255,255,.99) 0%, rgba(249,251,254,.98) 100%);
    border: 1px solid #DCE5EF;
    border-radius: 15px;
    box-shadow:
        0 10px 28px rgba(15,42,69,.055),
        inset 0 1px 0 rgba(255,255,255,.95);
}

.q1-matrix-shell::before {
    content: "";
    position: absolute;
    z-index: 6;
    top: 0;
    left: -30%;
    width: 25%;
    height: 2px;
    background: linear-gradient(
        90deg,
        rgba(37,99,235,0),
        rgba(37,99,235,.95),
        rgba(20,184,166,.80),
        rgba(124,58,237,.72),
        rgba(37,99,235,0)
    );
    animation: q1MatrixSweep 6.8s ease-in-out infinite;
}

@keyframes q1MatrixSweep {
    0%, 15%  { left: -30%; opacity: 0; }
    27%      { opacity: 1; }
    58%      { left: 108%; opacity: .95; }
    68%,100% { left: 108%; opacity: 0; }
}

.q1-matrix-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    padding: .66rem .78rem .50rem .78rem;
    border-bottom: 1px solid #E4EBF3;
    background:
        linear-gradient(100deg, rgba(244,248,253,.90), rgba(255,255,255,.98));
}

.q1-matrix-title {
    color: #102A43;
    font-size: .94rem;
    font-weight: 900;
    line-height: 1.15;
}

.q1-matrix-sub {
    color: #7A8DA3;
    font-size: .60rem;
    line-height: 1.35;
    margin-top: .13rem;
}

.q1-matrix-badge {
    flex: 0 0 auto;
    display: inline-flex;
    align-items: center;
    gap: .28rem;
    padding: .22rem .44rem;
    border-radius: 999px;
    color: #345D88;
    background: linear-gradient(135deg,#EDF5FF,#F6F2FF);
    border: 1px solid #DCE6F2;
    box-shadow: 0 3px 9px rgba(15,42,69,.035);
    font-size: .52rem;
    font-weight: 900;
    white-space: nowrap;
}

.q1-matrix-badge::before {
    content: "";
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #2F80ED;
    box-shadow: 0 0 0 3px rgba(47,128,237,.10);
}

.q1-matrix-scroll {
    width: 100%;
    overflow-x: auto;
    overflow-y: hidden;
    scrollbar-width: thin;
    scrollbar-color: #C7D4E2 #F5F8FB;
}

.q1-exec-table {
    width: 100%;
    min-width: 1230px;
    table-layout: fixed;
    border-collapse: separate;
    border-spacing: 0;
    font-family: Arial, sans-serif;
    color: #405872;
}

.q1-exec-table thead tr:first-child th {
    padding: .37rem .36rem;
    color: #244563;
    background: linear-gradient(180deg,#EAF3FC 0%,#E5EFF9 100%);
    border-bottom: 1px solid #D6E2EE;
    border-right: 1px solid #DDE6EF;
    font-size: .57rem;
    font-weight: 900;
    letter-spacing: .055em;
    text-transform: uppercase;
    text-align: center;
}

.q1-exec-table thead tr:nth-child(2) th {
    padding: .37rem .35rem;
    color: #4A627B;
    background: #F7FAFD;
    border-bottom: 1px solid #DEE7F0;
    border-right: 1px solid #E5EBF2;
    font-size: .56rem;
    font-weight: 850;
    text-align: center;
}

.q1-exec-table th:last-child,
.q1-exec-table td:last-child {
    border-right: none;
}

.q1-exec-table tbody td {
    padding: .31rem .35rem;
    border-bottom: 1px solid #E8EEF5;
    border-right: 1px solid #EDF1F6;
    background: rgba(255,255,255,.98);
    font-size: .55rem;
    line-height: 1.20;
    vertical-align: middle;
}

.q1-exec-table tbody tr {
    transition:
        background .18s ease,
        box-shadow .18s ease,
        transform .18s ease;
}

.q1-exec-table tbody tr:hover td {
    background: #F8FBFF;
}

.q1-exec-table tbody tr:hover {
    box-shadow: inset 3px 0 0 #4B7BEC;
}

.q1-campus-cell {
    vertical-align: top !important;
    padding-top: .43rem !important;
    background:
        linear-gradient(180deg,#F3F7FC 0%,#F8FAFD 100%) !important;
}

.q1-campus-pill {
    display: inline-flex;
    align-items: center;
    gap: .28rem;
    padding: .18rem .35rem;
    border-radius: 999px;
    background: #FFFFFF;
    border: 1px solid #DCE6F0;
    box-shadow: 0 3px 8px rgba(16,42,67,.035);
    color: #294A69;
    font-size: .55rem;
    font-weight: 900;
    white-space: nowrap;
}

.q1-campus-pill::before {
    content: "";
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: linear-gradient(135deg,#2563EB,#14B8A6);
    box-shadow: 0 0 0 3px rgba(37,99,235,.07);
}

.q1-activity-cell {
    color: #29455F;
    font-weight: 780;
}

.q1-activity-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    margin-right: .34rem;
    border-radius: 2px;
    vertical-align: 0;
    box-shadow: 0 0 0 2px rgba(15,42,69,.03);
}

.q1-event-chip {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    max-width: 130px;
    padding: .15rem .31rem;
    border-radius: 7px;
    border: 1px solid #DEE7F0;
    background: #F2F6FA;
    color: #5B7087;
    font-size: .54rem;
    line-height: 1.10;
    text-align: center;
}

.q1-event-chip.blank {
    color: #98A6B5;
    background: #FAFBFC;
    border-style: dashed;
}

.q1-status-box {
    position: relative;
    overflow: hidden;
    min-height: 22px;
    border-radius: 6px;
    background: #F8FAFC;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #52677E;
    font-weight: 900;
    font-variant-numeric: tabular-nums;
}

.q1-status-box .fill {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    border-radius: 6px;
    opacity: .19;
}

.q1-status-box .num {
    position: relative;
    z-index: 2;
}

.q1-status-box.cancelled .fill { background: #D65A63; }
.q1-status-box.completed .fill { background: #2F9B6B; }
.q1-status-box.confirmed .fill { background: #2F6FBC; }
.q1-status-box.planned   .fill { background: #8FC2E8; }
.q1-status-box.rescheduled .fill { background: #D99A32; }
.q1-status-box.blank .fill { background: #94A3B8; }

.q1-total-meter {
    position: relative;
    overflow: hidden;
    min-height: 22px;
    border-radius: 6px;
    background: #FFF9EC;
    border: 1px solid #F2DFB7;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 0 .31rem;
    color: #795719;
    font-weight: 900;
    font-variant-numeric: tabular-nums;
}

.q1-total-meter .fill {
    position: absolute;
    inset: 0 auto 0 0;
    background: linear-gradient(90deg,#F9CE65,#E9A72C);
    opacity: .33;
}

.q1-total-meter .num {
    position: relative;
    z-index: 2;
}

.q1-row-insight {
    color: #60758C;
    font-size: .53rem !important;
    line-height: 1.30 !important;
}

.q1-row-insight strong {
    color: #294A69;
    font-weight: 900;
}

.q1-exec-table tfoot td {
    padding: .39rem .35rem;
    color: #5A4921;
    background: linear-gradient(180deg,#FFF9E8 0%,#FFF4D7 100%);
    border-top: 1px solid #EAD5A5;
    border-right: 1px solid #EFDFB9;
    font-size: .56rem;
    font-weight: 900;
    text-align: center;
}

.q1-exec-table tfoot td:first-child {
    text-align: left;
}

.q1-matrix-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: .8rem;
    padding: .37rem .72rem .40rem .72rem;
    color: #7A8DA3;
    background: #FAFCFE;
    border-top: 1px solid #E5ECF3;
    font-size: .52rem;
}

.q1-matrix-footer strong {
    color: #36526E;
    font-weight: 900;
}

.q1-chart-lower {
    margin-top: .56rem;
}

@media (prefers-reduced-motion: reduce) {
    .q1-matrix-shell::before {
        animation: none !important;
    }
}

/* ---------- Q1 top visual + executive insight ---------- */
.q1-top-marker {
    display: none;
}

.q1-visual-title {
    color: #102A43;
    font-size: .91rem;
    font-weight: 900;
    margin-bottom: .04rem;
}

.q1-visual-sub {
    color: #7B8DA3;
    font-size: .59rem;
    line-height: 1.34;
    margin-bottom: .20rem;
}

.q1-exec-insight {
    position: relative;
    overflow: hidden;
    min-height: 300px;
    box-sizing: border-box;
    border-radius: 14px;
    padding: .72rem .72rem .66rem .72rem;
    background:
        radial-gradient(circle at 88% 9%, rgba(37,99,235,.10), transparent 25%),
        radial-gradient(circle at 12% 88%, rgba(20,184,166,.07), transparent 30%),
        linear-gradient(145deg,#F9FBFF 0%,#FFFFFF 58%,#F8FBFD 100%);
    border: 1px solid #DCE6F1;
    box-shadow:
        0 9px 24px rgba(15,42,69,.055),
        inset 0 1px 0 rgba(255,255,255,.95);
    animation: q1InsightFloat 4.8s ease-in-out infinite;
    transition:
        transform .22s ease,
        box-shadow .22s ease;
}

.q1-exec-insight:hover {
    transform: translateY(-3px);
    box-shadow:
        0 15px 32px rgba(15,42,69,.09),
        inset 0 1px 0 rgba(255,255,255,.95);
}

.q1-exec-insight::after {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: -42%;
    width: 28%;
    background: linear-gradient(
        105deg,
        rgba(255,255,255,0),
        rgba(255,255,255,.18),
        rgba(255,255,255,.78),
        rgba(255,255,255,.18),
        rgba(255,255,255,0)
    );
    transform: skewX(-18deg);
    animation: q1InsightSheen 6.4s ease-in-out infinite;
    pointer-events: none;
}

@keyframes q1InsightFloat {
    0%,100% { transform: translateY(0); }
    50%     { transform: translateY(-2px); }
}

@keyframes q1InsightSheen {
    0%,18%  { left: -42%; opacity: 0; }
    28%     { opacity: .85; }
    50%     { left: 112%; opacity: 0; }
    100%    { left: 112%; opacity: 0; }
}

.q1-insight-kicker {
    position: relative;
    z-index: 2;
    color: #2B6DE8;
    font-size: .53rem;
    font-weight: 950;
    letter-spacing: .10em;
    text-transform: uppercase;
}

.q1-insight-title {
    position: relative;
    z-index: 2;
    color: #102A43;
    font-size: .94rem;
    font-weight: 900;
    margin-top: .10rem;
    margin-bottom: .10rem;
}

.q1-insight-sub {
    position: relative;
    z-index: 2;
    color: #7B8DA3;
    font-size: .55rem;
    line-height: 1.35;
    margin-bottom: .48rem;
}

.q1-insight-grid {
    position: relative;
    z-index: 2;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 7px;
}

.q1-insight-metric {
    min-height: 64px;
    border-radius: 10px;
    padding: .43rem .48rem;
    border: 1px solid #E0E8F1;
    background: rgba(255,255,255,.82);
    box-shadow: 0 3px 10px rgba(15,42,69,.025);
}

.q1-insight-metric .label {
    color: #7A8EA4;
    font-size: .48rem;
    font-weight: 900;
    letter-spacing: .04em;
    text-transform: uppercase;
}

.q1-insight-metric .value {
    color: #153A5F;
    font-size: .82rem;
    font-weight: 950;
    line-height: 1.12;
    margin-top: .11rem;
}

.q1-insight-metric .note {
    color: #8394A8;
    font-size: .48rem;
    line-height: 1.22;
    margin-top: .08rem;
}

.q1-insight-action {
    position: relative;
    z-index: 2;
    margin-top: 8px;
    padding: .46rem .51rem;
    border-radius: 10px;
    background: linear-gradient(90deg,#EEF5FF 0%,#F7FAFF 100%);
    border: 1px solid #DCE8F8;
    border-left: 4px solid #2B6DE8;
    color: #536B84;
    font-size: .53rem;
    line-height: 1.35;
}

.q1-insight-action strong {
    color: #1D4F83;
    font-weight: 950;
}

.q1-table-heading {
    margin-top: .46rem;
    margin-bottom: .20rem;
}

.q1-table-heading .title {
    color: #102A43;
    font-size: .90rem;
    font-weight: 900;
}

.q1-table-heading .sub {
    color: #7B8DA3;
    font-size: .58rem;
    margin-top: .10rem;
    line-height: 1.32;
}

@media (prefers-reduced-motion: reduce) {
    .q1-exec-insight,
    .q1-exec-insight::after {
        animation: none !important;
    }
}


/* =========================================================
   Q1 — EXECUTIVE VISUAL ROW REFINEMENT
   ========================================================= */

/* Remove any extra dead-space before the Q1 visual row */
.q1-executive-row-spacer {
    height: 2px;
    margin: 0;
    padding: 0;
}

/* Left chart card — premium executive container */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-chart-marker) {
    min-height: 352px !important;
    height: 352px !important;
    overflow: hidden !important;
    padding: .72rem .82rem .48rem .82rem !important;
    background:
        radial-gradient(circle at 94% 8%, rgba(37,99,235,.045), transparent 25%),
        linear-gradient(180deg,#FFFFFF 0%,#FBFCFE 100%) !important;
    border: 1px solid #DCE5EF !important;
    border-radius: 15px !important;
    box-shadow:
        0 10px 26px rgba(15,42,69,.055),
        inset 0 1px 0 rgba(255,255,255,.96) !important;
    position: relative !important;
}

/* Subtle moving top accent for chart card */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-chart-marker)::before {
    content: "";
    position: absolute;
    top: 0;
    left: -28%;
    width: 24%;
    height: 2px;
    z-index: 5;
    background: linear-gradient(
        90deg,
        rgba(37,99,235,0),
        rgba(37,99,235,.95),
        rgba(20,184,166,.72),
        rgba(124,58,237,.55),
        rgba(37,99,235,0)
    );
    animation: q1ChartSweep 6.6s ease-in-out infinite;
}

@keyframes q1ChartSweep {
    0%,16%  { left:-28%; opacity:0; }
    28%     { opacity:1; }
    56%     { left:110%; opacity:.95; }
    68%,100%{ left:110%; opacity:0; }
}

.q1-chart-marker {
    display:none;
}

.q1-chart-heading {
    margin: 0 0 .16rem 0;
    padding: 0;
}

.q1-chart-heading .title {
    color:#102A43;
    font-size:.96rem;
    font-weight:900;
    line-height:1.14;
    letter-spacing:-.01em;
}

.q1-chart-heading .sub {
    color:#7B8DA3;
    font-size:.58rem;
    line-height:1.35;
    margin-top:.12rem;
    max-width:92%;
}

.q1-chart-separator {
    height:1px;
    margin:.34rem 0 .10rem 0;
    background:linear-gradient(
        90deg,
        #D9E4F0 0%,
        #ECF1F6 68%,
        rgba(236,241,246,0) 100%
    );
}

/* Keep Plotly safely below the heading block */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-chart-marker)
div[data-testid="stPlotlyChart"] {
    margin-top: .08rem !important;
}

/* Right insight card — exact same height/alignment as chart */
.q1-exec-insight {
    min-height:352px !important;
    height:352px !important;
    padding:.72rem .72rem .62rem .72rem !important;
    border-radius:15px !important;
    box-sizing:border-box !important;
    display:flex;
    flex-direction:column;
    justify-content:flex-start;
    background:
        radial-gradient(circle at 88% 7%, rgba(37,99,235,.105), transparent 24%),
        radial-gradient(circle at 10% 91%, rgba(20,184,166,.075), transparent 30%),
        linear-gradient(145deg,#F9FBFF 0%,#FFFFFF 57%,#F8FBFD 100%) !important;
    border:1px solid #DCE6F1 !important;
    box-shadow:
        0 10px 26px rgba(15,42,69,.055),
        inset 0 1px 0 rgba(255,255,255,.96) !important;
}

.q1-insight-kicker {
    font-size:.51rem !important;
    letter-spacing:.105em !important;
}

.q1-insight-title {
    font-size:.93rem !important;
    margin-top:.08rem !important;
    margin-bottom:.08rem !important;
}

.q1-insight-sub {
    font-size:.54rem !important;
    margin-bottom:.40rem !important;
}

.q1-insight-grid {
    gap:6px !important;
}

.q1-insight-metric {
    min-height:60px !important;
    padding:.39rem .43rem !important;
    background:
        linear-gradient(145deg,rgba(255,255,255,.94),rgba(248,251,255,.90)) !important;
    transition:
        transform .18s ease,
        box-shadow .18s ease,
        border-color .18s ease;
}

.q1-insight-metric:hover {
    transform:translateY(-2px);
    border-color:#CCDDF1;
    box-shadow:0 7px 16px rgba(15,42,69,.06);
}

.q1-insight-metric .value {
    font-size:.79rem !important;
}

.q1-insight-metric .note {
    font-size:.46rem !important;
}

.q1-insight-action {
    margin-top:auto !important;
    padding:.43rem .48rem !important;
    font-size:.51rem !important;
    line-height:1.34 !important;
    background:
        linear-gradient(90deg,#EEF5FF 0%,#F8FBFF 100%) !important;
}

/* Keep the full left/right row aligned from the same top edge */
div[data-testid="stHorizontalBlock"]:has(.q1-chart-marker) {
    align-items:stretch !important;
}

/* Professional table spacing after the visual row */
.q1-table-heading {
    margin-top:.58rem !important;
}

@media (prefers-reduced-motion: reduce) {
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-chart-marker)::before {
        animation:none !important;
    }
}


/* =========================================================
   JAIPURIA-INSPIRED PREMIUM THEME
   Warm ivory canvas + deep navy + restrained orange/violet
   ========================================================= */

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 92% 2%, rgba(103,60,128,.055), transparent 27%),
        radial-gradient(circle at 8% 90%, rgba(230,139,43,.050), transparent 26%),
        linear-gradient(180deg, #FBFAF7 0%, #F6F3EE 100%) !important;
}

.block-container,
[data-testid="stAppViewContainer"] {
    font-family: "Aptos", "Segoe UI", Arial, sans-serif !important;
}

.overview-eyebrow,
.overview-section-kicker {
    color: #6B3F7D !important;
}

.overview-title,
.overview-section-title,
.filter-panel-title,
.chart-title,
.table-title,
.q1-table-heading .title {
    color: #17395A !important;
}

.overview-subtitle,
.overview-section-sub,
.chart-subtitle,
.table-subtitle,
.filter-note,
.q1-table-heading .sub {
    color: #728297 !important;
}

/* Jaipuria-style orange accent instead of a generic blue rule */
.overview-accent {
    background: linear-gradient(
        90deg,
        #E58C2B 0%,
        #F0B356 22%,
        #70417D 50%,
        rgba(112,65,125,.16) 75%,
        rgba(112,65,125,0) 100%
    ) !important;
}

div[data-baseweb="select"] > div,
div[data-testid="stDateInput"] input {
    background: rgba(255,255,255,.94) !important;
    border-color: #E4DDD4 !important;
    color: #17395A !important;
    box-shadow: 0 3px 10px rgba(65,45,35,.028) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background:
        linear-gradient(180deg, rgba(255,255,255,.985) 0%, rgba(253,252,249,.98) 100%) !important;
    border-color: #E5DED6 !important;
    box-shadow: 0 9px 26px rgba(42,45,55,.045) !important;
}

.pro-kpi {
    background:
        linear-gradient(118deg, rgba(255,255,255,.99) 0%, rgba(255,255,255,.965) 64%, var(--wash) 170%) !important;
    border-color: #E7E0D8 !important;
    box-shadow:
        0 8px 22px rgba(50,42,38,.045),
        inset 0 1px 0 rgba(255,255,255,.95) !important;
}

.pro-kpi .label {
    color: #6D7888 !important;
}

.pro-kpi .value {
    color: #17395A !important;
}

.pro-kpi .sub {
    color: #8793A1 !important;
}

/* =========================================================
   Q1 — ACTIVITY TYPE × CAMPUS BUBBLE MATRIX
   ========================================================= */

.q1-brand-chart-marker {
    display: none;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker) {
    position: relative !important;
    min-height: 382px !important;
    height: 382px !important;
    overflow: hidden !important;
    padding: .74rem .86rem .52rem .86rem !important;
    background:
        radial-gradient(circle at 94% 6%, rgba(112,65,125,.060), transparent 25%),
        linear-gradient(180deg,#FFFFFF 0%,#FCFAF7 100%) !important;
    border: 1px solid #E4DDD4 !important;
    border-radius: 16px !important;
    box-shadow:
        0 12px 30px rgba(46,42,38,.060),
        inset 0 1px 0 rgba(255,255,255,.96) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)::before {
    content: "";
    position: absolute;
    top: 0;
    left: -28%;
    width: 25%;
    height: 3px;
    z-index: 5;
    background: linear-gradient(
        90deg,
        rgba(229,140,43,0),
        rgba(229,140,43,.96),
        rgba(112,65,125,.88),
        rgba(229,140,43,0)
    );
    animation: jaipuriaChartSweep 6.8s ease-in-out infinite;
}

@keyframes jaipuriaChartSweep {
    0%,16%  { left:-28%; opacity:0; }
    28%     { opacity:1; }
    56%     { left:110%; opacity:.95; }
    68%,100%{ left:110%; opacity:0; }
}

.q1-brand-heading {
    margin: 0;
    padding: 0;
}

.q1-brand-heading .eyebrow {
    color: #E08727;
    font-size: .50rem;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: .12em;
    margin-bottom: .10rem;
}

.q1-brand-heading .title {
    color: #17395A;
    font-size: .98rem;
    font-weight: 950;
    letter-spacing: -.012em;
    line-height: 1.12;
}

.q1-brand-heading .sub {
    color: #748397;
    font-size: .58rem;
    line-height: 1.36;
    margin-top: .12rem;
    max-width: 92%;
}

.q1-brand-rule {
    height: 1px;
    margin: .36rem 0 .08rem 0;
    background: linear-gradient(
        90deg,
        #E8D7C3 0%,
        #E8E0D8 58%,
        rgba(232,224,216,0) 100%
    );
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)
div[data-testid="stPlotlyChart"] {
    margin-top: .03rem !important;
}

/* =========================================================
   Q1 — BRAND MANAGEMENT INTELLIGENCE PANEL
   ========================================================= */

.q1-brand-insight {
    position: relative;
    overflow: hidden;
    height: 382px;
    box-sizing: border-box;
    border-radius: 16px;
    background:
        linear-gradient(180deg, #17395A 0%, #17395A 31%, #FFFFFF 31%, #FCFAF7 100%);
    border: 1px solid #DCD5CE;
    box-shadow:
        0 12px 30px rgba(44,39,37,.072),
        inset 0 1px 0 rgba(255,255,255,.08);
    animation: brandInsightFloat 5.0s ease-in-out infinite;
    transition:
        transform .22s ease,
        box-shadow .22s ease;
}

.q1-brand-insight:hover {
    transform: translateY(-3px);
    box-shadow:
        0 17px 36px rgba(44,39,37,.105),
        inset 0 1px 0 rgba(255,255,255,.08);
}

.q1-brand-insight::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 5px;
    height: 31%;
    background: linear-gradient(180deg,#F0A13A,#E17E20);
}

.q1-brand-insight::after {
    content: "";
    position: absolute;
    top: -35%;
    left: -45%;
    width: 35%;
    height: 165%;
    transform: rotate(18deg);
    background: linear-gradient(
        90deg,
        rgba(255,255,255,0),
        rgba(255,255,255,.15),
        rgba(255,255,255,0)
    );
    animation: brandInsightSheen 7s ease-in-out infinite;
    pointer-events: none;
}

@keyframes brandInsightFloat {
    0%,100% { transform: translateY(0); }
    50%     { transform: translateY(-2px); }
}

@keyframes brandInsightSheen {
    0%,18%  { left:-45%; opacity:0; }
    31%     { opacity:.75; }
    55%     { left:118%; opacity:0; }
    100%    { left:118%; opacity:0; }
}

.q1-brand-head {
    position: relative;
    z-index: 2;
    padding: .68rem .76rem .58rem .82rem;
}

.q1-brand-kicker {
    color: #F3AF52;
    font-size: .50rem;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: .12em;
}

.q1-brand-title {
    color: #FFFFFF;
    font-size: .98rem;
    font-weight: 950;
    margin-top: .08rem;
    letter-spacing: -.012em;
}

.q1-brand-sub {
    color: rgba(255,255,255,.70);
    font-size: .53rem;
    line-height: 1.34;
    margin-top: .10rem;
}

.q1-brand-body {
    position: relative;
    z-index: 2;
    padding: .56rem .66rem .64rem .66rem;
}

.q1-brand-hero {
    display: grid;
    grid-template-columns: 1.06fr .94fr;
    gap: 7px;
}

.q1-brand-hero-card {
    border-radius: 11px;
    padding: .45rem .50rem;
    border: 1px solid #E4DED7;
    background: linear-gradient(145deg,#FFFFFF,#FBF8F3);
    box-shadow: 0 4px 12px rgba(53,45,40,.035);
}

.q1-brand-hero-card .label {
    color: #7D8794;
    font-size: .46rem;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: .055em;
}

.q1-brand-hero-card .value {
    color: #17395A;
    font-size: .82rem;
    font-weight: 950;
    line-height: 1.14;
    margin-top: .10rem;
}

.q1-brand-hero-card .note {
    color: #8A949F;
    font-size: .46rem;
    line-height: 1.22;
    margin-top: .07rem;
}

.q1-brand-signal {
    margin-top: 8px;
    padding: .44rem .48rem;
    border-radius: 11px;
    background: #FFF7EC;
    border: 1px solid #F0DEC5;
}

.q1-brand-signal-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: .5rem;
}

.q1-brand-signal .label {
    color: #7D6950;
    font-size: .47rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: .045em;
}

.q1-brand-signal .value {
    color: #17395A;
    font-size: .64rem;
    font-weight: 950;
}

.q1-brand-progress {
    height: 5px;
    margin-top: .30rem;
    border-radius: 999px;
    overflow: hidden;
    background: #EDE6DD;
}

.q1-brand-progress span {
    display: block;
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg,#E58C2B,#F2B24E,#70417D);
}

.q1-brand-facts {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 7px;
    margin-top: 8px;
}

.q1-brand-fact {
    padding: .39rem .43rem;
    border-radius: 10px;
    background: #FFFFFF;
    border: 1px solid #E6E0D9;
}

.q1-brand-fact .label {
    color: #89939F;
    font-size: .44rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: .045em;
}

.q1-brand-fact .value {
    color: #6B3F7D;
    font-size: .68rem;
    font-weight: 950;
    margin-top: .08rem;
}

.q1-brand-action {
    margin-top: 8px;
    padding: .46rem .49rem;
    border-radius: 10px;
    background: linear-gradient(90deg,#F8F2EA,#FFF9F1);
    border: 1px solid #EBDCCB;
    border-left: 4px solid #E58C2B;
    color: #5C6877;
    font-size: .50rem;
    line-height: 1.34;
}

.q1-brand-action strong {
    color: #17395A;
    font-weight: 950;
}

div[data-testid="stHorizontalBlock"]:has(.q1-brand-chart-marker) {
    align-items: stretch !important;
}

@media (prefers-reduced-motion: reduce) {
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)::before,
    .q1-brand-insight,
    .q1-brand-insight::after {
        animation: none !important;
    }
}


/* =========================================================
   PREMIUM DYNAMIC FILTER BAR
   ========================================================= */

.filter-motion-marker {
    display: none;
}

div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker) {
    position: relative;
    overflow: visible;
    align-items: end !important;
    padding: .42rem .48rem .46rem .48rem !important;
    border: 1px solid #E5DDD4;
    border-radius: 15px;
    background:
        radial-gradient(circle at 92% 10%, rgba(112,65,125,.050), transparent 22%),
        radial-gradient(circle at 4% 90%, rgba(229,140,43,.045), transparent 20%),
        linear-gradient(145deg, rgba(255,255,255,.94), rgba(251,248,244,.96));
    box-shadow:
        0 10px 26px rgba(51,44,40,.045),
        inset 0 1px 0 rgba(255,255,255,.94);
}

/* Animated brand accent on the filter panel */
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)::before {
    content: "";
    position: absolute;
    top: 0;
    left: -24%;
    width: 22%;
    height: 2px;
    border-radius: 999px;
    background: linear-gradient(
        90deg,
        rgba(229,140,43,0),
        rgba(229,140,43,.98),
        rgba(112,65,125,.88),
        rgba(229,140,43,0)
    );
    animation: filterBrandSweep 7.2s ease-in-out infinite;
    pointer-events: none;
    z-index: 5;
}

@keyframes filterBrandSweep {
    0%,18%  { left:-24%; opacity:0; }
    30%     { opacity:1; }
    58%     { left:106%; opacity:.95; }
    70%,100%{ left:106%; opacity:0; }
}

/* Filter labels */
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stSelectbox"] label,
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stDateInput"] label {
    color: #53677B !important;
    font-size: .62rem !important;
    font-weight: 850 !important;
    letter-spacing: .018em !important;
    margin-bottom: .12rem !important;
}

/* Individual filter tabs */
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-baseweb="select"] > div,
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stDateInput"] input {
    min-height: 2.34rem !important;
    height: 2.34rem !important;
    border-radius: 10px !important;
    border: 1px solid #E4DDD4 !important;
    background:
        linear-gradient(145deg, #FFFFFF 0%, #FBF8F3 100%) !important;
    color: #17395A !important;
    box-shadow:
        0 4px 11px rgba(55,46,42,.035),
        inset 0 1px 0 rgba(255,255,255,.95) !important;
    transition:
        transform .18s ease,
        box-shadow .18s ease,
        border-color .18s ease,
        background .18s ease !important;
}

/* Hover lift for each tab */
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-baseweb="select"] > div:hover,
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stDateInput"] input:hover {
    transform: translateY(-2px);
    border-color: #D9C6B3 !important;
    background:
        linear-gradient(145deg, #FFFFFF 0%, #FFF9F1 100%) !important;
    box-shadow:
        0 9px 19px rgba(70,51,42,.070),
        0 0 0 1px rgba(229,140,43,.05) inset !important;
}

/* Active / focused control */
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-baseweb="select"] > div:focus-within,
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stDateInput"] input:focus {
    border-color: #B68A62 !important;
    box-shadow:
        0 10px 22px rgba(84,57,45,.085),
        0 0 0 2px rgba(229,140,43,.12) !important;
}

/* Brand-colored dropdown arrow area */
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
svg {
    color: #6B3F7D !important;
}

/* Reset button gets a premium branded gradient */
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stButton"] button {
    min-height: 2.34rem !important;
    height: 2.34rem !important;
    border-radius: 10px !important;
    border: 1px solid #D8C5B2 !important;
    color: #FFFFFF !important;
    background:
        linear-gradient(115deg,#17395A 0%,#254F74 42%,#6B3F7D 72%,#E58C2B 120%) !important;
    background-size: 180% 100% !important;
    box-shadow:
        0 8px 18px rgba(23,57,90,.18),
        inset 0 1px 0 rgba(255,255,255,.14) !important;
    animation: resetBrandFlow 6s ease-in-out infinite !important;
    transition:
        transform .18s ease,
        box-shadow .18s ease !important;
}

@keyframes resetBrandFlow {
    0%,100% { background-position: 0% 50%; }
    50%     { background-position: 100% 50%; }
}

div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stButton"] button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow:
        0 12px 24px rgba(23,57,90,.24),
        0 0 0 1px rgba(255,255,255,.12) inset !important;
}


/* =========================================================
   EXECUTIVE KPI TILES — MORE DYNAMIC, STILL PROFESSIONAL
   ========================================================= */

.pro-kpi {
    isolation: isolate;
}

.pro-kpi::after {
    transition: transform .35s ease, opacity .35s ease !important;
}

.pro-kpi:hover::after {
    transform: scale(1.18) translate(-3px, -2px);
    opacity: .92 !important;
}

/* very soft sheen across KPI tiles */
.pro-kpi .icon::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: linear-gradient(
        115deg,
        rgba(255,255,255,0),
        rgba(255,255,255,.50),
        rgba(255,255,255,0)
    );
    transform: translateX(-125%);
    animation: kpiIconSheen 7.5s ease-in-out infinite;
    pointer-events: none;
}

@keyframes kpiIconSheen {
    0%,24% { transform: translateX(-125%); opacity:0; }
    36%    { opacity:.8; }
    56%    { transform: translateX(125%); opacity:0; }
    100%   { transform: translateX(125%); opacity:0; }
}


/* =========================================================
   MANAGEMENT SIGNAL — PREMIUM DYNAMIC MICRO-CARDS
   ========================================================= */

.q1-brand-hero-card,
.q1-brand-fact,
.q1-brand-signal,
.q1-brand-action {
    position: relative;
    overflow: hidden;
    transition:
        transform .20s ease,
        box-shadow .20s ease,
        border-color .20s ease,
        background .20s ease;
}

/* distinct top accents */
.q1-brand-hero-card::before,
.q1-brand-fact::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 36%;
    height: 2px;
    border-radius: 999px;
    opacity: .92;
}

.q1-brand-hero-card:nth-child(1)::before {
    background: linear-gradient(90deg,#E58C2B,#F2B24E,rgba(242,178,78,0));
}

.q1-brand-hero-card:nth-child(2)::before {
    background: linear-gradient(90deg,#6B3F7D,#9C72AE,rgba(156,114,174,0));
}

.q1-brand-fact:nth-child(1)::before {
    background: linear-gradient(90deg,#159786,#64CDBA,rgba(100,205,186,0));
}

.q1-brand-fact:nth-child(2)::before {
    background: linear-gradient(90deg,#2D6CDF,#79A7F8,rgba(121,167,248,0));
}

.q1-brand-hero-card:hover,
.q1-brand-fact:hover {
    transform: translateY(-3px);
    border-color: #D7CBBF;
    box-shadow:
        0 11px 22px rgba(54,45,40,.080),
        inset 0 1px 0 rgba(255,255,255,.95);
}

/* staggered soft float */
.q1-brand-hero-card:nth-child(1) {
    animation: microCardFloatA 5.4s ease-in-out infinite;
}
.q1-brand-hero-card:nth-child(2) {
    animation: microCardFloatB 5.8s ease-in-out infinite;
}
.q1-brand-fact:nth-child(1) {
    animation: microCardFloatB 6.0s ease-in-out infinite;
}
.q1-brand-fact:nth-child(2) {
    animation: microCardFloatA 6.2s ease-in-out infinite;
}

@keyframes microCardFloatA {
    0%,100% { transform: translateY(0); }
    50%     { transform: translateY(-1.5px); }
}
@keyframes microCardFloatB {
    0%,100% { transform: translateY(-1px); }
    50%     { transform: translateY(1px); }
}

/* signal panel: subtle light movement */
.q1-brand-signal {
    background:
        radial-gradient(circle at 90% 15%, rgba(112,65,125,.06), transparent 28%),
        linear-gradient(100deg,#FFF5E8 0%,#FFF9F1 58%,#FBF6FA 100%) !important;
}

.q1-brand-signal::after {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: -34%;
    width: 24%;
    transform: skewX(-18deg);
    background: linear-gradient(
        105deg,
        rgba(255,255,255,0),
        rgba(255,255,255,.70),
        rgba(255,255,255,0)
    );
    animation: signalSheen 6.8s ease-in-out infinite;
    pointer-events: none;
}

@keyframes signalSheen {
    0%,22% { left:-34%; opacity:0; }
    34%    { opacity:.75; }
    56%    { left:112%; opacity:0; }
    100%   { left:112%; opacity:0; }
}

/* animated progress line */
.q1-brand-progress span {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(90deg,#E58C2B 0%,#F2B24E 48%,#6B3F7D 100%) !important;
    background-size: 180% 100% !important;
    animation: progressBrandFlow 4.8s ease-in-out infinite;
}

@keyframes progressBrandFlow {
    0%,100% { background-position: 0% 50%; }
    50%     { background-position: 100% 50%; }
}

/* action card looks more like a decision module */
.q1-brand-action {
    background:
        radial-gradient(circle at 98% 12%, rgba(112,65,125,.055), transparent 30%),
        linear-gradient(90deg,#FFF7EC 0%,#FFFDFC 100%) !important;
    border-left: 4px solid #E58C2B !important;
}

.q1-brand-action:hover {
    transform: translateY(-2px);
    box-shadow: 0 9px 18px rgba(59,48,42,.065);
    border-color: #DFC8AF;
}


/* =========================================================
   REDUCED MOTION ACCESSIBILITY
   ========================================================= */

@media (prefers-reduced-motion: reduce) {
    div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)::before,
    div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
    div[data-testid="stButton"] button,
    .pro-kpi .icon::after,
    .q1-brand-hero-card,
    .q1-brand-fact,
    .q1-brand-signal::after,
    .q1-brand-progress span {
        animation: none !important;
    }
}


/* =========================================================
   FILTERS — PREMIUM JAIPURIA CONTROL DECK
   ========================================================= */

/* no secondary sentence below Filters */
.filter-note {
    display: none !important;
}

div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker) {
    position: relative;
    overflow: hidden;
    padding: .50rem .56rem .50rem .56rem !important;
    border: 1px solid rgba(218,205,192,.95) !important;
    border-radius: 17px !important;
    background:
        radial-gradient(circle at 8% 15%, rgba(229,140,43,.070), transparent 24%),
        radial-gradient(circle at 91% 86%, rgba(107,63,125,.060), transparent 26%),
        linear-gradient(125deg,#FFFDFC 0%,#FAF7F2 45%,#FCF9F6 100%) !important;
    background-size: 125% 125% !important;
    box-shadow:
        0 14px 34px rgba(49,42,38,.070),
        0 1px 0 rgba(255,255,255,.95) inset !important;
    animation: filterDeckBreath 8.5s ease-in-out infinite;
    align-items: end !important;
}

@keyframes filterDeckBreath {
    0%,100% {
        background-position: 0% 50%;
        box-shadow:
            0 14px 34px rgba(49,42,38,.060),
            0 1px 0 rgba(255,255,255,.95) inset;
    }
    50% {
        background-position: 100% 50%;
        box-shadow:
            0 17px 40px rgba(72,51,44,.090),
            0 1px 0 rgba(255,255,255,.95) inset;
    }
}

/* orange-violet moving brand line */
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)::before {
    content: "";
    position: absolute;
    z-index: 6;
    top: 0;
    left: -26%;
    width: 25%;
    height: 3px;
    border-radius: 999px;
    background: linear-gradient(
        90deg,
        rgba(229,140,43,0),
        #E58C2B,
        #F1B45C,
        #6B3F7D,
        rgba(107,63,125,0)
    );
    animation: filterDeckSweep 6.8s ease-in-out infinite;
}

@keyframes filterDeckSweep {
    0%,16%  { left:-26%; opacity:0; }
    28%     { opacity:1; }
    57%     { left:108%; opacity:.95; }
    70%,100%{ left:108%; opacity:0; }
}

/* soft moving ambient highlight */
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)::after {
    content: "";
    position: absolute;
    pointer-events: none;
    width: 170px;
    height: 170px;
    right: -60px;
    top: -105px;
    border-radius: 50%;
    background: radial-gradient(
        circle,
        rgba(229,140,43,.10) 0%,
        rgba(107,63,125,.055) 42%,
        rgba(255,255,255,0) 72%
    );
    animation: filterOrbFloat 8s ease-in-out infinite;
}

@keyframes filterOrbFloat {
    0%,100% { transform: translate(0,0) scale(1); }
    50%     { transform: translate(-24px,15px) scale(1.08); }
}

/* labels */
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stSelectbox"] label,
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stDateInput"] label {
    color:#425B74 !important;
    font-size:.62rem !important;
    font-weight:900 !important;
    letter-spacing:.025em !important;
    margin:0 0 .13rem .05rem !important;
}

/* filter control tiles */
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-baseweb="select"] > div,
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stDateInput"] input {
    position: relative !important;
    min-height:2.40rem !important;
    height:2.40rem !important;
    border-radius:11px !important;
    border:1px solid #E4D9CF !important;
    color:#17395A !important;
    background:
        linear-gradient(145deg,#FFFFFF 0%,#FBF7F1 100%) !important;
    box-shadow:
        0 5px 13px rgba(58,47,42,.042),
        0 1px 0 rgba(255,255,255,.98) inset !important;
    transition:
        transform .20s ease,
        box-shadow .20s ease,
        border-color .20s ease,
        background .20s ease !important;
}

/* motion on every filter tile */
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stSelectbox"],
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stDateInput"] {
    animation: filterTileFloat 6.4s ease-in-out infinite;
}

@keyframes filterTileFloat {
    0%,100% { transform: translateY(0); }
    50%     { transform: translateY(-1px); }
}

div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-baseweb="select"] > div:hover,
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stDateInput"] input:hover {
    transform:translateY(-3px) !important;
    border-color:#D5B99E !important;
    background:
        linear-gradient(145deg,#FFFFFF 0%,#FFF7ED 100%) !important;
    box-shadow:
        0 11px 24px rgba(74,53,45,.100),
        0 0 0 1px rgba(229,140,43,.070) inset !important;
}

div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-baseweb="select"] > div:focus-within,
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stDateInput"] input:focus {
    border-color:#A87343 !important;
    box-shadow:
        0 12px 26px rgba(78,55,44,.100),
        0 0 0 2px rgba(229,140,43,.13) !important;
}

/* value text and caret */
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-baseweb="select"] span {
    color:#17395A !important;
    font-weight:700 !important;
}

div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker) svg {
    color:#6B3F7D !important;
}

/* reset */
div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stButton"] button {
    min-height:2.40rem !important;
    height:2.40rem !important;
    border-radius:11px !important;
    border:1px solid rgba(39,63,89,.25) !important;
    color:#FFFFFF !important;
    background:
        linear-gradient(115deg,#17395A 0%,#254E74 38%,#6B3F7D 72%,#E58C2B 120%) !important;
    background-size:190% 100% !important;
    box-shadow:
        0 9px 20px rgba(23,57,90,.20),
        0 1px 0 rgba(255,255,255,.14) inset !important;
    animation: resetFlow 5.5s ease-in-out infinite !important;
}

@keyframes resetFlow {
    0%,100% { background-position:0% 50%; }
    50%     { background-position:100% 50%; }
}

div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
div[data-testid="stButton"] button:hover {
    transform:translateY(-3px) scale(1.015) !important;
    box-shadow:0 14px 28px rgba(23,57,90,.27) !important;
}


/* =========================================================
   EXECUTIVE SNAPSHOT — PREMIUM HEADER + KPI RAIL
   ========================================================= */

.snapshot-banner {
    position: relative;
    overflow: hidden;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:1rem;
    margin:.26rem 0 .32rem 0;
    padding:.54rem .68rem .50rem .74rem;
    border-radius:14px;
    border:1px solid #E6DED5;
    background:
        radial-gradient(circle at 91% 15%, rgba(107,63,125,.060), transparent 28%),
        linear-gradient(110deg,#FFFDFC 0%,#F9F5EF 55%,#FCF9F6 100%);
    box-shadow:
        0 9px 24px rgba(52,45,40,.045),
        inset 0 1px 0 rgba(255,255,255,.95);
}

.snapshot-banner::before {
    content:"";
    position:absolute;
    left:0;
    top:0;
    bottom:0;
    width:4px;
    background:linear-gradient(180deg,#E58C2B,#F1B45C,#6B3F7D);
}

.snapshot-banner::after {
    content:"";
    position:absolute;
    left:-34%;
    top:0;
    bottom:0;
    width:22%;
    transform:skewX(-17deg);
    background:linear-gradient(
        105deg,
        rgba(255,255,255,0),
        rgba(255,255,255,.72),
        rgba(255,255,255,0)
    );
    animation:snapshotSheen 7.5s ease-in-out infinite;
}

@keyframes snapshotSheen {
    0%,20% { left:-34%; opacity:0; }
    32%    { opacity:.80; }
    54%    { left:110%; opacity:0; }
    100%   { left:110%; opacity:0; }
}

.snapshot-copy,
.snapshot-badges {
    position:relative;
    z-index:2;
}

.snapshot-eyebrow {
    color:#E08727;
    font-size:.49rem;
    font-weight:950;
    letter-spacing:.12em;
    text-transform:uppercase;
}

.snapshot-title {
    color:#17395A;
    font-size:1.02rem;
    font-weight:950;
    letter-spacing:-.015em;
    margin-top:.07rem;
}

.snapshot-sub {
    color:#7A8998;
    font-size:.57rem;
    margin-top:.08rem;
}

.snapshot-badges {
    display:flex;
    gap:6px;
    flex-wrap:wrap;
    justify-content:flex-end;
}

.snapshot-badge {
    padding:.20rem .36rem;
    border-radius:999px;
    font-size:.45rem;
    font-weight:950;
    letter-spacing:.05em;
    border:1px solid;
    box-shadow:0 3px 9px rgba(55,45,40,.035);
}

.snapshot-badge.navy {
    color:#17395A;
    background:#EEF4F9;
    border-color:#D9E4ED;
}
.snapshot-badge.orange {
    color:#9B601D;
    background:#FFF4E6;
    border-color:#F1D9BB;
}
.snapshot-badge.violet {
    color:#6B3F7D;
    background:#F6F0F8;
    border-color:#E5D8EA;
}

/* KPI rail container */
.snapshot-motion-marker {
    display:none;
}

div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) {
    position:relative;
    overflow:hidden;
    padding:.40rem .42rem .44rem .42rem !important;
    border-radius:16px;
    border:1px solid #E5DDD4;
    background:
        radial-gradient(circle at 6% 15%, rgba(229,140,43,.048), transparent 25%),
        radial-gradient(circle at 94% 90%, rgba(107,63,125,.045), transparent 25%),
        linear-gradient(135deg,#FFFEFC 0%,#FAF7F2 100%);
    box-shadow:
        0 12px 30px rgba(53,45,40,.055),
        inset 0 1px 0 rgba(255,255,255,.96);
}

div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker)::before {
    content:"";
    position:absolute;
    left:-28%;
    top:0;
    width:24%;
    height:2px;
    background:linear-gradient(
        90deg,
        rgba(229,140,43,0),
        #E58C2B,
        #F0B04F,
        #6B3F7D,
        rgba(107,63,125,0)
    );
    animation:snapshotRailSweep 6.8s ease-in-out infinite;
}

@keyframes snapshotRailSweep {
    0%,17%  { left:-28%; opacity:0; }
    29%     { opacity:1; }
    58%     { left:110%; opacity:.95; }
    70%,100%{ left:110%; opacity:0; }
}

/* KPI tiles feel more like a premium instrument panel */
div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi {
    min-height:72px !important;
    height:72px !important;
    background:
        linear-gradient(145deg,rgba(255,255,255,.98) 0%,rgba(255,255,255,.94) 58%,var(--wash) 150%) !important;
    border-color:#E5DED7 !important;
    box-shadow:
        0 6px 16px rgba(51,43,39,.045),
        inset 0 1px 0 rgba(255,255,255,.96) !important;
    animation:kpiPremiumFloat 6s ease-in-out infinite !important;
}

@keyframes kpiPremiumFloat {
    0%,100% { transform:translateY(0); }
    50%     { transform:translateY(-1.5px); }
}

div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi:hover {
    transform:translateY(-4px) scale(1.008) !important;
    border-color:#D7C8B9 !important;
    box-shadow:
        0 14px 28px rgba(58,45,38,.105),
        0 0 0 1px rgba(229,140,43,.055) inset !important;
}


/* =========================================================
   Q1 CHART — SHADOW + MOTION
   ========================================================= */

div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker) {
    transition:
        transform .25s ease,
        box-shadow .25s ease,
        border-color .25s ease !important;
    animation:q1CardBreath 6.4s ease-in-out infinite;
}

@keyframes q1CardBreath {
    0%,100% {
        box-shadow:
            0 12px 30px rgba(46,42,38,.060),
            inset 0 1px 0 rgba(255,255,255,.96);
    }
    50% {
        box-shadow:
            0 18px 38px rgba(65,48,41,.095),
            inset 0 1px 0 rgba(255,255,255,.96);
    }
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker):hover {
    transform:translateY(-3px);
    border-color:#D7C8B9 !important;
    box-shadow:
        0 20px 42px rgba(58,43,38,.120),
        inset 0 1px 0 rgba(255,255,255,.96) !important;
}

/* actual plotting surface gets a soft floating shadow */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)
div[data-testid="stPlotlyChart"] {
    position:relative;
    overflow:hidden;
    border-radius:13px;
    background:#FCFAF7;
    box-shadow:
        0 10px 22px rgba(64,48,40,.070),
        0 0 0 1px rgba(229,219,209,.85);
    transition:
        transform .24s ease,
        box-shadow .24s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)
div[data-testid="stPlotlyChart"]:hover {
    transform:translateY(-2px);
    box-shadow:
        0 16px 30px rgba(65,48,40,.105),
        0 0 0 1px rgba(216,198,181,.95);
}

/* ultra-subtle light sweep over chart surface */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)
div[data-testid="stPlotlyChart"]::after {
    content:"";
    position:absolute;
    pointer-events:none;
    top:0;
    bottom:0;
    left:-34%;
    width:22%;
    transform:skewX(-18deg);
    background:linear-gradient(
        105deg,
        rgba(255,255,255,0),
        rgba(255,255,255,.30),
        rgba(255,255,255,0)
    );
    animation:q1PlotSheen 8s ease-in-out infinite;
}

@keyframes q1PlotSheen {
    0%,22% { left:-34%; opacity:0; }
    34%    { opacity:.55; }
    54%    { left:112%; opacity:0; }
    100%   { left:112%; opacity:0; }
}

@media (prefers-reduced-motion: reduce) {
    div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker),
    div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)::before,
    div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)::after,
    div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
    div[data-testid="stSelectbox"],
    div[data-testid="stHorizontalBlock"]:has(.filter-motion-marker)
    div[data-testid="stDateInput"],
    .snapshot-banner::after,
    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker)::before,
    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker),
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)
    div[data-testid="stPlotlyChart"]::after {
        animation:none !important;
    }
}


/* =========================================================
   Q1 BUBBLE CHART — DEPTH + MOTION
   ========================================================= */

/* Stronger premium shadow around the complete chart card */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker) {
    box-shadow:
        0 18px 42px rgba(40,35,32,.105),
        0 4px 12px rgba(112,65,125,.055),
        inset 0 1px 0 rgba(255,255,255,.98) !important;
}

/* Soft raised plotting surface */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)
div[data-testid="stPlotlyChart"] {
    border-radius: 14px !important;
    background:
        linear-gradient(180deg,#FFFDFC 0%,#FBF8F4 100%) !important;
    box-shadow:
        0 14px 28px rgba(52,43,38,.085),
        0 3px 8px rgba(229,140,43,.045),
        0 0 0 1px rgba(224,214,203,.88) !important;
    transition:
        transform .24s ease,
        box-shadow .24s ease !important;
}

/* On hover, the plotting surface lifts very slightly */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)
div[data-testid="stPlotlyChart"]:hover {
    transform: translateY(-2px) !important;
    box-shadow:
        0 20px 38px rgba(52,43,38,.125),
        0 5px 12px rgba(107,63,125,.060),
        0 0 0 1px rgba(211,194,177,.96) !important;
}

/* Bubble points get a subtle floating/pulse animation + shadow */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)
.scatterlayer .point {
    transform-box: fill-box;
    transform-origin: center;
    filter:
        drop-shadow(0 5px 6px rgba(23,57,90,.20))
        drop-shadow(0 1px 2px rgba(229,140,43,.10));
    animation: q1BubblePulse 3.8s ease-in-out infinite;
    transition:
        filter .20s ease,
        opacity .20s ease;
}

/* Stagger bubble motion so all circles do not move together */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)
.scatterlayer .trace:nth-child(2n) .point {
    animation-delay: .45s;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)
.scatterlayer .trace:nth-child(3n) .point {
    animation-delay: .85s;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)
.scatterlayer .trace:nth-child(4n) .point {
    animation-delay: 1.20s;
}

@keyframes q1BubblePulse {
    0%,100% {
        transform: translateY(0) scale(1);
        filter:
            drop-shadow(0 5px 6px rgba(23,57,90,.18))
            drop-shadow(0 1px 2px rgba(229,140,43,.08));
    }
    50% {
        transform: translateY(-2px) scale(1.055);
        filter:
            drop-shadow(0 8px 10px rgba(23,57,90,.26))
            drop-shadow(0 2px 4px rgba(229,140,43,.14));
    }
}

/* Bubble hover = stronger depth without becoming flashy */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)
.scatterlayer .point:hover {
    filter:
        drop-shadow(0 10px 14px rgba(23,57,90,.32))
        drop-shadow(0 3px 6px rgba(229,140,43,.20));
}

/* Very subtle ambient chart glow */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)::after {
    content: "";
    position: absolute;
    pointer-events: none;
    width: 170px;
    height: 170px;
    right: -65px;
    bottom: -85px;
    border-radius: 50%;
    background: radial-gradient(
        circle,
        rgba(229,140,43,.085) 0%,
        rgba(107,63,125,.045) 46%,
        rgba(255,255,255,0) 72%
    );
    animation: q1AmbientGlow 7.5s ease-in-out infinite;
}

@keyframes q1AmbientGlow {
    0%,100% { transform: scale(1) translate(0,0); opacity:.72; }
    50%     { transform: scale(1.12) translate(-12px,-8px); opacity:1; }
}

@media (prefers-reduced-motion: reduce) {
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)
    .scatterlayer .point,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)::after {
        animation: none !important;
    }
}


/* =========================================================
   Q1 — REAL HTML/CSS BUBBLE MATRIX
   These bubbles are native HTML elements, so shadow + motion
   work reliably in Streamlit (unlike CSS targeting Plotly SVG).
   ========================================================= */

.q1-css-matrix {
    position: relative;
    overflow: hidden;
    margin-top: .18rem;
    padding: .40rem .46rem .44rem .46rem;
    border-radius: 14px;
    border: 1px solid #E2D8CE;
    background:
        radial-gradient(circle at 94% 6%, rgba(107,63,125,.050), transparent 24%),
        radial-gradient(circle at 5% 94%, rgba(229,140,43,.045), transparent 22%),
        linear-gradient(180deg,#FFFDFC 0%,#FAF7F2 100%);
    box-shadow:
        0 18px 34px rgba(52,43,38,.115),
        0 5px 12px rgba(107,63,125,.045),
        inset 0 1px 0 rgba(255,255,255,.96);
    transition:
        transform .24s ease,
        box-shadow .24s ease;
    animation: q1MatrixCardBreath 6.5s ease-in-out infinite;
}

.q1-css-matrix:hover {
    transform: translateY(-2px);
    box-shadow:
        0 24px 44px rgba(52,43,38,.145),
        0 7px 16px rgba(107,63,125,.060),
        inset 0 1px 0 rgba(255,255,255,.98);
}

@keyframes q1MatrixCardBreath {
    0%,100% {
        box-shadow:
            0 18px 34px rgba(52,43,38,.105),
            0 5px 12px rgba(107,63,125,.040),
            inset 0 1px 0 rgba(255,255,255,.96);
    }
    50% {
        box-shadow:
            0 23px 42px rgba(52,43,38,.145),
            0 8px 17px rgba(229,140,43,.055),
            inset 0 1px 0 rgba(255,255,255,.98);
    }
}

/* moving premium sheen on the visual surface */
.q1-css-matrix::before {
    content: "";
    position: absolute;
    z-index: 3;
    top: 0;
    bottom: 0;
    left: -32%;
    width: 20%;
    pointer-events: none;
    transform: skewX(-18deg);
    background: linear-gradient(
        105deg,
        rgba(255,255,255,0),
        rgba(255,255,255,.48),
        rgba(255,255,255,0)
    );
    animation: q1CssMatrixSheen 8s ease-in-out infinite;
}

@keyframes q1CssMatrixSheen {
    0%,22% { left:-32%; opacity:0; }
    33%    { opacity:.70; }
    56%    { left:110%; opacity:0; }
    100%   { left:110%; opacity:0; }
}

.q1-css-grid {
    position: relative;
    z-index: 2;
    display: grid;
    gap: 0;
    width: 100%;
    min-width: 690px;
}

.q1-css-corner,
.q1-css-campus,
.q1-css-activity,
.q1-css-cell {
    min-height: 38px;
    box-sizing: border-box;
    border-right: 1px solid #E8E0D8;
    border-bottom: 1px solid #E8E0D8;
}

.q1-css-campus {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #17395A;
    font-size: .61rem;
    font-weight: 900;
    background:
        linear-gradient(180deg,#FCFAF7 0%,#F8F3ED 100%);
    border-top: 1px solid #E2D8CE;
}

.q1-css-campus:last-child {
    border-right: none;
}

.q1-css-corner {
    border-top: 1px solid #E2D8CE;
    background:
        linear-gradient(180deg,#FCFAF7 0%,#F8F3ED 100%);
}

.q1-css-activity {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: .48rem;
    color: #3F566D;
    font-size: .57rem;
    font-weight: 760;
    background: rgba(255,255,255,.55);
    border-left: 1px solid #E2D8CE;
    white-space: nowrap;
}

.q1-css-cell {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        linear-gradient(180deg,rgba(255,255,255,.72),rgba(252,249,245,.68));
    transition: background .20s ease;
}

.q1-css-cell:hover {
    background:
        radial-gradient(circle at 50% 50%, rgba(229,140,43,.060), transparent 65%),
        linear-gradient(180deg,#FFFDFC,#F9F5F0);
}

/* The actual bubble: visible shadow + real motion */
.q1-motion-bubble {
    position: relative;
    z-index: 4;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-weight: 950;
    font-size: .58rem;
    line-height: 1;
    border: 1.5px solid rgba(255,255,255,.92);
    box-shadow:
        0 10px 15px rgba(23,57,90,.23),
        0 4px 7px rgba(47,35,31,.15),
        inset 0 3px 4px rgba(255,255,255,.58),
        inset 0 -3px 6px rgba(23,57,90,.10);
    animation:
        q1BubbleFloat var(--bubble-duration, 4.2s) ease-in-out infinite,
        q1BubbleGlow 5.8s ease-in-out infinite;
    animation-delay:
        var(--bubble-delay, 0s),
        calc(var(--bubble-delay, 0s) + .35s);
    transition:
        transform .20s ease,
        box-shadow .20s ease,
        filter .20s ease;
    cursor: default;
    will-change: transform, box-shadow;
}

.q1-motion-bubble::before {
    content: "";
    position: absolute;
    width: 32%;
    height: 23%;
    left: 18%;
    top: 13%;
    border-radius: 50%;
    transform: rotate(-28deg);
    background: rgba(255,255,255,.50);
    filter: blur(.2px);
    pointer-events: none;
}

.q1-motion-bubble::after {
    content: "";
    position: absolute;
    left: 18%;
    right: 18%;
    bottom: -8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(23,57,90,.16);
    filter: blur(5px);
    transform: scaleX(.82);
    opacity: .75;
    animation: q1BubbleGroundShadow var(--bubble-duration, 4.2s) ease-in-out infinite;
    animation-delay: var(--bubble-delay, 0s);
    pointer-events: none;
}

@keyframes q1BubbleFloat {
    0%,100% {
        transform: translateY(0) scale(1);
    }
    50% {
        transform: translateY(-5px) scale(1.075);
    }
}

@keyframes q1BubbleGroundShadow {
    0%,100% {
        transform: scaleX(.82);
        opacity: .70;
    }
    50% {
        transform: scaleX(.66);
        opacity: .42;
    }
}

@keyframes q1BubbleGlow {
    0%,100% {
        filter: saturate(1) brightness(1);
        box-shadow:
            0 10px 15px rgba(23,57,90,.23),
            0 4px 7px rgba(47,35,31,.15),
            inset 0 3px 4px rgba(255,255,255,.58),
            inset 0 -3px 6px rgba(23,57,90,.10);
    }
    50% {
        filter: saturate(1.08) brightness(1.03);
        box-shadow:
            0 15px 23px rgba(23,57,90,.30),
            0 6px 10px rgba(229,140,43,.15),
            inset 0 3px 5px rgba(255,255,255,.70),
            inset 0 -4px 7px rgba(23,57,90,.11);
    }
}

.q1-motion-bubble:hover {
    animation-play-state: paused;
    transform: translateY(-7px) scale(1.13);
    box-shadow:
        0 19px 29px rgba(23,57,90,.34),
        0 7px 12px rgba(229,140,43,.18),
        inset 0 3px 5px rgba(255,255,255,.72),
        inset 0 -4px 7px rgba(23,57,90,.12);
}

.q1-bubble-count {
    position: relative;
    z-index: 3;
    text-shadow: 0 1px 0 rgba(255,255,255,.38);
}

.q1-css-matrix-foot {
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: .7rem;
    margin-top: .30rem;
    color: #8692A0;
    font-size: .48rem;
}

.q1-css-matrix-foot strong {
    color: #17395A;
    font-weight: 900;
}

@media (prefers-reduced-motion: reduce) {
    .q1-css-matrix,
    .q1-css-matrix::before,
    .q1-motion-bubble,
    .q1-motion-bubble::after {
        animation: none !important;
    }
}


/* =========================================================
   Q1 — EXACT CHART / INSIGHT HEIGHT ALIGNMENT
   ========================================================= */

:root {
    --q1-equal-panel-height: 575px;
}

/* Make both Streamlit columns stretch to the same vertical size */
div[data-testid="stHorizontalBlock"]:has(.q1-brand-chart-marker) {
    align-items: stretch !important;
}

/* Left chart card */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker) {
    height: var(--q1-equal-panel-height) !important;
    min-height: var(--q1-equal-panel-height) !important;
    max-height: var(--q1-equal-panel-height) !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
}

/* Left card inner Streamlit block */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)
> div[data-testid="stVerticalBlock"] {
    height: 100% !important;
    min-height: 100% !important;
    box-sizing: border-box !important;
}

/* Matrix consumes remaining space cleanly */
.q1-css-matrix {
    height: 465px !important;
    min-height: 465px !important;
    max-height: 465px !important;
    box-sizing: border-box !important;
    display: flex !important;
    flex-direction: column !important;
}

.q1-css-grid {
    flex: 1 1 auto !important;
    height: auto !important;
}

/* Keep rows visually balanced */
.q1-css-corner,
.q1-css-campus,
.q1-css-activity,
.q1-css-cell {
    min-height: 48px !important;
}

/* Right insight card: exact same outer height */
.q1-brand-insight {
    height: var(--q1-equal-panel-height) !important;
    min-height: var(--q1-equal-panel-height) !important;
    max-height: var(--q1-equal-panel-height) !important;
    box-sizing: border-box !important;
    display: flex !important;
    flex-direction: column !important;
}

/* Let the white management body use all remaining space */
.q1-brand-body {
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
    box-sizing: border-box !important;
}

.q1-brand-action {
    margin-top: auto !important;
}

/* =========================================================
   Q1 — CLEAN BUBBLES: NO WHITE GLOSS PATCH
   ========================================================= */

/* Remove the white glossy highlight blob */
.q1-motion-bubble::before {
    display: none !important;
}

/* Cleaner premium depth without white glare */
.q1-motion-bubble {
    border: 1px solid rgba(255,255,255,.55) !important;
    box-shadow:
        0 10px 16px rgba(23,57,90,.24),
        0 4px 8px rgba(47,35,31,.14),
        inset 0 1px 2px rgba(255,255,255,.20),
        inset 0 -3px 6px rgba(23,57,90,.10) !important;
}

/* Bubble hover remains dimensional but not glossy */
.q1-motion-bubble:hover {
    box-shadow:
        0 19px 29px rgba(23,57,90,.34),
        0 7px 12px rgba(229,140,43,.16),
        inset 0 1px 2px rgba(255,255,255,.22),
        inset 0 -4px 7px rgba(23,57,90,.12) !important;
}

@media (max-width: 1200px) {
    :root {
        --q1-equal-panel-height: 555px;
    }
}


/* =========================================================
   Q1 — COMPACT EQUAL-HEIGHT LAYOUT
   Smaller chart + perfectly matched left/right panel height
   ========================================================= */

:root {
    --q1-compact-panel-height: 500px;
}

/* Keep both columns stretched equally */
div[data-testid="stHorizontalBlock"]:has(.q1-brand-chart-marker) {
    align-items: stretch !important;
}

/* LEFT PANEL — compact chart card */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker) {
    height: var(--q1-compact-panel-height) !important;
    min-height: var(--q1-compact-panel-height) !important;
    max-height: var(--q1-compact-panel-height) !important;
    padding: .62rem .72rem .42rem .72rem !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.q1-brand-chart-marker)
> div[data-testid="stVerticalBlock"] {
    height: 100% !important;
    min-height: 100% !important;
    gap: .24rem !important;
}

/* Slightly tighter heading */
.q1-brand-heading .title {
    font-size: .93rem !important;
}

.q1-brand-heading .sub {
    font-size: .54rem !important;
    line-height: 1.28 !important;
    margin-top: .08rem !important;
}

.q1-brand-rule {
    margin: .28rem 0 .06rem 0 !important;
}

/* Matrix becomes smaller but remains readable */
.q1-css-matrix {
    height: 392px !important;
    min-height: 392px !important;
    max-height: 392px !important;
    margin-top: .08rem !important;
    padding: .26rem .34rem .30rem .34rem !important;
    box-sizing: border-box !important;
}

.q1-css-grid {
    flex: 1 1 auto !important;
    height: auto !important;
}

/* Compact row heights */
.q1-css-corner,
.q1-css-campus,
.q1-css-activity,
.q1-css-cell {
    min-height: 40px !important;
}

.q1-css-campus {
    font-size: .57rem !important;
}

.q1-css-activity {
    font-size: .54rem !important;
    padding-right: .40rem !important;
}

.q1-css-matrix-foot {
    margin-top: .20rem !important;
    font-size: .44rem !important;
}

/* RIGHT PANEL — exactly same height as left */
.q1-brand-insight {
    height: var(--q1-compact-panel-height) !important;
    min-height: var(--q1-compact-panel-height) !important;
    max-height: var(--q1-compact-panel-height) !important;
    box-sizing: border-box !important;
}

/* Compact the right panel so content fits naturally */
.q1-brand-head {
    padding: .58rem .66rem .48rem .72rem !important;
}

.q1-brand-title {
    font-size: .91rem !important;
}

.q1-brand-sub {
    font-size: .50rem !important;
    line-height: 1.28 !important;
}

.q1-brand-body {
    padding: .46rem .54rem .54rem .54rem !important;
    gap: 0 !important;
}

.q1-brand-hero-card {
    padding: .38rem .42rem !important;
}

.q1-brand-hero-card .value {
    font-size: .76rem !important;
}

.q1-brand-hero-card .note {
    font-size: .43rem !important;
}

.q1-brand-signal {
    margin-top: 6px !important;
    padding: .38rem .42rem !important;
}

.q1-brand-facts {
    margin-top: 6px !important;
    gap: 6px !important;
}

.q1-brand-fact {
    padding: .34rem .38rem !important;
}

.q1-brand-fact .value {
    font-size: .62rem !important;
}

.q1-brand-action {
    margin-top: auto !important;
    padding: .40rem .43rem !important;
    font-size: .47rem !important;
    line-height: 1.28 !important;
}

/* Ensure the right card visually touches the same bottom line */
div[data-testid="stHorizontalBlock"]:has(.q1-brand-chart-marker)
> div[data-testid="stColumn"] {
    display: flex !important;
    flex-direction: column !important;
}

div[data-testid="stHorizontalBlock"]:has(.q1-brand-chart-marker)
> div[data-testid="stColumn"] > div {
    flex: 1 1 auto !important;
}

/* Responsive fallback */
@media (max-width: 1200px) {
    :root {
        --q1-compact-panel-height: 485px;
    }

    .q1-css-matrix {
        height: 378px !important;
        min-height: 378px !important;
        max-height: 378px !important;
    }

    .q1-css-corner,
    .q1-css-campus,
    .q1-css-activity,
    .q1-css-cell {
        min-height: 38px !important;
    }
}


/* =========================================================
   Q1 RIGHT PANEL — CAMPUS EVENT + STATUS INTELLIGENCE
   ========================================================= */

.q1-event-status-panel {
    position: relative;
    overflow: hidden;
    height: var(--q1-compact-panel-height, 500px);
    min-height: var(--q1-compact-panel-height, 500px);
    max-height: var(--q1-compact-panel-height, 500px);
    box-sizing: border-box;
    border-radius: 16px;
    border: 1px solid #DCD5CE;
    background:
        radial-gradient(circle at 90% 8%, rgba(107,63,125,.07), transparent 24%),
        linear-gradient(180deg,#17395A 0%,#17395A 24%,#FFFFFF 24%,#FCFAF7 100%);
    box-shadow:
        0 15px 34px rgba(44,39,37,.085),
        inset 0 1px 0 rgba(255,255,255,.08);
    display: flex;
    flex-direction: column;
    animation: q1EventPanelFloat 5.6s ease-in-out infinite;
    transition:
        transform .22s ease,
        box-shadow .22s ease;
}

.q1-event-status-panel:hover {
    transform: translateY(-3px);
    box-shadow:
        0 20px 42px rgba(44,39,37,.12),
        inset 0 1px 0 rgba(255,255,255,.08);
}

.q1-event-status-panel::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 5px;
    height: 24%;
    background: linear-gradient(180deg,#F0A13A,#E17E20);
}

.q1-event-status-panel::after {
    content: "";
    position: absolute;
    top: -30%;
    left: -44%;
    width: 32%;
    height: 150%;
    transform: rotate(17deg);
    background: linear-gradient(
        90deg,
        rgba(255,255,255,0),
        rgba(255,255,255,.13),
        rgba(255,255,255,0)
    );
    animation: q1EventPanelSheen 7.2s ease-in-out infinite;
    pointer-events: none;
}

@keyframes q1EventPanelFloat {
    0%,100% { transform: translateY(0); }
    50%     { transform: translateY(-2px); }
}

@keyframes q1EventPanelSheen {
    0%,18%  { left:-44%; opacity:0; }
    31%     { opacity:.72; }
    56%     { left:118%; opacity:0; }
    100%    { left:118%; opacity:0; }
}

.q1-event-head {
    position: relative;
    z-index: 2;
    padding: .60rem .72rem .50rem .78rem;
}

.q1-event-kicker {
    color: #F2AD4C;
    font-size: .49rem;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: .11em;
}

.q1-event-title {
    color: #FFFFFF;
    font-size: .92rem;
    font-weight: 950;
    margin-top: .08rem;
    line-height: 1.15;
}

.q1-event-sub {
    color: rgba(255,255,255,.70);
    font-size: .49rem;
    line-height: 1.28;
    margin-top: .09rem;
}

.q1-event-body {
    position: relative;
    z-index: 2;
    flex: 1 1 auto;
    min-height: 0;
    display: flex;
    flex-direction: column;
    padding: .48rem .56rem .54rem .56rem;
}

.q1-mini-section {
    border-radius: 12px;
    border: 1px solid #E4DED7;
    background:
        linear-gradient(145deg,#FFFFFF 0%,#FBF8F4 100%);
    padding: .42rem .48rem .44rem .48rem;
    box-shadow:
        0 5px 13px rgba(55,46,42,.035),
        inset 0 1px 0 rgba(255,255,255,.95);
}

.q1-mini-section + .q1-mini-section {
    margin-top: 7px;
}

.q1-mini-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: .4rem;
    margin-bottom: .34rem;
}

.q1-mini-heading .title {
    color: #17395A;
    font-size: .56rem;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: .045em;
}

.q1-mini-heading .meta {
    color: #8A7460;
    font-size: .47rem;
    font-weight: 850;
}

.q1-event-row {
    display: grid;
    grid-template-columns: 55px 1fr 28px;
    gap: 6px;
    align-items: center;
    min-height: 26px;
    margin-bottom: 4px;
}

.q1-event-row:last-child {
    margin-bottom: 0;
}

.q1-event-campus {
    color: #425C76;
    font-size: .49rem;
    font-weight: 850;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.q1-event-bar-track {
    position: relative;
    overflow: hidden;
    height: 8px;
    border-radius: 999px;
    background: #EEE8E1;
    box-shadow: inset 0 1px 2px rgba(46,37,33,.07);
}

.q1-event-bar-fill {
    height: 100%;
    border-radius: 999px;
    background:
        linear-gradient(90deg,#E58C2B 0%,#F1B45C 52%,#6B3F7D 100%);
    background-size: 180% 100%;
    animation: q1EventBarFlow 5s ease-in-out infinite;
    box-shadow: 0 0 8px rgba(229,140,43,.16);
}

@keyframes q1EventBarFlow {
    0%,100% { background-position: 0% 50%; }
    50%     { background-position: 100% 50%; }
}

.q1-event-count {
    color: #17395A;
    font-size: .52rem;
    font-weight: 950;
    text-align: right;
}

.q1-status-row {
    display: grid;
    grid-template-columns: 55px 1fr;
    gap: 6px;
    align-items: center;
    min-height: 28px;
    margin-bottom: 4px;
}

.q1-status-row:last-child {
    margin-bottom: 0;
}

.q1-status-stack {
    display: flex;
    width: 100%;
    height: 12px;
    overflow: hidden;
    border-radius: 999px;
    background: #EEE8E1;
    box-shadow: inset 0 1px 2px rgba(46,37,33,.07);
}

.q1-status-seg {
    height: 100%;
    min-width: 0;
    transition:
        filter .18s ease,
        transform .18s ease;
    animation: q1StatusPulse 5.8s ease-in-out infinite;
}

.q1-status-seg:hover {
    filter: brightness(1.08) saturate(1.08);
}

@keyframes q1StatusPulse {
    0%,100% { filter: brightness(1); }
    50%     { filter: brightness(1.035); }
}

.q1-status-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 5px 8px;
    margin-top: .34rem;
}

.q1-status-key {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    color: #718094;
    font-size: .43rem;
    font-weight: 750;
}

.q1-status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    box-shadow: 0 0 0 2px rgba(255,255,255,.85);
}

.q1-event-footer {
    margin-top: auto;
    padding: .39rem .44rem;
    border-radius: 10px;
    background:
        radial-gradient(circle at 95% 10%, rgba(107,63,125,.05), transparent 28%),
        linear-gradient(90deg,#FFF7EC 0%,#FFFDFC 100%);
    border: 1px solid #EADBC9;
    border-left: 4px solid #E58C2B;
    color: #5B6A7A;
    font-size: .47rem;
    line-height: 1.30;
}

.q1-event-footer strong {
    color: #17395A;
    font-weight: 950;
}

.q1-event-empty {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 80px;
    border-radius: 10px;
    border: 1px dashed #DDCFC0;
    background: #FFFDFC;
    color: #8B98A5;
    font-size: .49rem;
    text-align: center;
    padding: .5rem;
}

@media (prefers-reduced-motion: reduce) {
    .q1-event-status-panel,
    .q1-event-status-panel::after,
    .q1-event-bar-fill,
    .q1-status-seg {
        animation: none !important;
    }
}


/* =========================================================
   FULL-WIDTH MANAGEMENT SIGNAL SUMMARY
   Sits below Activity + Event charts
   ========================================================= */

.q1-management-summary {
    position: relative;
    overflow: hidden;
    margin: .52rem 0 .42rem 0;
    border-radius: 16px;
    border: 1px solid #DDD4CB;
    background:
        radial-gradient(circle at 92% 12%, rgba(107,63,125,.060), transparent 24%),
        radial-gradient(circle at 7% 88%, rgba(229,140,43,.055), transparent 24%),
        linear-gradient(120deg,#FFFDFC 0%,#F9F5EF 56%,#FCF9F6 100%);
    box-shadow:
        0 14px 34px rgba(48,41,37,.070),
        inset 0 1px 0 rgba(255,255,255,.96);
    animation: q1SummaryBreath 6.4s ease-in-out infinite;
    transition:
        transform .22s ease,
        box-shadow .22s ease;
}

.q1-management-summary:hover {
    transform: translateY(-2px);
    box-shadow:
        0 19px 42px rgba(48,41,37,.105),
        inset 0 1px 0 rgba(255,255,255,.98);
}

.q1-management-summary::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 5px;
    height: 100%;
    background: linear-gradient(180deg,#E58C2B 0%,#F1B45C 45%,#6B3F7D 100%);
}

.q1-management-summary::after {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: -34%;
    width: 22%;
    transform: skewX(-18deg);
    background: linear-gradient(
        105deg,
        rgba(255,255,255,0),
        rgba(255,255,255,.70),
        rgba(255,255,255,0)
    );
    animation: q1SummarySheen 7.4s ease-in-out infinite;
    pointer-events: none;
}

@keyframes q1SummaryBreath {
    0%,100% {
        box-shadow:
            0 14px 34px rgba(48,41,37,.060),
            inset 0 1px 0 rgba(255,255,255,.96);
    }
    50% {
        box-shadow:
            0 18px 40px rgba(65,48,41,.095),
            inset 0 1px 0 rgba(255,255,255,.98);
    }
}

@keyframes q1SummarySheen {
    0%,20% { left:-34%; opacity:0; }
    32%    { opacity:.72; }
    56%    { left:110%; opacity:0; }
    100%   { left:110%; opacity:0; }
}

.q1-summary-head {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
    padding: .58rem .72rem .44rem .80rem;
    border-bottom: 1px solid #E7DED5;
}

.q1-summary-kicker {
    color: #E08727;
    font-size: .48rem;
    font-weight: 950;
    letter-spacing: .11em;
    text-transform: uppercase;
}

.q1-summary-title {
    color: #17395A;
    font-size: .95rem;
    font-weight: 950;
    letter-spacing: -.012em;
    margin-top: .07rem;
}

.q1-summary-sub {
    color: #7C8998;
    font-size: .53rem;
    line-height: 1.30;
    margin-top: .09rem;
}

.q1-summary-status {
    flex: 0 0 auto;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: .22rem .40rem;
    border-radius: 999px;
    color: #17395A;
    background: #F2F6F9;
    border: 1px solid #D9E4EB;
    font-size: .44rem;
    font-weight: 950;
    letter-spacing: .045em;
    white-space: nowrap;
}

.q1-summary-status::before {
    content: "";
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #E58C2B;
    box-shadow: 0 0 0 3px rgba(229,140,43,.10);
    animation: q1SummaryDot 1.7s ease-in-out infinite;
}

@keyframes q1SummaryDot {
    0%,100% { transform: scale(1); opacity:.85; }
    50%     { transform: scale(1.30); opacity:1; }
}

.q1-summary-grid {
    position: relative;
    z-index: 2;
    display: grid;
    grid-template-columns: repeat(4, minmax(0,1fr));
    gap: 8px;
    padding: .52rem .70rem .48rem .80rem;
}

.q1-summary-card {
    position: relative;
    overflow: hidden;
    min-height: 78px;
    padding: .44rem .48rem;
    border-radius: 11px;
    border: 1px solid #E4DED7;
    background:
        linear-gradient(145deg,rgba(255,255,255,.98),rgba(250,247,243,.95));
    box-shadow:
        0 5px 13px rgba(55,46,42,.035),
        inset 0 1px 0 rgba(255,255,255,.95);
    transition:
        transform .20s ease,
        box-shadow .20s ease,
        border-color .20s ease;
}

.q1-summary-card:hover {
    transform: translateY(-3px);
    border-color: #D6C7B9;
    box-shadow:
        0 11px 22px rgba(55,46,42,.075),
        inset 0 1px 0 rgba(255,255,255,.96);
}

.q1-summary-card::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    right: 38%;
    height: 2px;
    border-radius: 999px;
}

.q1-summary-card.orange::before {
    background: linear-gradient(90deg,#E58C2B,#F1B45C,rgba(241,180,92,0));
}
.q1-summary-card.violet::before {
    background: linear-gradient(90deg,#6B3F7D,#A477B5,rgba(164,119,181,0));
}
.q1-summary-card.teal::before {
    background: linear-gradient(90deg,#159786,#66C7B7,rgba(102,199,183,0));
}
.q1-summary-card.blue::before {
    background: linear-gradient(90deg,#2D6CDF,#79A7F8,rgba(121,167,248,0));
}

.q1-summary-card .label {
    color: #7F8A97;
    font-size: .44rem;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: .050em;
}

.q1-summary-card .value {
    color: #17395A;
    font-size: .79rem;
    font-weight: 950;
    line-height: 1.13;
    margin-top: .11rem;
}

.q1-summary-card .note {
    color: #8994A0;
    font-size: .45rem;
    line-height: 1.24;
    margin-top: .08rem;
}

.q1-summary-bottom {
    position: relative;
    z-index: 2;
    display: grid;
    grid-template-columns: 1.25fr 1fr;
    gap: 8px;
    padding: 0 .70rem .60rem .80rem;
}

.q1-summary-finding,
.q1-summary-action {
    border-radius: 11px;
    padding: .45rem .50rem;
    font-size: .49rem;
    line-height: 1.34;
}

.q1-summary-finding {
    color: #526A80;
    background: linear-gradient(90deg,#F4F8FB 0%,#FCFDFE 100%);
    border: 1px solid #DCE6ED;
    border-left: 4px solid #2D6CDF;
}

.q1-summary-action {
    color: #5E6876;
    background:
        radial-gradient(circle at 96% 8%, rgba(107,63,125,.055), transparent 28%),
        linear-gradient(90deg,#FFF6E9 0%,#FFFDFC 100%);
    border: 1px solid #EADAC7;
    border-left: 4px solid #E58C2B;
}

.q1-summary-finding strong,
.q1-summary-action strong {
    color: #17395A;
    font-weight: 950;
}

@media (max-width: 1100px) {
    .q1-summary-grid {
        grid-template-columns: repeat(2, minmax(0,1fr));
    }

    .q1-summary-bottom {
        grid-template-columns: 1fr;
    }
}

@media (prefers-reduced-motion: reduce) {
    .q1-management-summary,
    .q1-management-summary::after,
    .q1-summary-status::before {
        animation: none !important;
    }
}


/* =========================================================
   CAMPUS EVENT & EXECUTION INTELLIGENCE — FULL WIDTH
   ========================================================= */

.event-board {
    position: relative;
    overflow: hidden;
    margin: .55rem 0 .62rem 0;
    border-radius: 17px;
    border: 1px solid #DDD5CD;
    background:
        radial-gradient(circle at 92% 6%, rgba(107,63,125,.060), transparent 25%),
        radial-gradient(circle at 6% 92%, rgba(229,140,43,.050), transparent 24%),
        linear-gradient(130deg,#FFFDFC 0%,#FAF7F2 52%,#FCF9F6 100%);
    box-shadow:
        0 16px 38px rgba(49,42,38,.075),
        inset 0 1px 0 rgba(255,255,255,.96);
    animation: eventBoardBreath 7s ease-in-out infinite;
    transition:
        transform .22s ease,
        box-shadow .22s ease;
}

.event-board:hover {
    transform: translateY(-2px);
    box-shadow:
        0 22px 48px rgba(49,42,38,.105),
        inset 0 1px 0 rgba(255,255,255,.98);
}

.event-board::before {
    content: "";
    position: absolute;
    z-index: 5;
    top: 0;
    left: -28%;
    width: 25%;
    height: 3px;
    border-radius: 999px;
    background: linear-gradient(
        90deg,
        rgba(229,140,43,0),
        #E58C2B,
        #F1B45C,
        #6B3F7D,
        rgba(107,63,125,0)
    );
    animation: eventBoardSweep 7.2s ease-in-out infinite;
}

@keyframes eventBoardBreath {
    0%,100% {
        box-shadow:
            0 16px 38px rgba(49,42,38,.070),
            inset 0 1px 0 rgba(255,255,255,.96);
    }
    50% {
        box-shadow:
            0 20px 44px rgba(67,48,41,.100),
            inset 0 1px 0 rgba(255,255,255,.98);
    }
}

@keyframes eventBoardSweep {
    0%,18%  { left:-28%; opacity:0; }
    30%     { opacity:1; }
    58%     { left:110%; opacity:.95; }
    70%,100%{ left:110%; opacity:0; }
}

.event-board-head {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
    padding: .66rem .78rem .58rem .82rem;
    background:
        linear-gradient(100deg,#17395A 0%,#204B6F 62%,#6B3F7D 135%);
}

.event-board-kicker {
    color: #F2AD4C;
    font-size: .49rem;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: .12em;
}

.event-board-title {
    color: #FFFFFF;
    font-size: 1.02rem;
    font-weight: 950;
    letter-spacing: -.015em;
    margin-top: .08rem;
}

.event-board-sub {
    color: rgba(255,255,255,.72);
    font-size: .53rem;
    line-height: 1.32;
    margin-top: .09rem;
}

.event-board-head-stats {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    justify-content: flex-end;
}

.event-board-stat {
    min-width: 78px;
    padding: .29rem .42rem;
    border-radius: 10px;
    background: rgba(255,255,255,.94);
    border: 1px solid rgba(255,255,255,.72);
    box-shadow: 0 5px 12px rgba(0,0,0,.08);
}

.event-board-stat .label {
    color: #7D8793;
    font-size: .41rem;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: .045em;
}

.event-board-stat .value {
    color: #17395A;
    font-size: .68rem;
    font-weight: 950;
    margin-top: .07rem;
}

.event-board-body {
    padding: .58rem .62rem .62rem .62rem;
}

.event-board-grid {
    display: grid;
    grid-template-columns: .86fr 1.44fr;
    gap: 10px;
}

.event-card {
    position: relative;
    overflow: hidden;
    border-radius: 13px;
    border: 1px solid #E4DED7;
    background:
        linear-gradient(145deg,#FFFFFF 0%,#FBF8F3 100%);
    box-shadow:
        0 7px 17px rgba(55,46,42,.045),
        inset 0 1px 0 rgba(255,255,255,.95);
    padding: .50rem .54rem .52rem .54rem;
    transition:
        transform .20s ease,
        box-shadow .20s ease,
        border-color .20s ease;
}

.event-card:hover {
    transform: translateY(-3px);
    border-color: #D7C8BA;
    box-shadow:
        0 14px 28px rgba(55,45,40,.090),
        inset 0 1px 0 rgba(255,255,255,.98);
}

.event-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 42%;
    height: 2px;
    border-radius: 999px;
}

.event-volume-card::before {
    background: linear-gradient(90deg,#E58C2B,#F1B45C,rgba(241,180,92,0));
}

.event-status-card::before {
    background: linear-gradient(90deg,#159786,#2D6CDF,#6B3F7D,rgba(107,63,125,0));
}

.event-card-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: .5rem;
    margin-bottom: .44rem;
}

.event-card-title {
    color: #17395A;
    font-size: .61rem;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: .045em;
}

.event-card-meta {
    color: #927457;
    font-size: .46rem;
    font-weight: 850;
}

.event-volume-row {
    display: grid;
    grid-template-columns: 66px 1fr 34px;
    gap: 7px;
    align-items: center;
    min-height: 34px;
    padding: .13rem .12rem;
    border-radius: 8px;
    transition: background .18s ease;
}

.event-volume-row:hover {
    background: #FFF8EE;
}

.event-campus-name {
    color: #425C76;
    font-size: .52rem;
    font-weight: 900;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.event-volume-track {
    position: relative;
    overflow: hidden;
    height: 11px;
    border-radius: 999px;
    background: #EEE8E1;
    box-shadow: inset 0 1px 2px rgba(46,37,33,.08);
}

.event-volume-fill {
    height: 100%;
    border-radius: 999px;
    background:
        linear-gradient(90deg,#E58C2B 0%,#F1B45C 45%,#6B3F7D 100%);
    background-size: 180% 100%;
    box-shadow: 0 0 8px rgba(229,140,43,.18);
    animation: eventVolumeFlow 5s ease-in-out infinite;
}

@keyframes eventVolumeFlow {
    0%,100% { background-position: 0% 50%; }
    50%     { background-position: 100% 50%; }
}

.event-volume-count {
    color: #17395A;
    font-size: .57rem;
    font-weight: 950;
    text-align: right;
}

.event-share {
    display: block;
    color: #9AA4AE;
    font-size: .39rem;
    font-weight: 750;
    margin-top: .03rem;
}

.event-status-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 6px;
}

.event-status-table th {
    color: #87919D;
    font-size: .41rem;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: .045em;
    padding: 0 .24rem .08rem .24rem;
    text-align: center;
}

.event-status-table th:first-child {
    text-align: left;
}

.event-status-table td {
    padding: .14rem .24rem;
    vertical-align: middle;
    font-size: .48rem;
}

.event-status-campus {
    color: #425C76;
    font-weight: 900;
    white-space: nowrap;
}

.event-status-total {
    color: #17395A;
    font-size: .54rem !important;
    font-weight: 950;
    text-align: center;
}

.event-stack {
    display: flex;
    width: 100%;
    height: 15px;
    overflow: hidden;
    border-radius: 999px;
    background: #EEE8E1;
    box-shadow:
        inset 0 1px 2px rgba(46,37,33,.08),
        0 2px 4px rgba(50,42,38,.025);
}

.event-stack-seg {
    height: 100%;
    min-width: 0;
    animation: eventStatusPulse 5.8s ease-in-out infinite;
    transition:
        filter .18s ease,
        transform .18s ease;
}

.event-stack-seg:hover {
    filter: brightness(1.10) saturate(1.08);
}

@keyframes eventStatusPulse {
    0%,100% { filter: brightness(1); }
    50%     { filter: brightness(1.04); }
}

.event-status-number {
    text-align: center;
    color: #51687E;
    font-size: .48rem !important;
    font-weight: 900;
}

.event-status-number.zero {
    color: #C0C7CE;
    font-weight: 700;
}

.event-completion-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 42px;
    padding: .15rem .25rem;
    border-radius: 999px;
    font-size: .43rem;
    font-weight: 950;
    color: #2F7A55;
    background: #EBF7F0;
    border: 1px solid #D1EADD;
}

.event-status-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 6px 10px;
    margin-top: .35rem;
    padding-top: .34rem;
    border-top: 1px solid #ECE5DD;
}

.event-status-key {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    color: #718094;
    font-size: .42rem;
    font-weight: 800;
}

.event-status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    box-shadow: 0 0 0 2px rgba(255,255,255,.88);
}

.event-insight-strip {
    display: grid;
    grid-template-columns: repeat(4,minmax(0,1fr));
    gap: 8px;
    margin-top: 9px;
}

.event-insight-card {
    position: relative;
    overflow: hidden;
    min-height: 68px;
    padding: .40rem .44rem;
    border-radius: 11px;
    border: 1px solid #E5DED7;
    background:
        linear-gradient(145deg,#FFFFFF 0%,#FBF8F3 100%);
    box-shadow: 0 5px 13px rgba(55,46,42,.035);
    transition:
        transform .18s ease,
        box-shadow .18s ease;
    animation: eventInsightFloat 6.2s ease-in-out infinite;
}

.event-insight-card:nth-child(2) { animation-delay:.35s; }
.event-insight-card:nth-child(3) { animation-delay:.70s; }
.event-insight-card:nth-child(4) { animation-delay:1.05s; }

.event-insight-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 40%;
    height: 2px;
    border-radius: 999px;
    background: linear-gradient(
        90deg,
        var(--event-accent,#E58C2B),
        rgba(255,255,255,0)
    );
}

.event-insight-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 11px 22px rgba(55,44,39,.080);
}

@keyframes eventInsightFloat {
    0%,100% { transform: translateY(0); }
    50%     { transform: translateY(-1.5px); }
}

.event-insight-label {
    color: #87919D;
    font-size: .42rem;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: .05em;
}

.event-insight-value {
    color: #17395A;
    font-size: .69rem;
    font-weight: 950;
    margin-top: .08rem;
}

.event-insight-note {
    color: #8A949F;
    font-size: .43rem;
    line-height: 1.22;
    margin-top: .07rem;
}

.event-action-box {
    margin-top: 8px;
    padding: .45rem .50rem;
    border-radius: 11px;
    border: 1px solid #E7D8C7;
    border-left: 4px solid #E58C2B;
    background:
        radial-gradient(circle at 97% 10%, rgba(107,63,125,.05), transparent 26%),
        linear-gradient(90deg,#FFF7EC 0%,#FFFDFC 100%);
    color: #5E6C79;
    font-size: .49rem;
    line-height: 1.34;
}

.event-action-box strong {
    color: #17395A;
    font-weight: 950;
}

.event-empty-state {
    padding: 1.2rem;
    border-radius: 12px;
    border: 1px dashed #DDCFC0;
    background: #FFFDFC;
    color: #8995A1;
    text-align: center;
    font-size: .55rem;
}

@media (max-width: 1150px) {
    .event-board-grid {
        grid-template-columns: 1fr;
    }

    .event-insight-strip {
        grid-template-columns: repeat(2,minmax(0,1fr));
    }
}

@media (prefers-reduced-motion: reduce) {
    .event-board,
    .event-board::before,
    .event-volume-fill,
    .event-stack-seg,
    .event-insight-card {
        animation: none !important;
    }
}


/* =========================================================
   RESTORED ACTIVITY TYPE × CAMPUS BUBBLE MATRIX
   ========================================================= */

.activity-bubble-board {
    position: relative;
    overflow: hidden;
    margin: .52rem 0 .58rem 0;
    padding: .66rem .72rem .60rem .72rem;
    border-radius: 17px;
    border: 1px solid #DDD5CD;
    background:
        radial-gradient(circle at 94% 8%, rgba(107,63,125,.055), transparent 24%),
        radial-gradient(circle at 5% 94%, rgba(229,140,43,.045), transparent 22%),
        linear-gradient(130deg,#FFFDFC 0%,#FAF7F2 52%,#FCF9F6 100%);
    box-shadow:
        0 16px 38px rgba(49,42,38,.075),
        inset 0 1px 0 rgba(255,255,255,.96);
    animation: activityBubbleBoardBreath 7s ease-in-out infinite;
    transition:
        transform .22s ease,
        box-shadow .22s ease;
}

.activity-bubble-board:hover {
    transform: translateY(-2px);
    box-shadow:
        0 22px 48px rgba(49,42,38,.105),
        inset 0 1px 0 rgba(255,255,255,.98);
}

.activity-bubble-board::before {
    content: "";
    position: absolute;
    z-index: 5;
    top: 0;
    left: -28%;
    width: 25%;
    height: 3px;
    border-radius: 999px;
    background: linear-gradient(
        90deg,
        rgba(229,140,43,0),
        #E58C2B,
        #F1B45C,
        #6B3F7D,
        rgba(107,63,125,0)
    );
    animation: activityBubbleBoardSweep 7.2s ease-in-out infinite;
}

@keyframes activityBubbleBoardBreath {
    0%,100% {
        box-shadow:
            0 16px 38px rgba(49,42,38,.070),
            inset 0 1px 0 rgba(255,255,255,.96);
    }
    50% {
        box-shadow:
            0 20px 44px rgba(67,48,41,.100),
            inset 0 1px 0 rgba(255,255,255,.98);
    }
}

@keyframes activityBubbleBoardSweep {
    0%,18%  { left:-28%; opacity:0; }
    30%     { opacity:1; }
    58%     { left:110%; opacity:.95; }
    70%,100%{ left:110%; opacity:0; }
}

.activity-bubble-head {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: .38rem;
}

.activity-bubble-kicker {
    color: #E08727;
    font-size: .49rem;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: .12em;
}

.activity-bubble-title {
    color: #17395A;
    font-size: 1.00rem;
    font-weight: 950;
    letter-spacing: -.015em;
    margin-top: .07rem;
}

.activity-bubble-sub {
    color: #758497;
    font-size: .54rem;
    line-height: 1.32;
    margin-top: .08rem;
}

.activity-bubble-badge {
    position: relative;
    z-index: 2;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: .22rem .40rem;
    border-radius: 999px;
    color: #17395A;
    background: #FFF7EA;
    border: 1px solid #E8D7C0;
    box-shadow: 0 4px 12px rgba(55,45,40,.04);
    font-size: .44rem;
    font-weight: 950;
    white-space: nowrap;
}

.activity-bubble-badge::before {
    content: "";
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #28A86B;
    box-shadow: 0 0 0 3px rgba(40,168,107,.12);
}

.activity-bubble-board .q1-css-matrix {
    height: 385px !important;
    min-height: 385px !important;
    max-height: 385px !important;
    margin-top: 0 !important;
}

.activity-bubble-board .q1-css-corner,
.activity-bubble-board .q1-css-campus,
.activity-bubble-board .q1-css-activity,
.activity-bubble-board .q1-css-cell {
    min-height: 39px !important;
}

@media (prefers-reduced-motion: reduce) {
    .activity-bubble-board,
    .activity-bubble-board::before {
        animation: none !important;
    }
}


/* =========================================================
   CAMPUS EVENT SECTION — SIMPLE PROFESSIONAL VERSION
   ========================================================= */

.event-board {
    margin: .52rem 0 .62rem 0 !important;
    border-radius: 15px !important;
    border: 1px solid #E1DAD2 !important;
    background:
        linear-gradient(180deg,#FFFFFF 0%,#FCFAF7 100%) !important;
    box-shadow:
        0 10px 26px rgba(48,41,37,.055),
        inset 0 1px 0 rgba(255,255,255,.96) !important;
    animation: none !important;
}

.event-board:hover {
    transform: none !important;
    box-shadow:
        0 13px 30px rgba(48,41,37,.075),
        inset 0 1px 0 rgba(255,255,255,.98) !important;
}

/* slim animated brand line only */
.event-board::before {
    height: 2px !important;
    width: 22% !important;
    background: linear-gradient(
        90deg,
        rgba(229,140,43,0),
        #E58C2B,
        #6B3F7D,
        rgba(107,63,125,0)
    ) !important;
    animation: eventSimpleSweep 8s ease-in-out infinite !important;
}

@keyframes eventSimpleSweep {
    0%,20%  { left:-24%; opacity:0; }
    32%     { opacity:.9; }
    58%     { left:108%; opacity:.9; }
    70%,100%{ left:108%; opacity:0; }
}

.event-board-head {
    display:flex !important;
    align-items:flex-start !important;
    justify-content:space-between !important;
    gap:1rem !important;
    padding:.62rem .72rem .48rem .76rem !important;
    background:transparent !important;
    border-bottom:1px solid #ECE5DD !important;
}

.event-board-kicker {
    color:#E08727 !important;
    font-size:.46rem !important;
    font-weight:950 !important;
    letter-spacing:.11em !important;
}

.event-board-title {
    color:#17395A !important;
    font-size:.98rem !important;
    margin-top:.06rem !important;
}

.event-board-sub {
    color:#788797 !important;
    font-size:.52rem !important;
    margin-top:.08rem !important;
}

.event-simple-stats {
    display:flex;
    gap:6px;
    flex-wrap:wrap;
    justify-content:flex-end;
    padding-top:.04rem;
}

.event-simple-chip {
    display:inline-flex;
    align-items:center;
    gap:5px;
    padding:.20rem .34rem;
    border-radius:999px;
    background:#FAF7F2;
    border:1px solid #E7DFD7;
    color:#53677B;
    font-size:.43rem;
    font-weight:900;
    white-space:nowrap;
}

.event-simple-chip strong {
    color:#17395A;
    font-size:.49rem;
}

.event-board-body {
    padding:.52rem .56rem .56rem .56rem !important;
}

.event-board-grid {
    grid-template-columns:.72fr 1.28fr !important;
    gap:9px !important;
}

.event-card {
    border-radius:11px !important;
    box-shadow:none !important;
    padding:.44rem .48rem .46rem .48rem !important;
    border:1px solid #E7E0D8 !important;
    background:#FFFFFF !important;
}

.event-card:hover {
    transform:none !important;
    box-shadow:0 6px 16px rgba(48,41,37,.055) !important;
}

.event-card::before {
    height:2px !important;
}

.event-card-head {
    margin-bottom:.34rem !important;
}

.event-card-title {
    font-size:.56rem !important;
}

.event-card-meta {
    font-size:.43rem !important;
}

/* simpler bars */
.event-volume-row {
    min-height:30px !important;
    padding:.10rem .08rem !important;
}

.event-volume-track {
    height:9px !important;
}

.event-volume-fill {
    background:linear-gradient(90deg,#E58C2B,#F2B24E,#8B5C87) !important;
    animation:none !important;
    box-shadow:none !important;
}

.event-status-table {
    border-spacing:0 4px !important;
}

.event-stack {
    height:12px !important;
}

.event-stack-seg {
    animation:none !important;
}

.event-completion-pill {
    min-width:40px !important;
    padding:.12rem .22rem !important;
}

/* remove old bottom metric cards */
.event-insight-strip {
    display:none !important;
}

/* one concise insight strip only */
.event-action-box {
    margin-top:8px !important;
    padding:.46rem .52rem !important;
    border-radius:9px !important;
    border:1px solid #E8DED2 !important;
    border-left:3px solid #E58C2B !important;
    background:#FFF9F1 !important;
    color:#617181 !important;
    font-size:.48rem !important;
    line-height:1.35 !important;
}

.event-action-box strong {
    color:#17395A !important;
}

@media (max-width:1150px) {
    .event-board-grid {
        grid-template-columns:1fr !important;
    }
}

@media (prefers-reduced-motion: reduce) {
    .event-board::before {
        animation:none !important;
    }
}


/* =========================================================
   ACTIVITY × CAMPUS MATRIX — TOTAL + EVENT MINI BUBBLES
   ========================================================= */
.q1-css-cell { padding: 3px 5px !important; }
.q1-cell-bubble-cluster {
    position: relative; z-index: 4; width: 100%; min-height: 36px;
    display: flex; align-items: center; justify-content: center;
    gap: 6px; flex-wrap: wrap; padding: 2px 4px; box-sizing: border-box;
}
.q1-cell-bubble-cluster .q1-motion-bubble { flex: 0 0 auto; }
.q1-event-mini-bubble {
    position: relative; z-index: 5; flex: 0 0 auto;
    display: flex; align-items: center; justify-content: center;
    border-radius: 50%; font-size: .47rem; font-weight: 950; line-height: 1;
    color: #FFFFFF; border: 1.5px solid rgba(255,255,255,.90);
    box-shadow: 0 7px 12px rgba(23,57,90,.20), 0 3px 6px rgba(47,35,31,.12),
                inset 0 1px 2px rgba(255,255,255,.22), inset 0 -2px 4px rgba(23,57,90,.09);
    animation: q1EventMiniFloat var(--event-duration,4.1s) ease-in-out infinite,
               q1EventMiniGlow 6s ease-in-out infinite;
    animation-delay: var(--event-delay,0s), calc(var(--event-delay,0s) + .25s);
    transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
    cursor: default; will-change: transform, box-shadow;
}
.q1-event-mini-bubble:hover {
    animation-play-state: paused; transform: translateY(-4px) scale(1.14);
    box-shadow: 0 13px 20px rgba(23,57,90,.29), 0 5px 9px rgba(229,140,43,.14),
                inset 0 1px 2px rgba(255,255,255,.24);
    filter: saturate(1.08) brightness(1.04);
}
@keyframes q1EventMiniFloat {
    0%,100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-3px) scale(1.06); }
}
@keyframes q1EventMiniGlow {
    0%,100% { filter: brightness(1); }
    50% { filter: brightness(1.035); }
}
.q1-more-events {
    display: inline-flex; align-items: center; justify-content: center;
    min-width: 22px; height: 22px; padding: 0 4px; border-radius: 999px;
    color: #6B3F7D; background: #F7F0F9; border: 1px dashed #D8C4DE;
    font-size: .42rem; font-weight: 950; box-shadow: 0 3px 7px rgba(55,44,39,.04);
}
.q1-event-bubble-legend {
    position: relative; z-index: 2; display: flex; align-items: center; flex-wrap: wrap;
    gap: 5px 10px; margin-top: .28rem; padding: .30rem .38rem .05rem .38rem;
    border-top: 1px solid #E9E1D9;
}
.q1-event-legend-title {
    color: #6C7D8E; font-size: .43rem; font-weight: 950;
    text-transform: uppercase; letter-spacing: .045em; margin-right: 2px;
}
.q1-event-legend-item {
    display: inline-flex; align-items: center; gap: 4px;
    color: #697A8C; font-size: .43rem; font-weight: 800;
}
.q1-event-legend-dot {
    width: 7px; height: 7px; border-radius: 50%;
    box-shadow: 0 0 0 2px rgba(255,255,255,.85);
}
.activity-bubble-board .q1-css-cell,
.activity-bubble-board .q1-css-activity,
.activity-bubble-board .q1-css-campus,
.activity-bubble-board .q1-css-corner { min-height: 48px !important; }
.activity-bubble-board .q1-css-matrix {
    height: 455px !important; min-height: 455px !important; max-height: 455px !important;
}
@media (prefers-reduced-motion: reduce) {
    .q1-event-mini-bubble { animation: none !important; }
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
        margin-top: .18rem;
        margin-bottom: .02rem;
        color: #2B6DE8;
        font-size: .63rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: .10em;
    }

    .overview-section-title {
        color: #102A43;
        font-size: .99rem;
        font-weight: 900;
        letter-spacing: -.01em;
        margin-bottom: .04rem;
    }

    .overview-section-sub {
        color: #7B8DA3;
        font-size: .66rem;
        line-height: 1.30;
        margin-bottom: .22rem;
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
        font-size: .57rem;
        margin-top: -.12rem;
        margin-bottom: .03rem;
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
        .pro-kpi {
            min-height: 69px !important;
            height: 69px !important;
        }
        .pro-kpi .value { font-size: 1.15rem !important; }
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


def overview_section(kicker, title=None, subtitle=None):
    """
    Render an Overview section heading.

    Supports both:
        overview_section("KICKER", "Title", "Subtitle")
    and the older two-argument form:
        overview_section("Title", "Subtitle")
    """
    if subtitle is None:
        subtitle = "" if title is None else str(title)
        title = str(kicker)
        kicker = ""

    kicker = "" if kicker is None else str(kicker)
    title = "" if title is None else str(title)
    subtitle = "" if subtitle is None else str(subtitle)

    kicker_html = (
        f'<div class="overview-section-kicker">{html.escape(kicker)}</div>'
        if kicker.strip()
        else ""
    )

    st.markdown(
        (
            kicker_html
            + f'<div class="overview-section-title">{html.escape(title)}</div>'
            + f'<div class="overview-section-sub">{html.escape(subtitle)}</div>'
            + '<div class="overview-divider"></div>'
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


def _activity_color_map():
    """Shared Activity Type palette for Q1 table and Q1 chart."""
    return {
        "Education Fair": "#0068C9",
        "Faculty Connect": "#83C9FF",
        "Student Workshop": "#FF2B2B",
        "Coaching Visit": "#FFABAB",
        "College Visit": "#29B09D",
        "Mentor Visit": "#6BDF9A",
        "Campus Event": "#FF8700",
    }


def _activity_fallback_color(activity_type):
    palette = [
        "#4B7BEC",
        "#14B8A6",
        "#8B5CF6",
        "#E98A3A",
        "#3AA76D",
        "#D65A63",
        "#5B8DEF",
        "#9B6BCE",
    ]
    key = str(activity_type)
    return palette[sum(ord(ch) for ch in key) % len(palette)]


def render_activity_execution_matrix(frame):
    """
    Professional Q1 pivot-style management table:
    Campus | Activity Type | Event | Status counts | Grand Total | Insights
    """
    required = {"Campus", "Activity Type"}
    if not required.issubset(frame.columns):
        st.info("Campus / Activity Type data is not available for the activity execution matrix.")
        return None

    work = frame.copy()

    for col in ["Campus", "Activity Type", "Event", "Status"]:
        if col not in work.columns:
            work[col] = pd.NA

        work[col] = (
            work[col]
            .astype("string")
            .str.strip()
            .replace({
                "": pd.NA,
                "nan": pd.NA,
                "None": pd.NA,
                "<NA>": pd.NA,
            })
        )

    work = work.dropna(subset=["Campus", "Activity Type"]).copy()

    if work.empty:
        st.info("No activity execution data is available for the selected filters.")
        return None

    work["Event"] = work["Event"].fillna("(blank)")
    work["Status"] = work["Status"].fillna("(blank)")

    # Exact business columns from the supplied reference table.
    status_columns = [
        "Cancelled",
        "Completed",
        "Confirmed",
        "Planned",
    ]

    # If Rescheduled exists, preserve it rather than dropping real activity rows.
    if work["Status"].eq("Rescheduled").any():
        status_columns.append("Rescheduled")

    status_columns.append("(blank)")

    grouped = (
        work.groupby(
            ["Campus", "Activity Type", "Event", "Status"],
            observed=True,
            dropna=False,
        )
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    for status in status_columns:
        if status not in grouped.columns:
            grouped[status] = 0

    # Protect against any unexpected status values without losing records.
    known_statuses = set(status_columns)
    unexpected = [
        col for col in grouped.columns
        if col not in {"Campus", "Activity Type", "Event"}
        and col not in known_statuses
    ]
    if unexpected:
        grouped["(blank)"] = grouped["(blank)"] + grouped[unexpected].sum(axis=1)

    grouped["Grand Total"] = grouped[status_columns].sum(axis=1)

    # Match the supplied pivot-table campus order first, then append any extras.
    preferred_campus_order = ["Indore", "Jaipur", "Lucknow", "Noida"]
    present_campuses = grouped["Campus"].astype(str).unique().tolist()
    campus_order = [
        campus for campus in preferred_campus_order
        if campus in present_campuses
    ] + sorted(
        [campus for campus in present_campuses if campus not in preferred_campus_order],
        key=lambda x: str(x).lower(),
    )

    campus_rank = {campus: idx for idx, campus in enumerate(campus_order)}
    grouped["_campus_rank"] = grouped["Campus"].map(campus_rank).fillna(999)

    grouped = (
        grouped.sort_values(
            ["_campus_rank", "Campus", "Activity Type", "Event"],
            ascending=[True, True, True, True],
        )
        .drop(columns="_campus_rank")
        .reset_index(drop=True)
    )

    activity_colors = _activity_color_map()
    max_row_total = max(int(grouped["Grand Total"].max()), 1)

    status_css = {
        "Cancelled": "cancelled",
        "Completed": "completed",
        "Confirmed": "confirmed",
        "Planned": "planned",
        "Rescheduled": "rescheduled",
        "(blank)": "blank",
    }

    campus_rowspans = grouped.groupby("Campus", observed=True).size().to_dict()
    campus_seen = set()

    body_rows = []

    for _, row in grouped.iterrows():
        campus = str(row["Campus"])
        activity_type = str(row["Activity Type"])
        event_name = str(row["Event"])
        row_total = int(row["Grand Total"])

        campus_html = ""
        if campus not in campus_seen:
            campus_seen.add(campus)
            campus_html = (
                f'<td class="q1-campus-cell" rowspan="{campus_rowspans[campus]}">'
                f'<span class="q1-campus-pill">{html.escape(campus)}</span>'
                '</td>'
            )

        activity_color = activity_colors.get(
            activity_type,
            _activity_fallback_color(activity_type),
        )

        event_class = "blank" if event_name == "(blank)" else ""
        event_html = (
            f'<span class="q1-event-chip {event_class}">'
            f'{html.escape(event_name)}'
            '</span>'
        )

        status_cells = []
        active_status_pairs = []

        for status in status_columns:
            count = int(row.get(status, 0))
            share = _pct(count, row_total)
            css_class = status_css.get(status, "blank")

            status_cells.append(
                '<td>'
                f'<div class="q1-status-box {css_class}">'
                f'<span class="fill" style="width:{min(share,100):.1f}%"></span>'
                f'<span class="num">{count if count else ""}</span>'
                '</div>'
                '</td>'
            )

            if count:
                active_status_pairs.append((status, count))

        # Row-level professional operational insight.
        blank_count = int(row.get("(blank)", 0))
        completed = int(row.get("Completed", 0))
        confirmed = int(row.get("Confirmed", 0))
        planned = int(row.get("Planned", 0))
        cancelled = int(row.get("Cancelled", 0))

        if blank_count > 0:
            insight_text = (
                f'<strong>Data gap:</strong> {blank_count} of {row_total} '
                f'activities have no status.'
            )
        elif planned >= max(completed, confirmed, cancelled) and planned > 0:
            insight_text = (
                f'<strong>Planning-heavy:</strong> {planned}/{row_total} planned; '
                'focus on confirmation and execution.'
            )
        elif confirmed >= max(completed, planned, cancelled) and confirmed > 0:
            insight_text = (
                f'<strong>Ready pipeline:</strong> {confirmed}/{row_total} confirmed; '
                'move these into completion.'
            )
        elif completed >= max(confirmed, planned, cancelled) and completed > 0:
            completed_share = _pct(completed, row_total)
            insight_text = (
                f'<strong>Execution strong:</strong> {completed}/{row_total} completed '
                f'({completed_share:.0f}%).'
            )
        elif cancelled > 0:
            insight_text = (
                f'<strong>Execution risk:</strong> {cancelled}/{row_total} cancelled; '
                'review cause and rescheduling opportunity.'
            )
        elif active_status_pairs:
            top_status, top_count = max(active_status_pairs, key=lambda x: x[1])
            insight_text = (
                f'<strong>{html.escape(top_status)} leads:</strong> '
                f'{top_count}/{row_total} activities.'
            )
        else:
            insight_text = '<strong>Review:</strong> No usable execution status is available.'

        if event_name != "(blank)":
            insight_text += f' Event: <strong>{html.escape(event_name)}</strong>.'

        total_width = _pct(row_total, max_row_total)

        body_rows.append(
            '<tr>'
            + campus_html
            + '<td class="q1-activity-cell">'
              f'<span class="q1-activity-dot" style="background:{activity_color}"></span>'
              f'{html.escape(activity_type)}'
              '</td>'
            + f'<td>{event_html}</td>'
            + "".join(status_cells)
            + '<td>'
              '<div class="q1-total-meter">'
              f'<span class="fill" style="width:{min(total_width,100):.1f}%"></span>'
              f'<span class="num">{row_total}</span>'
              '</div>'
              '</td>'
            + f'<td class="q1-row-insight">{insight_text}</td>'
            + '</tr>'
        )

    status_header_html = "".join(
        f'<th>{html.escape(status)}</th>'
        for status in status_columns
    )

    status_totals = {
        status: int((work["Status"] == status).sum())
        for status in status_columns
    }

    footer_status_html = "".join(
        f'<td>{status_totals.get(status, 0):,}</td>'
        for status in status_columns
    )

    grand_total = int(len(work))
    blank_total = int((work["Status"] == "(blank)").sum())
    completed_total = int((work["Status"] == "Completed").sum())
    confirmed_total = int((work["Status"] == "Confirmed").sum())
    planned_total = int((work["Status"] == "Planned").sum())
    cancelled_total = int((work["Status"] == "Cancelled").sum())

    campus_totals = (
        work.groupby("Campus", observed=True)
        .size()
        .sort_values(ascending=False)
    )
    leader_campus = str(campus_totals.index[0])
    leader_total = int(campus_totals.iloc[0])

    completion_rate = _pct(completed_total, grand_total)
    status_capture_rate = _pct(grand_total - blank_total, grand_total)

    table_html = (
        '<div class="q1-matrix-shell">'
            '<div class="q1-matrix-head">'
                '<div>'
                    '<div class="q1-matrix-title">Activity Execution Matrix</div>'
                    '<div class="q1-matrix-sub">'
                    'Campus → Activity Type → Event, with execution status, totals and management insight.'
                    '</div>'
                '</div>'
                f'<div class="q1-matrix-badge">{grand_total:,} filtered activities</div>'
            '</div>'
            '<div class="q1-matrix-scroll">'
                '<table class="q1-exec-table">'
                    '<colgroup>'
                        '<col style="width:88px">'
                        '<col style="width:150px">'
                        '<col style="width:118px">'
                        + "".join('<col style="width:76px">' for _ in status_columns)
                        + '<col style="width:88px">'
                        '<col style="width:275px">'
                    '</colgroup>'
                    '<thead>'
                        '<tr>'
                            '<th colspan="3">Activity Portfolio</th>'
                            f'<th colspan="{len(status_columns) + 1}">Status</th>'
                            '<th rowspan="2">Insights</th>'
                        '</tr>'
                        '<tr>'
                            '<th>Campus</th>'
                            '<th>Activity Type</th>'
                            '<th>Event</th>'
                            + status_header_html
                            + '<th>Grand Total</th>'
                        '</tr>'
                    '</thead>'
                    '<tbody>'
                        + "".join(body_rows)
                    + '</tbody>'
                    '<tfoot>'
                        '<tr>'
                            '<td colspan="3">Grand Total</td>'
                            + footer_status_html
                            + f'<td>{grand_total:,}</td>'
                            + (
                                '<td>'
                                f'{completion_rate:.1f}% completed · '
                                f'{status_capture_rate:.1f}% status captured'
                                '</td>'
                            )
                        + '</tr>'
                    '</tfoot>'
                '</table>'
            '</div>'
            '<div class="q1-matrix-footer">'
                f'<span><strong>{leader_campus}</strong> leads activity volume with {leader_total:,}</span>'
                f'<span><strong>{blank_total:,}</strong> blank status · '
                f'<strong>{grand_total - blank_total:,}</strong> status-captured</span>'
            '</div>'
        '</div>'
    )

    st.markdown(table_html, unsafe_allow_html=True)

    return {
        "grand_total": grand_total,
        "leader_campus": leader_campus,
        "leader_total": leader_total,
        "completed": completed_total,
        "confirmed": confirmed_total,
        "planned": planned_total,
        "cancelled": cancelled_total,
        "blank": blank_total,
        "completion_rate": completion_rate,
        "status_capture_rate": status_capture_rate,
    }


# =========================================================
# FINAL REFERENCE-STYLE OVERVIEW UI OVERRIDES
# =========================================================
st.markdown(
    """
<style>
/* =========================================================
   FINAL OVERVIEW — layout from approved reference image
   ========================================================= */
:root {
    --ov-navy:#0F2F57;
    --ov-blue:#245FC5;
    --ov-violet:#6E43C8;
    --ov-orange:#E79022;
    --ov-teal:#18A98D;
    --ov-green:#25A96B;
    --ov-border:#DDE5EF;
    --ov-muted:#71839A;
    --ov-canvas:#F7F8FB;
}

.block-container {
    max-width:none !important;
    padding-top:.22rem !important;
    padding-left:1.25rem !important;
    padding-right:1.25rem !important;
    padding-bottom:1.10rem !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 92% 1%, rgba(108,67,200,.045), transparent 25%),
        radial-gradient(circle at 55% 25%, rgba(36,95,197,.035), transparent 28%),
        linear-gradient(180deg,#FAFBFD 0%,#F5F7FA 100%) !important;
}

/* ---------- Header ---------- */
.overview-header {
    transform:none !important;
    margin:0 0 .34rem 0 !important;
    padding:.10rem .18rem 0 .18rem;
}
.overview-eyebrow {
    color:#6B3F7D !important;
    font-size:.61rem !important;
    font-weight:950 !important;
    letter-spacing:.15em !important;
    margin-bottom:.08rem !important;
}
.overview-title-row,
.overview-title-wrap {
    height:auto !important;
    overflow:visible !important;
}
.overview-title {
    position:static !important;
    transform:none !important;
    width:auto !important;
    color:var(--ov-navy) !important;
    font-size:1.48rem !important;
    font-weight:950 !important;
    line-height:1.02 !important;
    letter-spacing:-.025em !important;
    animation:ovTitleTone 8s ease-in-out infinite !important;
}
@keyframes ovTitleTone {
    0%,100% { text-shadow:0 0 0 rgba(36,95,197,0); }
    50% { text-shadow:0 3px 14px rgba(36,95,197,.11); }
}
.overview-subtitle {
    color:#68809A !important;
    font-size:.74rem !important;
    margin-top:.18rem !important;
}
.overview-accent {
    height:2px !important;
    margin-top:.30rem !important;
    background:linear-gradient(90deg,#E58C2B 0%,#6B3F7D 52%,rgba(107,63,125,0) 100%) !important;
}

/* =========================================================
   FILTER PANEL — premium one-line control deck
   ========================================================= */
.ov-filter-shell-marker,
.ov-snapshot-shell-marker { display:none; }

div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker) {
    position:relative !important;
    overflow:hidden !important;
    margin:.18rem 0 .46rem 0 !important;
    padding:.48rem .62rem .58rem .62rem !important;
    border-radius:15px !important;
    border:1px solid #E4DDD5 !important;
    background:
        radial-gradient(circle at 96% 12%, rgba(107,63,125,.045), transparent 24%),
        linear-gradient(120deg,#FFFDFC 0%,#FBF8F3 52%,#FCF9F6 100%) !important;
    box-shadow:0 10px 28px rgba(56,45,40,.055), inset 0 1px 0 rgba(255,255,255,.98) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker)::before {
    content:"";
    position:absolute;
    z-index:4;
    top:0;
    left:-24%;
    width:22%;
    height:2px;
    background:linear-gradient(90deg,transparent,#E58C2B,#6B3F7D,transparent);
    animation:ovFilterSweep 7.5s ease-in-out infinite;
}
@keyframes ovFilterSweep {
    0%,18% { left:-24%; opacity:0; }
    28% { opacity:1; }
    58% { left:108%; opacity:.95; }
    70%,100% { left:108%; opacity:0; }
}

.ov-filter-head {
    display:flex;
    align-items:center;
    gap:.50rem;
    margin:.02rem .05rem .28rem .05rem;
}
.ov-filter-icon {
    width:25px;
    height:25px;
    border-radius:8px;
    display:inline-flex;
    align-items:center;
    justify-content:center;
    color:#245FC5;
    background:linear-gradient(145deg,#EEF4FF,#F6F0FF);
    border:1px solid #DCE5F5;
    font-size:.78rem;
    box-shadow:0 4px 10px rgba(36,95,197,.07);
}
.ov-filter-title {
    color:var(--ov-navy);
    font-size:.89rem;
    font-weight:950;
}
.ov-filter-help {
    color:#7C8DA2;
    font-size:.56rem;
    padding-left:.48rem;
    border-left:1px solid #D8E0E9;
}

/* Streamlit row containing the filters */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker)
div[data-testid="stHorizontalBlock"] {
    align-items:end !important;
    gap:.48rem !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker)
div[data-testid="stSelectbox"] label,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker)
div[data-testid="stDateInput"] label,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker)
div[data-testid="stTextInput"] label {
    color:#36526F !important;
    font-size:.57rem !important;
    font-weight:900 !important;
    margin:0 0 .12rem .06rem !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker)
div[data-baseweb="select"] > div,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker)
div[data-testid="stDateInput"] input,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker)
div[data-testid="stTextInput"] input {
    min-height:2.28rem !important;
    height:2.28rem !important;
    border-radius:10px !important;
    border:1px solid #DDE5EF !important;
    background:linear-gradient(180deg,#FFFFFF 0%,#F8FAFD 100%) !important;
    box-shadow:0 4px 12px rgba(28,54,86,.035), inset 0 1px 0 rgba(255,255,255,.98) !important;
    color:#183A60 !important;
    font-size:.65rem !important;
    transition:transform .18s ease, border-color .18s ease, box-shadow .18s ease !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker)
div[data-baseweb="select"] > div:hover,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker)
div[data-testid="stDateInput"] input:hover {
    transform:translateY(-2px) !important;
    border-color:#B8CBE7 !important;
    box-shadow:0 9px 18px rgba(36,95,197,.08), 0 0 0 1px rgba(107,63,125,.035) inset !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker)
div[data-baseweb="select"] svg,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker)
div[data-testid="stDateInput"] svg {
    color:#6B3F7D !important;
    width:17px !important;
    height:17px !important;
    transition:transform .18s ease !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker)
div[data-baseweb="select"]:hover svg {
    transform:translateY(1px) scale(1.08);
}

.overview-filter-reset-spacer { height:1.08rem !important; }

div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker)
div[data-testid="stButton"] button {
    min-height:2.28rem !important;
    height:2.28rem !important;
    border-radius:10px !important;
    border:1px solid #284C72 !important;
    color:#FFFFFF !important;
    font-size:.62rem !important;
    font-weight:900 !important;
    background:linear-gradient(120deg,#11365C 0%,#24507A 58%,#5E3D79 135%) !important;
    background-size:170% 100% !important;
    box-shadow:0 8px 18px rgba(17,54,92,.18) !important;
    animation:ovResetFlow 6s ease-in-out infinite !important;
}
@keyframes ovResetFlow {
    0%,100% { background-position:0% 50%; }
    50% { background-position:100% 50%; }
}

/* =========================================================
   EXECUTIVE SNAPSHOT — one unified shell
   ========================================================= */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-snapshot-shell-marker) {
    position:relative !important;
    overflow:hidden !important;
    margin:.05rem 0 .50rem 0 !important;
    padding:.48rem .56rem .54rem .56rem !important;
    border-radius:15px !important;
    border:1px solid #E1DAD2 !important;
    background:linear-gradient(180deg,#FFFEFC 0%,#FBF8F4 100%) !important;
    box-shadow:0 11px 28px rgba(50,42,38,.055), inset 0 1px 0 rgba(255,255,255,.98) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-snapshot-shell-marker)::before {
    content:"";
    position:absolute;
    left:0;
    top:0;
    bottom:0;
    width:4px;
    background:linear-gradient(180deg,#F0A13A,#E58C2B 46%,#6B3F7D 100%);
}

.snapshot-banner {
    margin:0 0 .34rem 0 !important;
    padding:.05rem .22rem .30rem .30rem !important;
    border:0 !important;
    border-radius:0 !important;
    background:transparent !important;
    box-shadow:none !important;
}
.snapshot-banner::before,
.snapshot-banner::after { display:none !important; }
.snapshot-eyebrow {
    color:#E08727 !important;
    font-size:.46rem !important;
    font-weight:950 !important;
    letter-spacing:.11em !important;
}
.snapshot-title {
    color:var(--ov-navy) !important;
    font-size:.95rem !important;
    font-weight:950 !important;
}
.snapshot-sub {
    color:#7C8A98 !important;
    font-size:.50rem !important;
}
.snapshot-badges { gap:5px !important; }
.snapshot-badge {
    padding:.18rem .34rem !important;
    font-size:.40rem !important;
    font-weight:950 !important;
    border-radius:999px !important;
}

/* KPI row */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-snapshot-shell-marker)
div[data-testid="stHorizontalBlock"] {
    gap:.46rem !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-snapshot-shell-marker) .pro-kpi {
    min-height:74px !important;
    height:74px !important;
    border-radius:11px !important;
    padding:.42rem .50rem .38rem .50rem !important;
    box-shadow:0 6px 16px rgba(31,51,76,.045), inset 0 1px 0 rgba(255,255,255,.96) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-snapshot-shell-marker) .pro-kpi:hover {
    transform:translateY(-3px) scale(1.01) !important;
    box-shadow:0 12px 25px rgba(31,51,76,.09) !important;
}

/* =========================================================
   ACTIVITY MATRIX — compact approved reference layout
   ========================================================= */
.activity-bubble-board {
    margin:.10rem 0 .52rem 0 !important;
    padding:.50rem .60rem .48rem .60rem !important;
    border-radius:15px !important;
    border:1px solid #E1DAD2 !important;
    background:linear-gradient(180deg,#FFFFFF 0%,#FCFAF7 100%) !important;
    box-shadow:0 12px 28px rgba(50,42,38,.055), inset 0 1px 0 rgba(255,255,255,.97) !important;
}
.activity-bubble-head { margin-bottom:.24rem !important; }
.activity-bubble-kicker { font-size:.45rem !important; color:#E08727 !important; }
.activity-bubble-title { font-size:.96rem !important; color:var(--ov-navy) !important; }
.activity-bubble-sub { font-size:.48rem !important; color:#7B8998 !important; }
.activity-bubble-badge {
    font-size:.40rem !important;
    padding:.18rem .34rem !important;
    border-color:#ECDCC6 !important;
    background:#FFF9EF !important;
}
.activity-bubble-board .q1-css-matrix {
    height:305px !important;
    min-height:305px !important;
    max-height:305px !important;
    border-radius:10px !important;
    padding:.18rem .20rem .18rem .20rem !important;
    box-shadow:0 5px 14px rgba(52,43,38,.035), 0 0 0 1px #E6DED5 inset !important;
}
.activity-bubble-board .q1-css-corner,
.activity-bubble-board .q1-css-campus,
.activity-bubble-board .q1-css-activity,
.activity-bubble-board .q1-css-cell {
    min-height:34px !important;
}
.activity-bubble-board .q1-css-campus { font-size:.50rem !important; font-weight:900 !important; }
.activity-bubble-board .q1-css-activity { font-size:.48rem !important; font-weight:800 !important; }
.q1-motion-bubble {
    box-shadow:0 7px 13px rgba(23,57,90,.18), 0 2px 5px rgba(47,35,31,.10) !important;
}
.q1-event-mini-bubble {
    box-shadow:0 5px 10px rgba(23,57,90,.16), 0 2px 4px rgba(47,35,31,.09) !important;
}
.q1-css-matrix-foot,
.q1-event-bubble-legend { display:none !important; }

/* =========================================================
   MONTHLY CAMPUS SUMMARY — approved reference layout
   ========================================================= */
.monthly-summary-shell {
    position:relative;
    overflow:hidden;
    margin:.08rem 0 .54rem 0 !important;
    padding:.48rem .56rem .52rem .56rem !important;
    border-radius:15px !important;
    border:1px solid #DDE5EF !important;
    background:linear-gradient(180deg,#FFFFFF 0%,#FBFCFE 100%) !important;
    box-shadow:0 11px 28px rgba(24,56,102,.055) !important;
}
.monthly-summary-shell::before {
    content:"";
    position:absolute;
    top:0;
    left:-24%;
    width:22%;
    height:2px;
    background:linear-gradient(90deg,transparent,#2B6DE8,#7C3AED,transparent);
    animation:monthlySweep 7.4s ease-in-out infinite;
}
@keyframes monthlySweep {
    0%,18% { left:-24%; opacity:0; }
    30% { opacity:.9; }
    58% { left:108%; opacity:.9; }
    70%,100% { left:108%; opacity:0; }
}
.monthly-summary-head { margin-bottom:.34rem !important; align-items:center !important; }
.monthly-summary-title { font-size:.90rem !important; color:var(--ov-navy) !important; }
.monthly-summary-sub { font-size:.49rem !important; color:#7B8DA3 !important; }
.monthly-range-chip {
    display:inline-flex;
    align-items:center;
    gap:5px;
    padding:.20rem .38rem;
    border-radius:999px;
    background:linear-gradient(145deg,#F5F8FF,#F5F0FF);
    border:1px solid #DCE5F4;
    color:#385A80;
    font-size:.43rem;
    font-weight:900;
    white-space:nowrap;
    box-shadow:0 3px 8px rgba(36,95,197,.04);
}
.monthly-range-chip::before { content:"▣"; color:#6B3F7D; font-size:.56rem; }
.monthly-table-wrap {
    border-radius:10px !important;
    border:1px solid #DFE7F0 !important;
    box-shadow:0 4px 12px rgba(24,56,102,.025) inset !important;
}
.monthly-table {
    min-width:1180px !important;
    font-size:9px !important;
}
.monthly-table th,
.monthly-table td {
    padding:4px 4px !important;
    font-size:9px !important;
}
.monthly-table .ms-month-group,
.monthly-table .ms-campus-group { font-size:9px !important; }
.monthly-table .ms-subhead { font-size:8px !important; }

.monthly-panels {
    grid-template-columns:1fr 1.04fr 1.04fr !important;
    gap:8px !important;
    margin-top:8px !important;
}
.monthly-panel {
    min-height:142px !important;
    padding:.48rem .52rem .46rem .52rem !important;
    border-radius:12px !important;
    box-shadow:0 6px 16px rgba(23,58,103,.045) !important;
    transition:transform .18s ease, box-shadow .18s ease !important;
}
.monthly-panel:hover {
    transform:translateY(-2px);
    box-shadow:0 10px 22px rgba(23,58,103,.075) !important;
}
.monthly-panel-title {
    gap:6px !important;
    font-size:.72rem !important;
    margin-bottom:6px !important;
}
.monthly-panel-icon {
    width:22px !important;
    height:22px !important;
    flex:0 0 22px !important;
    font-size:11px !important;
}
.monthly-point {
    grid-template-columns:21px 1fr !important;
    gap:6px !important;
    margin-bottom:5px !important;
}
.monthly-point-badge {
    width:19px !important;
    height:19px !important;
    font-size:9px !important;
    box-shadow:0 4px 9px rgba(43,109,232,.18) !important;
}
.monthly-point-text {
    font-size:.52rem !important;
    line-height:1.30 !important;
}
.monthly-perf-table { font-size:9px !important; }
.monthly-perf-table th { font-size:8px !important; padding:0 0 4px 0 !important; }
.monthly-perf-table td { font-size:9px !important; padding:4px 0 !important; }
.monthly-perf-bar { height:7px !important; }
.monthly-perf-pct { font-size:8px !important; }

@media (max-width:1250px) {
    .monthly-panels { grid-template-columns:1fr !important; }
    .activity-bubble-board .q1-css-matrix {
        height:330px !important;
        min-height:330px !important;
        max-height:330px !important;
    }
}

@media (prefers-reduced-motion:reduce) {
    .overview-title,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker)::before,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ov-filter-shell-marker) div[data-testid="stButton"] button,
    .monthly-summary-shell::before {
        animation:none !important;
    }
}
</style>
    """,
    unsafe_allow_html=True,
)

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
with st.container(border=True):
    st.markdown('<span class="ov-filter-shell-marker"></span>', unsafe_allow_html=True)
    st.markdown(
        (
            '<div class="ov-filter-head">'
                '<span class="ov-filter-icon">⌘</span>'
                '<span class="ov-filter-title">Filters</span>'
                '<span class="ov-filter-help">Refine the outreach view across campus, activity, event and execution dimensions.</span>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    filter_cols = st.columns(
        [0.82, 1.00, 0.78, 0.82, 1.02, 0.90, 0.70, 1.24, 0.66],
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
    filtered["Event"]
    .astype("string")
    .str.strip()
    .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA, "(blank)": pd.NA})
    .notna()
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
with st.container(border=True):
    st.markdown('<span class="ov-snapshot-shell-marker"></span>', unsafe_allow_html=True)

    st.markdown(
        (
            '<div class="snapshot-banner">'
                '<div class="snapshot-copy">'
                    '<div class="snapshot-eyebrow">Executive Snapshot</div>'
                    '<div class="snapshot-title">Outreach Performance at a Glance</div>'
                    '<div class="snapshot-sub">'
                        'Live outreach volume, event coverage and student-reach performance.'
                    '</div>'
                '</div>'
                '<div class="snapshot-badges">'
                    '<span class="snapshot-badge navy">LIVE VIEW</span>'
                    '<span class="snapshot-badge orange">MANAGEMENT SUMMARY</span>'
                    '<span class="snapshot-badge violet">AUTO-SYNC</span>'
                '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
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
# ACTIVITY TYPE × CAMPUS BUBBLE MATRIX
# Main bubble = total activity count
# Small bubbles = Event-wise counts inside the same cell
# =========================================================
activity_mix = pd.DataFrame()
event_mix = pd.DataFrame()

if {"Campus", "Activity Type"}.issubset(filtered.columns):
    activity_mix = (
        filtered.dropna(subset=["Campus", "Activity Type"])
        .groupby(["Activity Type", "Campus"], observed=True)
        .size()
        .reset_index(name="Activities")
    )

if {"Campus", "Activity Type", "Event"}.issubset(filtered.columns):
    event_source = filtered.copy()
    event_source["Event"] = (
        event_source["Event"].astype("string").str.strip().replace({
            "": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA, "(blank)": pd.NA,
        })
    )
    event_source = event_source.dropna(subset=["Campus", "Activity Type", "Event"])
    if not event_source.empty:
        event_mix = (
            event_source.groupby(["Activity Type", "Campus", "Event"], observed=True)
            .size().reset_index(name="Event Count")
        )

if not activity_mix.empty:
    activity_colors = _activity_color_map()
    for activity_type in activity_mix["Activity Type"].astype(str).unique():
        activity_colors.setdefault(activity_type, _activity_fallback_color(activity_type))

    campus_totals_activity = (
        activity_mix.groupby("Campus", observed=True)["Activities"].sum().sort_values(ascending=False)
    )
    activity_totals = (
        activity_mix.groupby("Activity Type", observed=True)["Activities"].sum().sort_values(ascending=False)
    )
    preferred_campus_order = ["Noida", "Lucknow", "Jaipur", "Indore"]
    campus_present = campus_totals_activity.index.astype(str).tolist()
    campus_order = [c for c in preferred_campus_order if c in campus_present]
    campus_order += [c for c in campus_present if c not in campus_order]
    activity_order = activity_totals.index.tolist()
    max_count = max(int(activity_mix["Activities"].max()), 1)
    bubble_lookup = {
        (str(row["Activity Type"]), str(row["Campus"])): int(row["Activities"])
        for _, row in activity_mix.iterrows()
    }

    event_palette = [
        "#6B3F7D", "#E58C2B", "#2D6CDF", "#159786", "#D65A63",
        "#7453C6", "#2A8B5A", "#D18A24", "#4E7A9E", "#B85B87",
    ]
    event_color_map = {}
    event_lookup = {}
    if not event_mix.empty:
        event_order = (
            event_mix.groupby("Event", observed=True)["Event Count"].sum()
            .sort_values(ascending=False).index.astype(str).tolist()
        )
        event_color_map = {
            event_name: event_palette[idx % len(event_palette)]
            for idx, event_name in enumerate(event_order)
        }
        max_event_count = max(int(event_mix["Event Count"].max()), 1)
        for (activity_type, campus), group in event_mix.groupby(
            ["Activity Type", "Campus"], observed=True
        ):
            event_lookup[(str(activity_type), str(campus))] = (
                group.sort_values(["Event Count", "Event"], ascending=[False, True]).reset_index(drop=True)
            )
    else:
        event_order = []
        max_event_count = 1

    def _hex_luminance(hex_color):
        value = str(hex_color).lstrip("#")
        if len(value) != 6:
            return 1.0
        r = int(value[0:2], 16) / 255.0
        g = int(value[2:4], 16) / 255.0
        b = int(value[4:6], 16) / 255.0
        return (0.2126 * r) + (0.7152 * g) + (0.0722 * b)

    grid_columns = "118px " + " ".join(["minmax(125px, 1fr)"] * len(campus_order))
    total_activity_count = int(activity_mix["Activities"].sum())
    total_event_records = int(event_mix["Event Count"].sum()) if not event_mix.empty else 0

    matrix_parts = [
        '<div class="activity-bubble-board">',
        '<div class="activity-bubble-head">',
        '<div>',
        '<div class="activity-bubble-kicker">Activity Portfolio</div>',
        '<div class="activity-bubble-title">Activity Type × Campus Matrix</div>',
        '<div class="activity-bubble-sub">Large bubble = total activity count. Small bubbles = Event-wise counts inside the same Campus × Activity Type cell.</div>',
        '</div>',
        f'<div class="activity-bubble-badge">{total_activity_count:,} activities' +
        (f' · {total_event_records:,} event records' if total_event_records else '') + '</div>',
        '</div>',
        '<div class="q1-css-matrix">',
        f'<div class="q1-css-grid" style="grid-template-columns:{grid_columns};">',
        '<div class="q1-css-corner"></div>',
    ]

    for campus in campus_order:
        matrix_parts.append(f'<div class="q1-css-campus">{html.escape(str(campus))}</div>')

    bubble_index = 0
    event_bubble_index = 0

    for activity_type in activity_order:
        matrix_parts.append(f'<div class="q1-css-activity">{html.escape(str(activity_type))}</div>')
        activity_color = activity_colors.get(activity_type, _activity_fallback_color(activity_type))
        total_text_color = "#FFFFFF" if _hex_luminance(activity_color) < .47 else "#17395A"

        for campus in campus_order:
            total_count = bubble_lookup.get((str(activity_type), str(campus)), 0)
            matrix_parts.append('<div class="q1-css-cell">')

            if total_count > 0:
                matrix_parts.append('<div class="q1-cell-bubble-cluster">')
                cell_events = event_lookup.get((str(activity_type), str(campus)))

                if cell_events is not None and not cell_events.empty:
                    visible_events = cell_events.head(4)
                    hidden_events = max(len(cell_events) - len(visible_events), 0)

                    for _, event_row in visible_events.iterrows():
                        event_name = str(event_row["Event"])
                        event_count = int(event_row["Event Count"])
                        event_color = event_color_map.get(event_name, "#6B3F7D")
                        event_text_color = "#FFFFFF" if _hex_luminance(event_color) < .58 else "#17395A"
                        event_size = 15 + (math.sqrt(event_count / max_event_count) * 11)
                        event_delay = -((event_bubble_index % 11) * .23)
                        event_duration = 3.7 + ((event_bubble_index % 5) * .19)
                        event_tooltip = (
                            f"Campus: {campus} | Activity Type: {activity_type} | "
                            f"Event: {event_name} | Event Count: {event_count}"
                        )
                        matrix_parts.append(
                            '<div class="q1-event-mini-bubble" '
                            f'title="{html.escape(event_tooltip)}" '
                            f'style="width:{event_size:.1f}px;height:{event_size:.1f}px;'
                            f'background:{event_color};color:{event_text_color};'
                            f'--event-delay:{event_delay:.2f}s;--event-duration:{event_duration:.2f}s;">'
                            f'{event_count}</div>'
                        )
                        event_bubble_index += 1

                    if hidden_events > 0:
                        hidden_names = ", ".join(cell_events.iloc[4:]["Event"].astype(str).tolist())
                        matrix_parts.append(
                            f'<span class="q1-more-events" title="{html.escape(hidden_names)}">+{hidden_events}</span>'
                        )

                size_px = 19 + (math.sqrt(total_count / max_count) * 29)
                delay = -((bubble_index % 9) * .31)
                duration = 3.8 + ((bubble_index % 5) * .22)
                total_tooltip = f"{activity_type} · {campus}: {total_count} total activities"
                matrix_parts.append(
                    '<div class="q1-motion-bubble" '
                    f'title="{html.escape(total_tooltip)}" '
                    f'style="width:{size_px:.1f}px;height:{size_px:.1f}px;'
                    f'background:{activity_color};color:{total_text_color};'
                    f'--bubble-delay:{delay:.2f}s;--bubble-duration:{duration:.2f}s;">'
                    f'<span class="q1-bubble-count">{total_count}</span></div>'
                )
                bubble_index += 1
                matrix_parts.append('</div>')

            matrix_parts.append('</div>')

    matrix_parts.extend([
        '</div>',
        '<div class="q1-css-matrix-foot">',
        '<span><strong>Large bubble:</strong> total activity count · <strong>Small bubbles:</strong> Event-wise count</span>',
        '<span><strong>Hover:</strong> Event name + exact count</span>',
        '</div>',
    ])

    if event_order:
        matrix_parts.append(
            '<div class="q1-event-bubble-legend"><span class="q1-event-legend-title">Event bubbles</span>'
        )
        for event_name in event_order:
            event_color = event_color_map[event_name]
            matrix_parts.append(
                '<span class="q1-event-legend-item">'
                f'<span class="q1-event-legend-dot" style="background:{event_color};"></span>'
                f'{html.escape(event_name)}</span>'
            )
        matrix_parts.append('</div>')

    matrix_parts.extend(['</div>', '</div>'])
    st.markdown("".join(matrix_parts), unsafe_allow_html=True)


# =========================================================
# MONTHLY CAMPUS-WISE ACTIVITY & EVENT SUMMARY
# Approved compact reference layout
# =========================================================

def _monthly_status_clean(x):
    if pd.isna(x):
        return ""
    return str(x).strip().title()


def _monthly_safe_pct(num, den):
    try:
        num = float(num)
        den = float(den)
        if den == 0:
            return 0.0
        return (num / den) * 100.0
    except Exception:
        return 0.0


def _monthly_num(v):
    try:
        return int(v)
    except Exception:
        return 0


def _monthly_perf_bar(pct):
    pct = max(0.0, min(100.0, float(pct)))
    return f"""
        <div style="display:flex; align-items:center; gap:5px;">
            <div class="monthly-perf-bar">
                <div class="monthly-perf-fill" style="width:{pct:.1f}%;"></div>
            </div>
            <span class="monthly-perf-pct">{pct:.0f}%</span>
        </div>
    """


if "Activity Date" not in filtered.columns or filtered["Activity Date"].dropna().empty:
    st.info("Monthly summary cannot be calculated because Activity Date is unavailable for this selection.")
else:
    monthly_base = filtered.dropna(subset=["Activity Date"]).copy()

    monthly_base["Month Start"] = (
        monthly_base["Activity Date"].dt.to_period("M").dt.to_timestamp()
    )
    multi_year = monthly_base["Month Start"].dt.year.nunique() > 1
    monthly_base["Month Label"] = monthly_base["Month Start"].dt.strftime(
        "%b %Y" if multi_year else "%b"
    )
    monthly_base["Campus"] = (
        monthly_base["Campus"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )
    monthly_base["Status Clean"] = (
        monthly_base["Status"].apply(_monthly_status_clean)
        if "Status" in monthly_base.columns
        else ""
    )

    if "Event" in monthly_base.columns:
        monthly_base["Event Clean"] = (
            monthly_base["Event"]
            .astype("string")
            .str.strip()
            .replace({
                "": pd.NA,
                "nan": pd.NA,
                "None": pd.NA,
                "<NA>": pd.NA,
                "(blank)": pd.NA,
            })
        )
        monthly_base["Has Event"] = monthly_base["Event Clean"].notna()
    else:
        monthly_base["Has Event"] = False

    preferred_campuses = ["Noida", "Lucknow", "Jaipur", "Indore"]
    campus_values = monthly_base["Campus"].dropna().astype(str).unique().tolist()
    campuses = [c for c in preferred_campuses if c in campus_values]
    campuses += [c for c in campus_values if c not in campuses]

    months_order = (
        monthly_base[["Month Start", "Month Label"]]
        .drop_duplicates()
        .sort_values("Month Start")
        .reset_index(drop=True)
    )

    rows = []

    for _, mrow in months_order.iterrows():
        month_start = mrow["Month Start"]
        month_label = mrow["Month Label"]
        month_slice = monthly_base[monthly_base["Month Start"].eq(month_start)].copy()
        row = {"Month": month_label}

        for campus in campuses:
            cdf = month_slice[month_slice["Campus"].eq(campus)].copy()
            event_cdf = cdf[cdf["Has Event"]].copy()

            row[(campus, "Activities")] = int(len(cdf))
            row[(campus, "Events")] = int(len(event_cdf))
            row[(campus, "Completed")] = int(event_cdf["Status Clean"].eq("Completed").sum())
            row[(campus, "Confirmed")] = int(event_cdf["Status Clean"].eq("Confirmed").sum())
            row[(campus, "Planned")] = int(event_cdf["Status Clean"].eq("Planned").sum())
            row[(campus, "Cancelled")] = int(event_cdf["Status Clean"].eq("Cancelled").sum())

        rows.append(row)

    total_row = {"Month": "Total"}
    for campus in campuses:
        cdf = monthly_base[monthly_base["Campus"].eq(campus)].copy()
        event_cdf = cdf[cdf["Has Event"]].copy()

        total_row[(campus, "Activities")] = int(len(cdf))
        total_row[(campus, "Events")] = int(len(event_cdf))
        total_row[(campus, "Completed")] = int(event_cdf["Status Clean"].eq("Completed").sum())
        total_row[(campus, "Confirmed")] = int(event_cdf["Status Clean"].eq("Confirmed").sum())
        total_row[(campus, "Planned")] = int(event_cdf["Status Clean"].eq("Planned").sum())
        total_row[(campus, "Cancelled")] = int(event_cdf["Status Clean"].eq("Cancelled").sum())

    rows.append(total_row)

    # -----------------------------
    # Month and campus intelligence
    # -----------------------------
    month_totals = []
    for _, mrow in months_order.iterrows():
        month_start = mrow["Month Start"]
        month_label = mrow["Month Label"]
        mdf = monthly_base[monthly_base["Month Start"].eq(month_start)].copy()
        medf = mdf[mdf["Has Event"]].copy()

        completed = int(medf["Status Clean"].eq("Completed").sum())
        confirmed = int(medf["Status Clean"].eq("Confirmed").sum())
        planned = int(medf["Status Clean"].eq("Planned").sum())
        cancelled = int(medf["Status Clean"].eq("Cancelled").sum())

        month_totals.append({
            "Month": month_label,
            "Activities": int(len(mdf)),
            "Events": int(len(medf)),
            "Completed": completed,
            "Confirmed": confirmed,
            "Planned": planned,
            "Cancelled": cancelled,
            "Execution Ready": completed + confirmed,
        })

    month_totals_df = pd.DataFrame(month_totals)

    campus_perf_rows = []
    for campus in campuses:
        cdf = monthly_base[monthly_base["Campus"].eq(campus)].copy()
        event_cdf = cdf[cdf["Has Event"]].copy()
        completed = int(event_cdf["Status Clean"].eq("Completed").sum())
        events = int(len(event_cdf))

        campus_perf_rows.append({
            "Campus": campus,
            "Activities": int(len(cdf)),
            "Events": events,
            "Completed": completed,
            "Completion %": _monthly_safe_pct(completed, events),
        })

    campus_perf_df = pd.DataFrame(campus_perf_rows).sort_values(
        ["Activities", "Events"],
        ascending=False,
    ).reset_index(drop=True)

    total_activities_monthly = int(len(monthly_base))
    total_events_monthly = int(monthly_base["Has Event"].sum())
    event_only_all = monthly_base[monthly_base["Has Event"]].copy()
    total_completed = int(event_only_all["Status Clean"].eq("Completed").sum())
    total_confirmed = int(event_only_all["Status Clean"].eq("Confirmed").sum())
    total_planned = int(event_only_all["Status Clean"].eq("Planned").sum())
    total_cancelled = int(event_only_all["Status Clean"].eq("Cancelled").sum())

    best_month_activity = month_totals_df.sort_values(
        ["Activities", "Events"],
        ascending=False,
    ).iloc[0]
    best_month_execution = month_totals_df.sort_values(
        ["Execution Ready", "Completed"],
        ascending=False,
    ).iloc[0]

    leader_campus_row = campus_perf_df.iloc[0]
    leader_campus = str(leader_campus_row["Campus"])
    leader_activity_share = _monthly_safe_pct(
        leader_campus_row["Activities"],
        total_activities_monthly,
    )
    leader_event_share = _monthly_safe_pct(
        leader_campus_row["Events"],
        total_events_monthly,
    ) if total_events_monthly else 0.0

    valid_completion = campus_perf_df[campus_perf_df["Events"] > 0].copy()
    if valid_completion.empty:
        weaker_campus_text = "campuses with event activity"
    else:
        completion_median = valid_completion["Completion %"].median()
        weaker = valid_completion[valid_completion["Completion %"] < completion_median]
        weaker_campus_text = (
            ", ".join(weaker["Campus"].astype(str).tolist()[:2])
            if not weaker.empty
            else str(valid_completion.sort_values("Completion %").iloc[0]["Campus"])
        )

    first_month = str(months_order.iloc[0]["Month Label"])
    last_month = str(months_order.iloc[-1]["Month Label"])
    month_range = first_month if first_month == last_month else f"{first_month} – {last_month}"

    # -----------------------------
    # Build monthly HTML
    # -----------------------------
    table_html = [
        '<div class="monthly-summary-shell">',
        '<div class="monthly-summary-head">',
        '<div>',
        '<div class="monthly-summary-title">Monthly Campus-wise Activity &amp; Event Summary</div>',
        '<div class="monthly-summary-sub">Detailed count of activities, events and event status by campus and month.</div>',
        '</div>',
        f'<div class="monthly-range-chip">{html.escape(month_range)}</div>',
        '</div>',
        '<div class="monthly-table-wrap">',
        '<table class="monthly-table">',
        '<thead>',
        '<tr>',
        '<th class="ms-month-group" rowspan="2" style="min-width:68px;text-align:left;padding-left:8px;">Month</th>',
    ]

    for campus in campuses:
        table_html.append(
            f'<th class="ms-campus-group" colspan="6">{html.escape(str(campus))}</th>'
        )

    table_html.extend(['</tr>', '<tr>'])

    for _campus in campuses:
        table_html.extend([
            '<th class="ms-subhead ms-activities">Activities</th>',
            '<th class="ms-subhead ms-events">Events</th>',
            '<th class="ms-subhead ms-completed">Completed</th>',
            '<th class="ms-subhead ms-confirmed">Confirmed</th>',
            '<th class="ms-subhead ms-planned">Planned</th>',
            '<th class="ms-subhead ms-cancelled">Cancelled</th>',
        ])

    table_html.extend(['</tr>', '</thead>', '<tbody>'])

    for idx, row in enumerate(rows):
        is_total = idx == len(rows) - 1
        tr_class = ' class="ms-total-row"' if is_total else ""
        table_html.append(f'<tr{tr_class}>')
        table_html.append(
            f'<td class="ms-month-cell">{html.escape(str(row["Month"]))}</td>'
        )

        for campus in campuses:
            for metric in ["Activities", "Events", "Completed", "Confirmed", "Planned", "Cancelled"]:
                val = _monthly_num(row.get((campus, metric), 0))
                table_html.append(f'<td>{val}</td>')

        table_html.append('</tr>')

    table_html.extend(['</tbody>', '</table>', '</div>'])

    key_points = [
        f"{best_month_activity['Month']} has the highest activity volume ({_monthly_num(best_month_activity['Activities'])}) across all campuses.",
        f"Event execution (Completed + Confirmed) is strongest in {best_month_execution['Month']} ({_monthly_num(best_month_execution['Execution Ready'])} events).",
        f"{leader_campus} contributes the highest share of activities ({leader_activity_share:.1f}%) and events ({leader_event_share:.1f}%).",
        f"Focus on converting planned events, especially around {best_month_activity['Month']} and the current execution pipeline.",
    ]

    perf_html = [
        '<table class="monthly-perf-table">',
        '<thead><tr>',
        '<th style="width:26%;">Campus</th>',
        '<th style="width:14%;">Activities</th>',
        '<th style="width:12%;">Events</th>',
        '<th style="width:14%;">Completed</th>',
        '<th style="width:34%;">Completion %</th>',
        '</tr></thead><tbody>',
    ]

    for _, prow in campus_perf_df.iterrows():
        perf_html.extend([
            '<tr>',
            f'<td>{html.escape(str(prow["Campus"]))}</td>',
            f'<td>{_monthly_num(prow["Activities"])}</td>',
            f'<td>{_monthly_num(prow["Events"])}</td>',
            f'<td>{_monthly_num(prow["Completed"])}</td>',
            f'<td>{_monthly_perf_bar(prow["Completion %"])}</td>',
            '</tr>',
        ])

    total_completion_pct = _monthly_safe_pct(total_completed, total_events_monthly)
    perf_html.extend([
        '<tr>',
        '<td>Total</td>',
        f'<td>{total_activities_monthly}</td>',
        f'<td>{total_events_monthly}</td>',
        f'<td>{total_completed}</td>',
        f'<td>{_monthly_perf_bar(total_completion_pct)}</td>',
        '</tr>',
        '</tbody></table>',
    ])

    planned_share = _monthly_safe_pct(total_planned, total_events_monthly)
    actions = [
        f"Prioritize execution of {total_planned} planned events ({planned_share:.1f}% of total events).",
        f"Focus on improving completion rate in {weaker_campus_text}.",
        "Increase event outcomes in months with high activity volume but lower event conversion.",
        "Review the latest visible event pipeline to ensure timely execution.",
    ]

    table_html.append('<div class="monthly-panels">')

    # Key insights
    table_html.extend([
        '<div class="monthly-panel">',
        '<div class="monthly-panel-title">',
        '<span class="monthly-panel-icon monthly-icon-yellow">💡</span>',
        'Key Insights',
        '</div>',
    ])
    for i, text in enumerate(key_points, start=1):
        table_html.extend([
            '<div class="monthly-point">',
            f'<div class="monthly-point-badge">{i}</div>',
            f'<div class="monthly-point-text">{html.escape(text)}</div>',
            '</div>',
        ])
    table_html.append('</div>')

    # Campus performance
    table_html.extend([
        '<div class="monthly-panel">',
        '<div class="monthly-panel-title">',
        '<span class="monthly-panel-icon monthly-icon-blue">📊</span>',
        f'Campus Performance Total ({html.escape(month_range)})',
        '</div>',
        ''.join(perf_html),
        '</div>',
    ])

    # Recommended actions
    table_html.extend([
        '<div class="monthly-panel monthly-actions">',
        '<div class="monthly-panel-title">',
        '<span class="monthly-panel-icon monthly-icon-red">🎯</span>',
        'Recommended Actions',
        '</div>',
    ])
    for i, text in enumerate(actions, start=1):
        table_html.extend([
            '<div class="monthly-point">',
            f'<div class="monthly-point-badge">{i}</div>',
            f'<div class="monthly-point-text">{html.escape(text)}</div>',
            '</div>',
        ])
    table_html.extend(['</div>', '</div>', '</div>'])

    st.markdown(''.join(table_html), unsafe_allow_html=True)


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
