import html
import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from html import escape


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
    font-family: "Aptos", "Segoe UI", Arial, sans-serif;
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
    font-family: "Aptos", "Segoe UI", Arial, sans-serif;
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
KPI_ICONS = {
    "Total Activities": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11v2h4l7 4V7l-7 4H3z"/><path d="M18 8c1.5 1 2.3 2.3 2.3 4S19.5 15 18 16"/></svg>',
    "Total Events": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18M8 14h3M13 14h3"/></svg>',
    "Institutions": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V9l7-4 7 4v12M8 12h2M14 12h2M8 16h2M14 16h2"/></svg>',
    "Cities Covered": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-5.2 7-12a7 7 0 10-14 0c0 6.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.2"/></svg>',
    "Planned Reach": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20c0-4 2.5-7 6-7s6 3 6 7M14 14c3 0 6 2 6 6"/></svg>',
    "Actual Reach": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><path d="M12 12l7-7M16 5h3v3"/></svg>',
}

def professional_kpi(label, value, subtitle, icon, css_class):
    icon_html = KPI_ICONS.get(label, html.escape(str(icon)))
    st.markdown(
        (
            f'<div class="pro-kpi {css_class}">'
            f'<div class="kpi-icon-zone"><div class="icon">{icon_html}</div></div>'
            f'<div class="kpi-content">'
            f'<div class="value">{value}</div>'
            f'<div class="label">{html.escape(str(label))}</div>'
            f'<div class="sub">{html.escape(str(subtitle))}</div>'
            f'</div>'
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
            family="Aptos, Segoe UI, Arial, sans-serif",
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



def _ensure_filter_state(key, options):
    """Return a valid persisted selection for a custom filter."""
    options = list(options) if options else ["All"]
    current = st.session_state.get(key, "All")
    if current not in options:
        current = "All" if "All" in options else options[0]
        st.session_state[key] = current
    elif key not in st.session_state:
        st.session_state[key] = current
    return current


def _filter_label(label, css_class, svg_html):
    st.markdown(
        (
            f'<div class="cf-label {css_class}">'
            f'<span class="cf-icon">{svg_html}</span>'
            f'<span>{html.escape(label)}</span>'
            f'</div>'
        ),
        unsafe_allow_html=True,
    )


def _custom_select_filter(label, options, state_key, css_class, svg_html):
    """Professional popover selector while keeping normal Streamlit state."""
    options = list(options) if options else ["All"]
    current = _ensure_filter_state(state_key, options)

    _filter_label(label, css_class, svg_html)

    if hasattr(st, "popover"):
        with st.popover(str(current), use_container_width=True):
            st.markdown(
                f'<div class="cf-popover-title">{html.escape(label)}</div>'
                '<div class="cf-popover-sub">Choose one value to update the dashboard.</div>',
                unsafe_allow_html=True,
            )

            for idx, option in enumerate(options):
                option_text = str(option)
                selected = option_text == str(current)
                button_label = f"✓  {option_text}" if selected else option_text
                if st.button(
                    button_label,
                    key=f"{state_key}__option__{idx}",
                    width="stretch",
                    type="primary" if selected else "secondary",
                ):
                    st.session_state[state_key] = option
                    st.rerun()
    else:
        # Safe fallback for older Streamlit versions.
        current = st.selectbox(
            label,
            options,
            index=options.index(current),
            key=state_key,
            label_visibility="collapsed",
        )

    return st.session_state.get(state_key, current)


def _custom_date_filter(frame, column="Activity Date"):
    calendar_svg = (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="3" y="5" width="18" height="16" rx="2"/>'
        '<path d="M8 3v4M16 3v4M3 10h18"/></svg>'
    )
    _filter_label("Date Range", "cf-date", calendar_svg)

    if column not in frame.columns or not frame[column].notna().any():
        if hasattr(st, "popover"):
            with st.popover("No dates", use_container_width=True):
                st.caption("Activity Date is not available for this selection.")
        else:
            st.text_input("Date Range", value="", disabled=True, label_visibility="collapsed")
        return None

    min_date = frame[column].min().date()
    max_date = frame[column].max().date()

    current = st.session_state.get("ov_date")
    if not (
        isinstance(current, (list, tuple))
        and len(current) == 2
        and current[0] is not None
        and current[1] is not None
    ):
        current = (min_date, max_date)
        st.session_state["ov_date"] = current

    start_value, end_value = current[0], current[1]
    display = f"{pd.Timestamp(start_value).strftime('%Y/%m/%d')} — {pd.Timestamp(end_value).strftime('%Y/%m/%d')}"

    if hasattr(st, "popover"):
        with st.popover(display, use_container_width=True):
            st.markdown(
                '<div class="cf-popover-title">Date Range</div>'
                '<div class="cf-popover-sub">Select the outreach activity period.</div>',
                unsafe_allow_html=True,
            )

            if "ov_date_picker" not in st.session_state:
                st.session_state["ov_date_picker"] = current

            picked = st.date_input(
                "Select date range",
                value=st.session_state.get("ov_date_picker", current),
                min_value=min_date,
                max_value=max_date,
                key="ov_date_picker",
                label_visibility="collapsed",
            )

            if isinstance(picked, (list, tuple)) and len(picked) == 2:
                picked_tuple = (picked[0], picked[1])
                if tuple(current) != picked_tuple:
                    st.session_state["ov_date"] = picked_tuple
                    st.rerun()
    else:
        picked = st.date_input(
            "Date Range",
            value=current,
            min_value=min_date,
            max_value=max_date,
            key="ov_date_picker",
            label_visibility="collapsed",
        )
        if isinstance(picked, (list, tuple)) and len(picked) == 2:
            st.session_state["ov_date"] = (picked[0], picked[1])

    return st.session_state.get("ov_date", current)


# Inline vector icons for the custom filter labels.
FILTER_ICONS = {
    "campus": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h16M6 20V9l6-4 6 4v11M9 20v-5h6v5"/></svg>',
    "activity": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16M9 14h2M13 14h2"/></svg>',
    "event": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13l-7 7-9-9V4h7l9 9z"/><circle cx="8.5" cy="8.5" r="1.2"/></svg>',
    "status": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M8 12l2.5 2.5L16 9"/></svg>',
    "segment": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20c0-4 2.5-7 6-7s6 3 6 7M14 14c3 0 6 2 6 6"/></svg>',
    "owner": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.5 3.5-7 8-7s8 2.5 8 7"/></svg>',
    "priority": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.7 5.5 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1-4.4-4.3 6.1-.9L12 3z"/></svg>',
}

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
        "ov_date_picker",
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
# FINAL FILTER + KPI UI OVERRIDES
# =========================================================
st.markdown(
    """
    <style>
    /* ---------- FILTER DECK: compact, stable, colorful ---------- */
    .custom-filter-deck-marker { display:none !important; }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.custom-filter-deck-marker) {
        position:relative !important;
        overflow:visible !important;
        margin:.10rem 0 .48rem 0 !important;
        padding:.72rem .78rem .68rem .78rem !important;
        border:1px solid #DEE6F2 !important;
        border-radius:18px !important;
        background:
            radial-gradient(circle at 4% 20%, rgba(124,58,237,.055), transparent 22%),
            radial-gradient(circle at 96% 82%, rgba(37,99,235,.055), transparent 24%),
            linear-gradient(135deg,#FFFFFF 0%,#FBFCFF 58%,#F8F8FF 100%) !important;
        box-shadow:0 12px 30px rgba(25,52,92,.065), inset 0 1px 0 rgba(255,255,255,.96) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.custom-filter-deck-marker)::before {
        content:""; position:absolute; left:16px; right:16px; top:0; height:3px;
        border-radius:0 0 999px 999px;
        background:linear-gradient(90deg,#6D5DFB,#2F80ED,#18B99B,#F4A62A,#F05B7A);
        opacity:.90;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.custom-filter-deck-marker) div[data-testid="stHorizontalBlock"] {
        align-items:flex-end !important; gap:.55rem !important;
    }

    .cf-label {
        display:flex !important; align-items:center !important; gap:.38rem !important;
        min-height:27px !important; margin:0 0 .22rem .02rem !important;
        color:#173B67 !important; font-size:.70rem !important; font-weight:850 !important;
        line-height:1 !important; white-space:nowrap !important;
    }
    .cf-icon {
        width:25px !important; height:25px !important; min-width:25px !important;
        display:inline-flex !important; align-items:center !important; justify-content:center !important;
        border-radius:9px !important; border:1px solid currentColor !important;
        box-shadow:0 5px 12px rgba(29,58,105,.08) !important;
        overflow:hidden !important;
    }
    .cf-icon svg { width:14px !important; height:14px !important; min-width:14px !important; max-width:14px !important; display:block !important; }

    .cf-campus .cf-icon   { color:#7650E8 !important; background:#F4EFFF !important; }
    .cf-activity .cf-icon { color:#F07E1B !important; background:#FFF3E8 !important; }
    .cf-event .cf-icon    { color:#2B72EC !important; background:#EDF4FF !important; }
    .cf-status .cf-icon   { color:#18A45E !important; background:#ECFAF2 !important; }
    .cf-segment .cf-icon  { color:#9A46E9 !important; background:#F8EEFF !important; }
    .cf-owner .cf-icon    { color:#EE5076 !important; background:#FFF0F4 !important; }
    .cf-priority .cf-icon { color:#E8A016 !important; background:#FFF7E3 !important; }
    .cf-date .cf-icon     { color:#2563EB !important; background:#EEF4FF !important; }

    /* per-filter accent variables */
    div[data-testid="stColumn"]:has(.cf-campus)   { --fc:#7650E8; --fs:#F8F5FF; }
    div[data-testid="stColumn"]:has(.cf-activity) { --fc:#F07E1B; --fs:#FFF8F1; }
    div[data-testid="stColumn"]:has(.cf-event)    { --fc:#2B72EC; --fs:#F4F8FF; }
    div[data-testid="stColumn"]:has(.cf-status)   { --fc:#18A45E; --fs:#F3FCF7; }
    div[data-testid="stColumn"]:has(.cf-segment)  { --fc:#9A46E9; --fs:#FBF7FF; }
    div[data-testid="stColumn"]:has(.cf-owner)    { --fc:#EE5076; --fs:#FFF6F8; }
    div[data-testid="stColumn"]:has(.cf-priority) { --fc:#E8A016; --fs:#FFFAEF; }
    div[data-testid="stColumn"]:has(.cf-date)     { --fc:#2563EB; --fs:#F4F8FF; }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.custom-filter-deck-marker) div[data-testid="stPopover"] > button {
        width:100% !important; height:2.58rem !important; min-height:2.58rem !important;
        padding:0 .72rem !important; justify-content:space-between !important;
        border-radius:11px !important; border:1px solid #DCE5F1 !important;
        border-left:3px solid var(--fc,#4678E8) !important;
        background:linear-gradient(180deg,#FFFFFF 0%,var(--fs,#F7F9FD) 100%) !important;
        color:#173B67 !important; font-size:.74rem !important; font-weight:750 !important;
        box-shadow:0 4px 10px rgba(30,63,112,.045), inset 0 1px 0 rgba(255,255,255,.98) !important;
        transition:transform .17s ease,box-shadow .17s ease,border-color .17s ease !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.custom-filter-deck-marker) div[data-testid="stPopover"] > button:hover {
        transform:translateY(-2px) !important; border-color:var(--fc,#4678E8) !important;
        box-shadow:0 10px 20px rgba(28,64,120,.11), 0 0 0 2px color-mix(in srgb,var(--fc,#4678E8) 10%,transparent) !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.custom-filter-deck-marker) div[data-testid="stPopover"] > button p {
        color:#173B67 !important; font-weight:750 !important; white-space:nowrap !important; overflow:hidden !important; text-overflow:ellipsis !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.custom-filter-deck-marker) div[data-testid="stPopover"] > button svg {
        width:15px !important; height:15px !important; max-width:15px !important; color:var(--fc,#4678E8) !important; flex:0 0 15px !important;
    }

    .custom-filter-reset-spacer { height:1.54rem !important; }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.custom-filter-deck-marker) div[data-testid="stButton"] button {
        height:2.58rem !important; min-height:2.58rem !important; border-radius:11px !important;
        color:#FFFFFF !important; font-size:.72rem !important; font-weight:850 !important;
        border:1px solid rgba(38,64,130,.25) !important;
        background:linear-gradient(110deg,#0E4A82 0%,#245EB8 52%,#5947D9 112%) !important;
        box-shadow:0 8px 18px rgba(31,73,142,.20), inset 0 1px 0 rgba(255,255,255,.18) !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.custom-filter-deck-marker) div[data-testid="stButton"] button:hover {
        transform:translateY(-2px) !important; box-shadow:0 12px 24px rgba(31,73,142,.27) !important;
    }

    /* no helper/header strip in filter card */
    .custom-filter-deck-head,.custom-filter-foot { display:none !important; }

    /* ---------- KPI SNAPSHOT: no banner, only premium cards ---------- */
    .snapshot-banner { display:none !important; }
    .snapshot-motion-marker { display:none !important; }

    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) {
        position:relative !important; overflow:visible !important;
        margin:.02rem 0 .56rem 0 !important; padding:.50rem !important;
        border:1px solid #DFE7F2 !important; border-radius:18px !important;
        background:linear-gradient(135deg,#FFFFFF 0%,#FBFCFF 100%) !important;
        box-shadow:0 12px 30px rgba(25,53,95,.065) !important; gap:.52rem !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker)::before {
        content:"" !important; position:absolute !important; left:18px !important; right:18px !important; top:0 !important; height:3px !important;
        border-radius:0 0 999px 999px !important;
        background:linear-gradient(90deg,#2D6CDF,#16B7C8,#7950D8,#17A78B,#EAA126,#25A869) !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi {
        height:86px !important; min-height:86px !important; border-radius:15px !important;
        padding:.62rem .68rem !important; grid-template-columns:44px minmax(0,1fr) !important;
        grid-template-rows:29px 18px 16px !important; column-gap:.60rem !important;
        background:linear-gradient(135deg,#FFFFFF 0%,#FFFFFF 55%,var(--wash) 145%) !important;
        border:1px solid var(--border) !important;
        box-shadow:0 8px 18px rgba(27,53,91,.065), inset 0 1px 0 rgba(255,255,255,.96) !important;
        animation:kpiFinalFloat 5.5s ease-in-out infinite !important;
    }
    @keyframes kpiFinalFloat { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-1.5px)} }
    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi:hover {
        transform:translateY(-4px) scale(1.008) !important;
        box-shadow:0 15px 30px rgba(27,53,91,.12),0 0 0 1px var(--border) inset !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .icon {
        grid-column:1 !important; grid-row:1 / 4 !important; width:42px !important; height:42px !important;
        border-radius:13px !important; margin:0 !important; font-size:18px !important;
        background:linear-gradient(145deg,#FFFFFF 0%,var(--iconbg) 100%) !important;
        color:var(--accent) !important; border:1px solid var(--border) !important;
        box-shadow:0 7px 16px rgba(27,53,91,.08) !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .icon svg {
        width:22px !important; height:22px !important; max-width:22px !important; display:block !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .value {
        grid-column:2 !important; grid-row:1 !important; color:#0E315C !important; font-size:1.38rem !important; font-weight:950 !important; line-height:1 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .label {
        grid-column:2 !important; grid-row:2 !important; color:#294A70 !important; font-size:.55rem !important; font-weight:900 !important; text-transform:none !important; letter-spacing:0 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .sub {
        grid-column:2 !important; grid-row:3 !important; color:#8798AC !important; font-size:.43rem !important; line-height:1.08 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi::before {
        width:100% !important; height:3px !important; background:linear-gradient(90deg,var(--accent),var(--accent2),rgba(255,255,255,0)) !important;
    }

    @media (max-width:1200px) {
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.custom-filter-deck-marker) div[data-testid="stHorizontalBlock"] { overflow-x:auto !important; }
    }
    @media (prefers-reduced-motion:reduce) {
        div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi { animation:none !important; }
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
# FILTERS — CUSTOM PROFESSIONAL POPOVER CONTROLS
# Order locked: Campus → Activity Type → Event → Status →
# Target Segment → Owner → Priority → Date Range → Reset
# =========================================================

with st.container(border=True):
    st.markdown(
        '<span class="custom-filter-deck-marker"></span>',
        unsafe_allow_html=True,
    )

    filter_cols = st.columns(
        [0.90, 1.05, 0.84, 0.84, 1.08, 0.88, 0.78, 1.42, 0.82],
        gap="small",
    )

    with filter_cols[0]:
        campus_filter = _custom_select_filter(
            "Campus",
            _options(df, "Campus"),
            "ov_campus",
            "cf-campus",
            FILTER_ICONS["campus"],
        )

    with filter_cols[1]:
        activity_filter = _custom_select_filter(
            "Activity Type",
            _options(df, "Activity Type"),
            "ov_activity",
            "cf-activity",
            FILTER_ICONS["activity"],
        )

    with filter_cols[2]:
        event_filter = _custom_select_filter(
            "Event",
            _options(df, "Event"),
            "ov_event",
            "cf-event",
            FILTER_ICONS["event"],
        )

    with filter_cols[3]:
        status_filter = _custom_select_filter(
            "Status",
            _options(df, "Status"),
            "ov_status",
            "cf-status",
            FILTER_ICONS["status"],
        )

    with filter_cols[4]:
        segment_filter = _custom_select_filter(
            "Target Segment",
            _options(df, "Target Segment"),
            "ov_segment",
            "cf-segment",
            FILTER_ICONS["segment"],
        )

    with filter_cols[5]:
        owner_filter = _custom_select_filter(
            "Owner",
            _options(df, "Activity Owner"),
            "ov_owner",
            "cf-owner",
            FILTER_ICONS["owner"],
        )

    with filter_cols[6]:
        priority_filter = _custom_select_filter(
            "Priority",
            _options(df, "Priority"),
            "ov_priority",
            "cf-priority",
            FILTER_ICONS["priority"],
        )

    with filter_cols[7]:
        date_range = _custom_date_filter(df, "Activity Date")

    with filter_cols[8]:
        st.markdown(
            '<div class="custom-filter-reset-spacer"></div>',
            unsafe_allow_html=True,
        )
        if st.button("↻  Reset", width="stretch", key="ov_reset"):
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
# EXECUTIVE KPI SNAPSHOT
# =========================================================
k1, k2, k3, k4, k5, k6 = st.columns(6, gap="small")

with k1:
    st.markdown(
        '<span class="snapshot-motion-marker"></span>',
        unsafe_allow_html=True,
    )

    professional_kpi(
        "Total Activities",
        f"{total_activities:,}",
        "Filtered outreach activity volume",
        """<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.1' stroke-linecap='round' stroke-linejoin='round'><path d='M4 13v6M9 9v10M14 5v14M19 11v8'/></svg>""",
        "kpi-blue",
    )

with k2:
    professional_kpi(
        "Total Events",
        f"{total_events:,}",
        "Records with Event populated",
        """<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><rect x='4' y='5' width='16' height='15' rx='2'/><path d='M8 3v4M16 3v4M4 10h16'/></svg>""",
        "kpi-cyan",
    )

with k3:
    professional_kpi(
        "Institutions",
        f"{institutions:,}",
        "Unique institutions / event names",
        """<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M4 20h16M6 20V9l6-4 6 4v11M9 12h2M13 12h2M9 16h2M13 16h2'/></svg>""",
        "kpi-violet",
    )

with k4:
    professional_kpi(
        "Cities Covered",
        f"{cities:,}",
        "Current outreach footprint",
        """<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1 1 16 0Z'/><circle cx='12' cy='10' r='2.5'/></svg>""",
        "kpi-teal",
    )

with k5:
    professional_kpi(
        "Planned Reach",
        f"{planned_reach:,}",
        "Planned student / faculty reach",
        """<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='9' cy='8' r='3'/><circle cx='17' cy='9' r='2.5'/><path d='M3 20c0-4 2.5-7 6-7s6 3 6 7M14 14c3 0 6 2 6 6'/></svg>""",
        "kpi-amber",
    )

with k6:
    professional_kpi(
        "Actual Reach",
        f"{actual_reach:,}",
        f"{reach_achievement:.1f}% of planned reach" if planned_reach else "Actual reach entered",
        """<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.1' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='8'/><path d='m8.5 12 2.2 2.2 4.8-5'/></svg>""",
        "kpi-green",
    )


# =========================================================
# ACTIVITY TYPE × EVENT × CAMPUS STATUS MATRIX
# Professional campus-wise execution matrix shown directly
# below the Executive KPI cards and above the bubble matrix.
# =========================================================

def _aev_clean_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def _aev_clean_status(value):
    if pd.isna(value):
        return ""
    raw = str(value).strip()
    if not raw:
        return ""

    lookup = {
        "planned": "Planned",
        "plan": "Planned",
        "confirmed": "Confirmed",
        "confirm": "Confirmed",
        "completed": "Completed",
        "complete": "Completed",
        "cancelled": "Cancelled",
        "canceled": "Cancelled",
        "cancel": "Cancelled",
        "rescheduled": "Rescheduled",
        "reschedule": "Rescheduled",
    }
    return lookup.get(raw.lower(), raw.title())


def _aev_count_cell(value, status_name):
    value = int(value or 0)
    if value <= 0:
        return '<span class="aev-zero">—</span>'
    return (
        f'<span class="aev-count aev-count-{status_name.lower()}">'
        f'{value:,}'
        '</span>'
    )


def render_activity_event_status_matrix(matrix_df):
    required = {"Activity Type", "Event", "Campus", "Status"}
    missing = [column for column in required if column not in matrix_df.columns]
    if missing:
        st.info(
            "Activity Type × Event & Status Matrix cannot be shown because "
            f"these columns are unavailable: {', '.join(sorted(missing))}."
        )
        return

    source = matrix_df.copy()
    source["Activity Type"] = source["Activity Type"].apply(_aev_clean_text)
    source["Event"] = source["Event"].apply(_aev_clean_text)
    source["Campus"] = source["Campus"].apply(_aev_clean_text)
    source["Status"] = source["Status"].apply(_aev_clean_status)
    source = source[source["Activity Type"].ne("")].copy()

    if source.empty:
        return

    campus_order = ["Noida", "Lucknow", "Jaipur", "Indore"]
    visible_campuses = [c for c in campus_order if c in source["Campus"].unique().tolist()]
    extra_campuses = sorted([c for c in source["Campus"].unique().tolist() if c and c not in visible_campuses])
    campus_order = visible_campuses + extra_campuses
    status_order = ["Planned", "Confirmed", "Completed", "Cancelled", "Rescheduled"]

    preferred_activity_order = [
        "Campus Event",
        "Coaching Visit",
        "College Visit",
        "Education Fair",
        "Faculty Connect",
        "Mentor Visit",
        "Student Workshop",
    ]
    present_activities = source["Activity Type"].drop_duplicates().tolist()
    activity_order = [
        activity for activity in preferred_activity_order
        if activity in present_activities
    ] + sorted(
        activity for activity in present_activities
        if activity not in preferred_activity_order
    )

    source["Event Display"] = source["Event"].where(source["Event"].ne(""), "No Event")

    grouped = (
        source.groupby(
            ["Activity Type", "Event Display", "Campus", "Status"],
            observed=True,
            dropna=False,
        )
        .size()
        .reset_index(name="Count")
    )

    rows = []
    for activity in activity_order:
        activity_source = source[source["Activity Type"].eq(activity)].copy()
        activity_total = int(len(activity_source))

        event_summary = (
            activity_source.groupby("Event Display", observed=True, dropna=False)
            .size()
            .reset_index(name="Event Total")
            .sort_values(["Event Total", "Event Display"], ascending=[False, True])
        )

        for row_index, event_row in event_summary.reset_index(drop=True).iterrows():
            event_name = str(event_row["Event Display"])
            event_total = int(event_row["Event Total"])
            counts = {}

            for campus in campus_order:
                for status in status_order:
                    match = grouped[
                        grouped["Activity Type"].eq(activity)
                        & grouped["Event Display"].eq(event_name)
                        & grouped["Campus"].eq(campus)
                        & grouped["Status"].eq(status)
                    ]
                    counts[(campus, status)] = int(match["Count"].sum()) if not match.empty else 0

            rows.append({
                "activity": activity,
                "activity_total": activity_total,
                "event": event_name,
                "event_total": event_total,
                "show_activity": row_index == 0,
                "rowspan": int(len(event_summary)),
                "counts": counts,
            })

    total_records = int(len(source))
    unique_events = int(source.loc[source["Event"].ne(""), "Event"].nunique())

    campus_status = {}
    campus_perf_rows = []
    for campus in campus_order:
        cdf = source[source["Campus"].eq(campus)]
        total = int(len(cdf))
        planned = int(cdf["Status"].eq("Planned").sum())
        confirmed = int(cdf["Status"].eq("Confirmed").sum())
        completed = int(cdf["Status"].eq("Completed").sum())
        cancelled = int(cdf["Status"].eq("Cancelled").sum())
        rescheduled = int(cdf["Status"].eq("Rescheduled").sum())
        completion_pct = (completed / total * 100.0) if total else 0.0
        campus_status[campus] = {
            "Total": total,
            "Planned": planned,
            "Confirmed": confirmed,
            "Completed": completed,
            "Cancelled": cancelled,
            "Rescheduled": rescheduled,
        }
        campus_perf_rows.append({
            "Campus": campus,
            "Total": total,
            "Planned": planned,
            "Confirmed": confirmed,
            "Completed": completed,
            "Completion %": completion_pct,
        })

    campus_perf_df = pd.DataFrame(campus_perf_rows)
    leading_campus_row = campus_perf_df.sort_values(
        ["Total", "Completed", "Confirmed"], ascending=False
    ).iloc[0]
    leading_campus = str(leading_campus_row["Campus"])
    leading_campus_count = int(leading_campus_row["Total"])

    activity_totals = source.groupby("Activity Type", observed=True).size().sort_values(ascending=False)
    leading_activity = str(activity_totals.index[0]) if not activity_totals.empty else "—"
    leading_activity_count = int(activity_totals.iloc[0]) if not activity_totals.empty else 0

    status_totals = source.groupby("Status", observed=True).size()
    completed_count = int(status_totals.get("Completed", 0))
    confirmed_count = int(status_totals.get("Confirmed", 0))
    planned_count = int(status_totals.get("Planned", 0))
    cancelled_count = int(status_totals.get("Cancelled", 0))
    rescheduled_count = int(status_totals.get("Rescheduled", 0))
    ready_pipeline = confirmed_count + planned_count + rescheduled_count

    event_combo = (
        source[source["Event"].ne("")]
        .groupby(["Activity Type", "Event Display"], observed=True)
        .size()
        .sort_values(ascending=False)
    )
    if not event_combo.empty:
        top_activity_event = f"{event_combo.index[0][0]} · {event_combo.index[0][1]}"
        top_activity_event_count = int(event_combo.iloc[0])
    else:
        top_activity_event = "No tagged Event"
        top_activity_event_count = 0

    st.markdown(
        r"""
        <style>
        .aev-shell{position:relative;overflow:hidden;margin:.16rem 0 .68rem 0;border:1px solid #DCE6F2;border-radius:18px;background:linear-gradient(180deg,#FFFFFF 0%,#FBFCFF 100%);box-shadow:0 12px 30px rgba(22,47,83,.065),inset 0 1px 0 rgba(255,255,255,.96);}
        .aev-shell::before{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,#2D6CDF 0%,#6A67E8 34%,#F09D2B 68%,#1CA96E 100%);opacity:.92;z-index:4;}
        .aev-head{display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;padding:.78rem .92rem .64rem .92rem;border-bottom:1px solid #E7EDF5;background:linear-gradient(90deg,#FFFFFF 0%,#FCFDFF 64%,#FBF9FF 100%);}
        .aev-title{color:#16385F;font-size:1.02rem;font-weight:950;line-height:1.08;}
        .aev-sub{color:#7589A2;font-size:.58rem;line-height:1.38;margin-top:.13rem;max-width:760px;}
        .aev-head-badges{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:flex-end;}
        .aev-head-badge{display:inline-flex;align-items:center;gap:5px;padding:.28rem .48rem;border-radius:999px;border:1px solid #DCE5F1;background:#FFFFFF;color:#365574;font-size:.49rem;font-weight:900;box-shadow:0 4px 10px rgba(23,52,90,.04);white-space:nowrap;}
        .aev-head-badge::before{content:"";width:6px;height:6px;border-radius:50%;background:#3978ED;box-shadow:0 0 0 3px rgba(57,120,237,.10);}
        .aev-scroll{width:100%;overflow-x:auto;overflow-y:hidden;padding:.18rem .80rem .16rem .80rem;scrollbar-width:thin;scrollbar-color:#BFCDE0 #F1F5FA;}
        .aev-table{width:100%;min-width:1330px;border-collapse:separate;border-spacing:0;table-layout:fixed;color:#274766;background:#FFFFFF;border:1px solid #DCE6F1;border-radius:14px;overflow:hidden;font-family:"Aptos", "Segoe UI", Arial, sans-serif;}
        .aev-table th,.aev-table td{border-right:1px solid #E1E8F1;border-bottom:1px solid #E7EDF4;text-align:center;vertical-align:middle;}
        .aev-table th:last-child,.aev-table td:last-child{border-right:none;}
        .aev-left-head{background:linear-gradient(180deg,#EEF4FB 0%,#E8F0F9 100%);color:#17375E;font-size:.56rem;font-weight:950;padding:.48rem .36rem;text-align:left!important;}
        .aev-campus-head{background:linear-gradient(180deg,#EEF4FB 0%,#E6EFF9 100%);color:#193A64;font-size:.64rem;font-weight:950;padding:.46rem .16rem;letter-spacing:.01em;}
        .aev-status-head{color:#FFFFFF;font-size:.43rem;font-weight:950;padding:.32rem .06rem;line-height:1.05;white-space:nowrap;}
        .aev-status-head.planned{background:#8DBFE3;color:#FFFFFF;}
        .aev-status-head.confirmed{background:#3776C5;}
        .aev-status-head.completed{background:#2C9B63;}
        .aev-status-head.cancelled{background:#EE5B57;}
        .aev-status-head.rescheduled{background:#E6A53A;color:#FFFFFF;}
        .aev-activity-cell{width:160px;padding:.44rem .45rem!important;text-align:left!important;color:#15395F;font-size:.58rem;font-weight:900;line-height:1.25;white-space:normal;word-break:normal;overflow-wrap:break-word;background:linear-gradient(180deg,#F7FBFF 0%,#F1F6FC 100%)!important;}
        .aev-activity-wrap{display:flex;align-items:flex-start;justify-content:space-between;gap:.35rem;}
        .aev-activity-name{display:block;flex:1;min-width:0;}
        .aev-activity-count{display:inline-flex;align-items:center;justify-content:center;min-width:22px;height:18px;padding:0 .24rem;border-radius:999px;color:#285A8D;background:#E5F0FB;border:1px solid #D1E2F3;font-size:.44rem;font-weight:950;flex:0 0 auto;}
        .aev-event-cell{width:142px;padding:.35rem .34rem!important;text-align:left!important;background:#FFFFFF;white-space:normal;}
        .aev-event-wrap{display:flex;align-items:flex-start;justify-content:space-between;gap:.30rem;}
        .aev-event-main{color:#294B6F;font-size:.54rem;font-weight:820;line-height:1.22;display:block;word-break:break-word;}
        .aev-event-main.no-event{color:#6B7F95;font-style:italic;}
        .aev-event-count{display:inline-flex;align-items:center;justify-content:center;min-width:18px;height:16px;padding:0 .18rem;border-radius:999px;color:#6A7F97;background:#F1F5F9;border:1px solid #DFE7F0;font-size:.42rem;font-weight:900;flex:0 0 auto;}
        .aev-data-cell{width:58px;height:34px;padding:.28rem .06rem!important;background:#FFFFFF;font-size:.50rem;}
        .aev-table tbody tr:nth-child(even) td:not(.aev-activity-cell){background:#FBFCFE;}
        .aev-table tbody tr:hover td:not(.aev-activity-cell){background:#F4F8FE;}
        .aev-zero{color:#C4CFDB;font-weight:700;}
        .aev-count{display:inline-flex;align-items:center;justify-content:center;min-width:25px;height:20px;padding:0 .18rem;border-radius:6px;font-size:.47rem;font-weight:950;font-variant-numeric:tabular-nums;box-shadow:inset 0 1px 0 rgba(255,255,255,.75);}
        .aev-count-planned{color:#245E91;background:#DCEEFF;border:1px solid #C8E1F7;}
        .aev-count-confirmed{color:#FFFFFF;background:#3B79C8;border:1px solid #3470BA;}
        .aev-count-completed{color:#FFFFFF;background:#2EA069;border:1px solid #29945F;}
        .aev-count-cancelled{color:#FFFFFF;background:#EF625D;border:1px solid #E15752;}
        .aev-count-rescheduled{color:#7C5205;background:#FFE7B7;border:1px solid #F0D295;}
        .aev-total-row td{background:linear-gradient(180deg,#FFF9E9 0%,#FFF4D8 100%)!important;color:#153A5F;font-weight:950;border-top:1px solid #ECD9A8;font-size:.57rem;line-height:1.08;padding:.38rem .07rem!important;}
        .aev-total-label{text-align:left!important;padding:.39rem .50rem!important;font-size:.59rem!important;font-weight:950!important;}
        .aev-intel-panel{margin:.72rem .80rem .86rem .80rem;padding:.94rem .96rem .90rem .96rem;border:1px solid #D7E3F0;border-radius:18px;background:radial-gradient(circle at 96% 6%,rgba(45,108,223,.085),transparent 24%),radial-gradient(circle at 5% 96%,rgba(28,169,110,.060),transparent 25%),linear-gradient(135deg,#F8FBFF 0%,#FFFFFF 52%,#FBF9FF 100%);box-shadow:0 13px 30px rgba(22,49,88,.075),inset 0 1px 0 rgba(255,255,255,.97);position:relative;overflow:hidden;}
        .aev-intel-panel::before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:linear-gradient(180deg,#2D6CDF 0%,#7156D9 48%,#1CA96E 100%);}
        .aev-intel-panel::after{content:"";position:absolute;left:18px;right:18px;top:0;height:3px;background:linear-gradient(90deg,#2D6CDF 0%,#7554D8 38%,#F0A12A 68%,#1CA96E 100%);border-radius:0 0 999px 999px;opacity:.88;}
        .aev-intel-head{display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;margin-bottom:.78rem;padding-left:.10rem;position:relative;z-index:1;}
        .aev-intel-kicker{color:#2D6CDF;font-size:.48rem;font-weight:950;letter-spacing:.10em;text-transform:uppercase;margin-bottom:.12rem;}
        .aev-intel-title{color:#12365F;font-size:1.02rem;font-weight:950;line-height:1.10;letter-spacing:-.018em;}
        .aev-intel-sub{color:#72869F;font-size:.59rem;line-height:1.42;margin-top:.13rem;max-width:820px;}
        .aev-intel-tag{display:inline-flex;align-items:center;gap:6px;padding:.31rem .55rem;border-radius:999px;background:linear-gradient(135deg,#EEF5FF,#F6F2FF);border:1px solid #D8E4F4;color:#2D64A4;font-size:.50rem;font-weight:900;white-space:nowrap;box-shadow:0 4px 11px rgba(37,99,235,.055);}
        .aev-intel-tag::before{content:"";width:6px;height:6px;border-radius:50%;background:#2F80ED;box-shadow:0 0 0 3px rgba(47,128,237,.10);}
        .aev-command-grid{display:grid;grid-template-columns:1.18fr .96fr .96fr;gap:12px;position:relative;z-index:1;}
        .aev-command-card{position:relative;overflow:hidden;min-height:156px;padding:.78rem .82rem .74rem .82rem;border-radius:15px;background:linear-gradient(180deg,#FFFFFF 0%,#FBFCFF 100%);border:1px solid #DDE6F1;box-shadow:0 7px 18px rgba(22,49,88,.05),inset 0 1px 0 rgba(255,255,255,.96);transition:transform .18s ease,box-shadow .18s ease;}
        .aev-command-card:hover{transform:translateY(-2px);box-shadow:0 12px 25px rgba(22,49,88,.085),inset 0 1px 0 rgba(255,255,255,.96);}
        .aev-command-card.hero{background:radial-gradient(circle at 92% 12%,rgba(45,108,223,.10),transparent 28%),linear-gradient(145deg,#F7FBFF,#FFFFFF 65%);border-color:#CBDDF5;}
        .aev-command-card.hero::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:#2D6CDF;}
        .aev-command-card.health::before,.aev-command-card.momentum::before{content:"";position:absolute;left:0;right:0;top:0;height:3px;}
        .aev-command-card.health::before{background:linear-gradient(90deg,#1CA96E,#4CCB8A);}
        .aev-command-card.momentum::before{background:linear-gradient(90deg,#7554D8,#A17BEA);}
        .aev-command-label{color:#72859A;font-size:.48rem;font-weight:950;letter-spacing:.075em;text-transform:uppercase;}
        .aev-command-value{color:#12385F;font-size:1.34rem;font-weight:950;line-height:1.02;margin-top:.18rem;letter-spacing:-.025em;}
        .aev-command-value.small{font-size:1.06rem;line-height:1.08;}
        .aev-command-note{color:#71869D;font-size:.53rem;line-height:1.38;margin-top:.13rem;}
        .aev-command-callout{display:inline-flex;align-items:center;gap:5px;margin-top:.48rem;padding:.24rem .40rem;border-radius:8px;background:#EEF5FF;border:1px solid #D7E7FA;color:#2B5F96;font-size:.48rem;font-weight:900;}
        .aev-mini-status-row{display:flex;gap:6px;flex-wrap:wrap;margin-top:.50rem;}
        .aev-mini-status{display:inline-flex;align-items:center;gap:4px;padding:.23rem .38rem;border-radius:8px;background:#F7F9FC;border:1px solid #E2E9F2;color:#567089;font-size:.46rem;font-weight:850;}
        .aev-mini-status strong{color:#173F67;font-size:.49rem;font-weight:950;}
        .aev-health-track{height:10px;border-radius:999px;background:#E8EEF5;overflow:hidden;margin-top:.50rem;box-shadow:inset 0 1px 2px rgba(18,56,95,.05);}
        .aev-health-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#1CA96E,#55CD91);}
        .aev-health-row{display:flex;justify-content:space-between;align-items:center;gap:.5rem;margin-top:.36rem;color:#70849B;font-size:.47rem;}
        .aev-health-row strong{color:#1B7550;font-size:.50rem;font-weight:950;}
        .aev-campus-stack{display:grid;gap:5px;margin-top:.48rem;}
        .aev-campus-line{display:grid;grid-template-columns:58px 1fr 31px;gap:6px;align-items:center;color:#536E89;font-size:.46rem;font-weight:850;}
        .aev-campus-line-track{height:7px;border-radius:999px;background:#E9EEF5;overflow:hidden;}
        .aev-campus-line-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#7554D8,#9A78E4);}
        .aev-campus-line-pct{text-align:right;color:#5E4BB8;font-weight:950;font-size:.47rem;}
        .aev-action-queue{margin-top:.70rem;padding-top:.66rem;border-top:1px solid #E2EAF3;position:relative;z-index:1;}
        .aev-action-head{display:flex;align-items:center;justify-content:space-between;gap:.7rem;margin-bottom:.42rem;}
        .aev-action-title{color:#173A60;font-size:.66rem;font-weight:950;}
        .aev-action-caption{color:#7B8EA4;font-size:.48rem;}
        .aev-action-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;}
        .aev-action-item{display:grid;grid-template-columns:28px 1fr;gap:.45rem;align-items:start;padding:.50rem .55rem;border-radius:11px;background:#FFFFFF;border:1px solid #DEE7F1;box-shadow:0 3px 9px rgba(22,49,88,.025);}
        .aev-action-no{width:28px;height:28px;border-radius:9px;display:flex;align-items:center;justify-content:center;background:linear-gradient(145deg,#2D6CDF,#5B59D7);color:#FFFFFF;font-size:.48rem;font-weight:950;box-shadow:0 5px 11px rgba(50,77,189,.18);}
        .aev-action-item:nth-child(2) .aev-action-no{background:linear-gradient(145deg,#E39A24,#F0B64A);}
        .aev-action-item:nth-child(3) .aev-action-no{background:linear-gradient(145deg,#D94E62,#ED7483);}
        .aev-action-item-title{color:#244A70;font-size:.52rem;font-weight:950;line-height:1.18;}
        .aev-action-item-text{color:#73879D;font-size:.47rem;line-height:1.36;margin-top:.08rem;}
        @media(max-width:1100px){.aev-head{flex-direction:column;align-items:flex-start;}.aev-head-badges{justify-content:flex-start;}.aev-command-grid{grid-template-columns:1fr 1fr;}.aev-command-card.hero{grid-column:1/-1;}.aev-action-grid{grid-template-columns:1fr;}}
        @media(max-width:720px){.aev-command-grid{grid-template-columns:1fr;}.aev-command-card.hero{grid-column:auto;}}
        </style>
        """,
        unsafe_allow_html=True,
    )

    parts = [
        '<div class="aev-shell">', '<div class="aev-head">', '<div>',
        '<div class="aev-title">Activity Type – Event &amp; Status Matrix</div>',
        '<div class="aev-sub">Campus-wise activity, event and execution status in one clean operational view. The layout is optimized for dashboard readability and horizontal scan.</div>',
        '</div>', '<div class="aev-head-badges">',
        f'<span class="aev-head-badge">{total_records:,} records</span>',
        f'<span class="aev-head-badge">{len(activity_order):,} activity types</span>',
        f'<span class="aev-head-badge">{unique_events:,} event types</span>',
        '</div>', '</div>', '<div class="aev-scroll">', '<table class="aev-table">', '<colgroup>',
        '<col style="width:160px">', '<col style="width:142px">',
        *['<col style="width:58px">' for _ in range(len(campus_order) * len(status_order))],
        '</colgroup>', '<thead><tr>', '<th class="aev-left-head" rowspan="2">Activity Type</th>', '<th class="aev-left-head" rowspan="2">Event</th>',
    ]

    for campus in campus_order:
        parts.append(f'<th class="aev-campus-head" colspan="{len(status_order)}">{escape(campus)}</th>')

    parts.append('</tr><tr>')
    for _campus in campus_order:
        for status in status_order:
            parts.append(f'<th class="aev-status-head {status.lower()}">{escape(status)}</th>')
    parts.append('</tr></thead><tbody>')

    for row in rows:
        parts.append('<tr>')
        if row["show_activity"]:
            parts.append(
                f'<td class="aev-activity-cell" rowspan="{row["rowspan"]}"><div class="aev-activity-wrap"><span class="aev-activity-name">{escape(row["activity"])}</span><span class="aev-activity-count">{row["activity_total"]:,}</span></div></td>'
            )

        event_class = 'aev-event-main no-event' if str(row["event"]).strip().lower() == 'no event' else 'aev-event-main'
        parts.append(
            f'<td class="aev-event-cell"><div class="aev-event-wrap"><span class="{event_class}">{escape(row["event"])}</span><span class="aev-event-count">{row["event_total"]:,}</span></div></td>'
        )

        for campus in campus_order:
            for status in status_order:
                parts.append('<td class="aev-data-cell">' + _aev_count_cell(row["counts"].get((campus, status), 0), status) + '</td>')
        parts.append('</tr>')

    parts.append('<tr class="aev-total-row">')
    parts.append('<td class="aev-total-label" colspan="2">Total</td>')
    for campus in campus_order:
        for status in status_order:
            parts.append(f'<td>{int(campus_status[campus][status]):,}</td>')
    parts.append('</tr>')
    parts.extend(['</tbody></table></div>'])

    total_activity_share = (leading_campus_count / total_records * 100.0) if total_records else 0.0
    overall_completion = (completed_count / total_records * 100.0) if total_records else 0.0

    key_points = [
        f'{leading_campus} has the highest current activity volume ({leading_campus_count:,}; {total_activity_share:.1f}% of records).',
        f'{leading_activity} is the leading activity type with {leading_activity_count:,} records.',
        f'{top_activity_event} is the strongest tagged event combination ({top_activity_event_count:,} records).',
        f'{ready_pipeline:,} records are currently in planned / confirmed / rescheduled execution pipeline.',
    ]
    action_points = [
        f'Convert the {ready_pipeline:,} ready-pipeline records into completed execution.',
        f'Prioritize follow-up in {leading_campus}, the highest-volume campus in the current selection.',
        f'Review {planned_count:,} planned and {confirmed_count:,} confirmed records for ownership and event readiness.',
        f'Address {cancelled_count:,} cancelled and {rescheduled_count:,} rescheduled records before adding avoidable new volume.',
    ]

    pipeline_pct = (ready_pipeline / total_records * 100.0) if total_records else 0.0
    strongest_completion_row = campus_perf_df[campus_perf_df["Total"] > 0].sort_values(
        ["Completion %", "Completed", "Total"], ascending=False
    ).iloc[0]
    strongest_completion_campus = str(strongest_completion_row["Campus"])
    strongest_completion_pct = float(strongest_completion_row["Completion %"])

    pipeline_by_campus = []
    for campus in campus_order:
        c = campus_status[campus]
        pending = int(c["Planned"] + c["Confirmed"] + c["Rescheduled"])
        pipeline_by_campus.append((campus, pending))
    pipeline_by_campus.sort(key=lambda x: x[1], reverse=True)
    focus_campus, focus_pipeline = pipeline_by_campus[0] if pipeline_by_campus else (leading_campus, 0)
    exception_count = cancelled_count + rescheduled_count

    parts.append('<div class="aev-intel-panel">')
    parts.append(
        '<div class="aev-intel-head">'
        '<div><div class="aev-intel-kicker">Management View</div>'
        '<div class="aev-intel-title">Execution Command Center</div>'
        '<div class="aev-intel-sub">A focused read of conversion opportunity, execution health and campus momentum from the current filtered portfolio.</div></div>'
        '<span class="aev-intel-tag">Live filtered view</span>'
        '</div>'
    )

    parts.append('<div class="aev-command-grid">')
    parts.append(
        '<div class="aev-command-card hero">'
        '<div class="aev-command-label">Conversion Opportunity</div>'
        f'<div class="aev-command-value">{ready_pipeline:,} <span style="font-size:.62rem;color:#6C8198;font-weight:850;">records</span></div>'
        f'<div class="aev-command-note">{pipeline_pct:.1f}% of the current portfolio is still in an executable pipeline and can move toward completion.</div>'
        f'<div class="aev-command-callout">Highest open pipeline: {escape(focus_campus)} · {focus_pipeline:,}</div>'
        '<div class="aev-mini-status-row">'
        f'<span class="aev-mini-status">Planned <strong>{planned_count:,}</strong></span>'
        f'<span class="aev-mini-status">Confirmed <strong>{confirmed_count:,}</strong></span>'
        f'<span class="aev-mini-status">Rescheduled <strong>{rescheduled_count:,}</strong></span>'
        '</div></div>'
    )

    parts.append(
        '<div class="aev-command-card health">'
        '<div class="aev-command-label">Execution Health</div>'
        f'<div class="aev-command-value">{overall_completion:.0f}%</div>'
        f'<div class="aev-command-note">{completed_count:,} of {total_records:,} records are completed in the current view.</div>'
        '<div class="aev-health-track">'
        f'<div class="aev-health-fill" style="width:{max(0.0,min(100.0,overall_completion)):.1f}%"></div>'
        '</div>'
        f'<div class="aev-health-row"><span>Completed <strong>{completed_count:,}</strong></span><span>Exceptions <strong>{exception_count:,}</strong></span></div>'
        '</div>'
    )

    parts.append('<div class="aev-command-card momentum">')
    parts.append('<div class="aev-command-label">Campus Momentum</div>')
    parts.append(f'<div class="aev-command-value small">{escape(strongest_completion_campus)} · {strongest_completion_pct:.0f}%</div>')
    parts.append(f'<div class="aev-command-note">Strongest completion rate. Volume leader: {escape(leading_campus)} with {leading_campus_count:,} records.</div>')
    parts.append('<div class="aev-campus-stack">')
    for _, perf in campus_perf_df.iterrows():
        pct = max(0.0, min(100.0, float(perf["Completion %"])))
        parts.append(
            '<div class="aev-campus-line">'
            f'<span>{escape(str(perf["Campus"]))}</span>'
            '<span class="aev-campus-line-track">'
            f'<span class="aev-campus-line-fill" style="display:block;width:{pct:.1f}%"></span>'
            '</span>'
            f'<span class="aev-campus-line-pct">{pct:.0f}%</span>'
            '</div>'
        )
    parts.append('</div></div>')
    parts.append('</div>')

    parts.append('<div class="aev-action-queue">')
    parts.append(
        '<div class="aev-action-head">'
        '<div class="aev-action-title">Priority Action Queue</div>'
        '<div class="aev-action-caption">Next best operational moves from this matrix</div>'
        '</div>'
    )
    parts.append('<div class="aev-action-grid">')
    parts.append(
        '<div class="aev-action-item"><span class="aev-action-no">01</span><div>'
        '<div class="aev-action-item-title">Move confirmed activity to execution</div>'
        f'<div class="aev-action-item-text">Work the {confirmed_count:,} confirmed records first; they are closest to completion.</div>'
        '</div></div>'
    )
    parts.append(
        '<div class="aev-action-item"><span class="aev-action-no">02</span><div>'
        f'<div class="aev-action-item-title">Focus {escape(focus_campus)} pipeline</div>'
        f'<div class="aev-action-item-text">{focus_pipeline:,} open records sit in the largest campus pipeline; assign ownership and dates.</div>'
        '</div></div>'
    )
    parts.append(
        '<div class="aev-action-item"><span class="aev-action-no">03</span><div>'
        '<div class="aev-action-item-title">Clear execution exceptions</div>'
        f'<div class="aev-action-item-text">Review {cancelled_count:,} cancelled and {rescheduled_count:,} rescheduled records before adding avoidable new volume.</div>'
        '</div></div>'
    )
    parts.append('</div></div>')
    parts.append('</div></div>')
    st.markdown(''.join(parts), unsafe_allow_html=True)

# Render immediately below the Total Activity / KPI cards.
render_activity_event_status_matrix(filtered)


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
    campus_order = campus_totals_activity.index.tolist()
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
                        event_size = 18 + (math.sqrt(event_count / max_event_count) * 15)
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

                size_px = 22 + (math.sqrt(total_count / max_count) * 38)
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
# CAMPUS EVENT / MONTHLY SUMMARY SECTIONS REMOVED
# Per final Overview layout, the dashboard now continues
# directly from the Activity Type × Campus Matrix to Reach Performance.
# =========================================================

# =========================================================
# REACH PERFORMANCE
# =========================================================
overview_section(
    "Reach Performance",
    "Campus Planned vs Actual Reach",
    "A compact execution view compares planned reach with delivered reach and surfaces the campuses requiring management attention.",
)

st.markdown(
    r"""
    <style>
    .reach-chart-marker,
    .reach-insight-marker { display:none !important; }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.reach-chart-marker),
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.reach-insight-marker) {
        position:relative !important;
        overflow:hidden !important;
        min-height:410px !important;
        height:410px !important;
        padding:.82rem .88rem .64rem .88rem !important;
        border:1px solid #DCE6F1 !important;
        border-radius:18px !important;
        background:linear-gradient(180deg,#FFFFFF 0%,#FBFCFF 100%) !important;
        box-shadow:0 12px 28px rgba(22,49,88,.060), inset 0 1px 0 rgba(255,255,255,.96) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.reach-chart-marker)::before,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.reach-insight-marker)::before {
        content:"";
        position:absolute;
        left:0; right:0; top:0;
        height:3px;
        background:linear-gradient(90deg,#2D6CDF,#6A67E8,#19A38D,#F0A12B);
        z-index:4;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.reach-chart-marker) .js-plotly-plot,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.reach-chart-marker) [data-testid="stPlotlyChart"] {
        width:100% !important;
    }

    .reach-card-head {
        display:flex;
        align-items:flex-start;
        justify-content:space-between;
        gap:.8rem;
        margin-bottom:.12rem;
    }
    .reach-card-head-compact {
        justify-content:flex-end;
        min-height:22px;
        margin-bottom:-.22rem;
    }
    .reach-card-kicker {
        color:#6E55C7;
        font-size:.50rem;
        font-weight:950;
        letter-spacing:.11em;
        text-transform:uppercase;
    }
    .reach-card-title {
        color:#17395F;
        font-size:1.01rem;
        font-weight:950;
        line-height:1.12;
        margin-top:.08rem;
    }
    .reach-card-sub {
        color:#7A8EA4;
        font-size:.56rem;
        line-height:1.36;
        margin-top:.12rem;
    }
    .reach-live-pill {
        flex:0 0 auto;
        display:inline-flex;
        align-items:center;
        gap:5px;
        padding:.25rem .45rem;
        border-radius:999px;
        border:1px solid #D8E5F2;
        background:#F8FBFF;
        color:#486985;
        font-size:.45rem;
        font-weight:900;
        white-space:nowrap;
    }
    .reach-live-pill::before {
        content:"";
        width:6px;
        height:6px;
        border-radius:50%;
        background:#18A36F;
        box-shadow:0 0 0 3px rgba(24,163,111,.10);
    }

    .reach-intel {
        height:100%;
        display:flex;
        flex-direction:column;
    }
    .reach-intel-top {
        display:flex;
        align-items:flex-start;
        justify-content:space-between;
        gap:.65rem;
        margin-bottom:.58rem;
    }
    .reach-intel-title {
        color:#17395F;
        font-size:1.00rem;
        font-weight:950;
        line-height:1.12;
    }
    .reach-intel-sub {
        color:#7A8EA4;
        font-size:.54rem;
        line-height:1.34;
        margin-top:.11rem;
    }
    .reach-health-badge {
        flex:0 0 auto;
        padding:.23rem .42rem;
        border-radius:999px;
        font-size:.44rem;
        font-weight:950;
        border:1px solid #E0E7F0;
        background:#FFFFFF;
        color:#526B84;
        box-shadow:0 3px 10px rgba(22,49,88,.035);
    }

    .reach-kpi-grid {
        display:grid;
        grid-template-columns:1fr 1fr;
        gap:8px;
        margin-bottom:.55rem;
    }
    .reach-kpi {
        position:relative;
        overflow:hidden;
        min-height:76px;
        padding:.52rem .56rem .47rem .56rem;
        border:1px solid #E0E7F0;
        border-radius:13px;
        background:#FFFFFF;
        box-shadow:0 5px 14px rgba(22,49,88,.035);
    }
    .reach-kpi::before {
        content:"";
        position:absolute;
        left:0; top:0; bottom:0;
        width:3px;
        background:var(--reach-accent,#2D6CDF);
    }
    .reach-kpi-label {
        color:#7B8DA3;
        font-size:.43rem;
        font-weight:950;
        letter-spacing:.065em;
        text-transform:uppercase;
    }
    .reach-kpi-value {
        color:#17395F;
        font-size:.91rem;
        font-weight:950;
        line-height:1.05;
        margin-top:.13rem;
    }
    .reach-kpi-note {
        color:#7F91A5;
        font-size:.44rem;
        line-height:1.28;
        margin-top:.12rem;
    }

    .reach-readout {
        flex:1;
        padding:.56rem .60rem;
        border:1px solid #DDE8F2;
        border-radius:13px;
        background:linear-gradient(135deg,#F8FBFF 0%,#FFFFFF 100%);
    }
    .reach-readout-title {
        display:flex;
        align-items:center;
        gap:.35rem;
        color:#21466B;
        font-size:.58rem;
        font-weight:950;
        margin-bottom:.42rem;
    }
    .reach-readout-title::before {
        content:"";
        width:7px;
        height:7px;
        border-radius:50%;
        background:#2D6CDF;
        box-shadow:0 0 0 3px rgba(45,108,223,.10);
    }
    .reach-signal {
        display:grid;
        grid-template-columns:22px 1fr;
        gap:.36rem;
        align-items:start;
        margin-bottom:.38rem;
    }
    .reach-signal:last-child { margin-bottom:0; }
    .reach-signal-num {
        width:20px;
        height:20px;
        border-radius:7px;
        display:flex;
        align-items:center;
        justify-content:center;
        background:#EAF2FF;
        color:#2D6CDF;
        font-size:.46rem;
        font-weight:950;
    }
    .reach-signal-text {
        color:#5E748C;
        font-size:.49rem;
        line-height:1.36;
    }
    .reach-signal-text strong { color:#244A70; font-weight:950; }

    .reach-action {
        margin-top:.50rem;
        padding:.49rem .55rem;
        border:1px solid #F1D7A2;
        border-left:4px solid #E9A11B;
        border-radius:11px;
        background:linear-gradient(90deg,#FFF9EB 0%,#FFFDF7 100%);
        color:#64758A;
        font-size:.48rem;
        line-height:1.34;
    }
    .reach-action strong { color:#805D13; font-weight:950; }

    @media(max-width:1100px){
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.reach-chart-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.reach-insight-marker) {
            min-height:auto !important;
            height:auto !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

reach_data = pd.DataFrame()
if "Campus" in filtered.columns:
    reach_base = filtered.copy()
    reach_base["Planned Student Reach"] = pd.to_numeric(
        reach_base["Planned Student Reach"], errors="coerce"
    )
    reach_base["Actual Student Reach"] = pd.to_numeric(
        reach_base["Actual Student Reach"], errors="coerce"
    )

    reach_data = (
        reach_base.groupby("Campus", observed=True)[
            ["Planned Student Reach", "Actual Student Reach"]
        ]
        .sum(min_count=1)
        .reset_index()
        .rename(
            columns={
                "Planned Student Reach": "Planned Reach",
                "Actual Student Reach": "Actual Reach",
            }
        )
    )
    reach_data = reach_data[
        reach_data[["Planned Reach", "Actual Reach"]].notna().any(axis=1)
    ].copy()
    reach_data[["Planned Reach", "Actual Reach"]] = reach_data[
        ["Planned Reach", "Actual Reach"]
    ].fillna(0)
    reach_data["Achievement %"] = reach_data.apply(
        lambda r: _pct(r["Actual Reach"], r["Planned Reach"]), axis=1
    )
    reach_data["Gap"] = (
        reach_data["Planned Reach"] - reach_data["Actual Reach"]
    ).clip(lower=0)
    reach_data = reach_data.sort_values(
        ["Planned Reach", "Actual Reach"], ascending=False
    ).reset_index(drop=True)

if reach_data.empty or reach_data[["Planned Reach", "Actual Reach"]].sum().sum() == 0:
    st.info("No Planned/Actual Reach values are available for the selected filters.")
else:
    overall_planned = float(reach_data["Planned Reach"].sum())
    overall_actual = float(reach_data["Actual Reach"].sum())
    overall_pct = _pct(overall_actual, overall_planned)
    overall_gap = max(overall_planned - overall_actual, 0)

    reliable_reach = reach_data[reach_data["Planned Reach"] > 0].copy()
    if not reliable_reach.empty:
        best_reach_row = reliable_reach.sort_values(
            ["Achievement %", "Actual Reach"], ascending=False
        ).iloc[0]
        weakest_reach_row = reliable_reach.sort_values(
            ["Achievement %", "Planned Reach"], ascending=[True, False]
        ).iloc[0]
        gap_row = reliable_reach.sort_values(
            ["Gap", "Planned Reach"], ascending=False
        ).iloc[0]
    else:
        best_reach_row = reach_data.iloc[0]
        weakest_reach_row = reach_data.iloc[-1]
        gap_row = reach_data.iloc[0]

    best_campus = str(best_reach_row["Campus"])
    best_pct = float(best_reach_row["Achievement %"])
    weakest_campus = str(weakest_reach_row["Campus"])
    weakest_pct = float(weakest_reach_row["Achievement %"])
    gap_campus = str(gap_row["Campus"])
    largest_gap = float(gap_row["Gap"])

    actual_leader_row = reach_data.sort_values("Actual Reach", ascending=False).iloc[0]
    actual_leader = str(actual_leader_row["Campus"])
    actual_leader_value = float(actual_leader_row["Actual Reach"])
    actual_share = _pct(actual_leader_value, overall_actual)

    zero_actual = reliable_reach[reliable_reach["Actual Reach"] <= 0]
    zero_actual_count = int(len(zero_actual))

    if overall_pct >= 90:
        health_label = "Strong delivery"
        health_accent = "#17A36B"
    elif overall_pct >= 70:
        health_label = "On track"
        health_accent = "#2D6CDF"
    elif overall_pct >= 50:
        health_label = "Needs acceleration"
        health_accent = "#E9A11B"
    else:
        health_label = "Execution risk"
        health_accent = "#E05555"

    achievement_colors = []
    for pct in reach_data["Achievement %"]:
        if pct >= 90:
            achievement_colors.append("#18A36F")
        elif pct >= 70:
            achievement_colors.append("#2F7BD8")
        elif pct >= 50:
            achievement_colors.append("#EAA325")
        else:
            achievement_colors.append("#E35A59")

    campus_order = reach_data["Campus"].astype(str).tolist()
    actual_text = [
        f"{int(v):,} · {p:.0f}%"
        for v, p in zip(reach_data["Actual Reach"], reach_data["Achievement %"])
    ]

    reach_left, reach_right = st.columns([1.68, .82], gap="small")

    with reach_left:
        with st.container(border=True):
            st.markdown('<span class="reach-chart-marker"></span>', unsafe_allow_html=True)
            st.markdown(
                '<div class="reach-card-head reach-card-head-compact">'
                '<span class="reach-live-pill">Filtered view</span>'
                '</div>',
                unsafe_allow_html=True,
            )

            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=reach_data["Planned Reach"],
                    y=reach_data["Campus"],
                    name="Planned Reach",
                    orientation="h",
                    width=.62,
                    marker=dict(color="#E1EAF4", line=dict(color="#D5E0EC", width=.7)),
                    customdata=reach_data[["Actual Reach", "Achievement %", "Gap"]].values,
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Planned: %{x:,.0f}<br>"
                        "Actual: %{customdata[0]:,.0f}<br>"
                        "Achievement: %{customdata[1]:.1f}%<br>"
                        "Gap: %{customdata[2]:,.0f}<extra></extra>"
                    ),
                )
            )
            fig.add_trace(
                go.Bar(
                    x=reach_data["Actual Reach"],
                    y=reach_data["Campus"],
                    name="Actual Reach",
                    orientation="h",
                    width=.30,
                    marker=dict(color=achievement_colors),
                    text=actual_text,
                    textposition="outside",
                    cliponaxis=False,
                    textfont=dict(size=10, color="#284A68"),
                    customdata=reach_data[["Planned Reach", "Achievement %", "Gap"]].values,
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Actual: %{x:,.0f}<br>"
                        "Planned: %{customdata[0]:,.0f}<br>"
                        "Achievement: %{customdata[1]:.1f}%<br>"
                        "Gap: %{customdata[2]:,.0f}<extra></extra>"
                    ),
                )
            )
            fig.update_layout(
                barmode="overlay",
                bargap=.34,
                height=315,
                margin=dict(l=8, r=72, t=34, b=26),
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                font=dict(family="Aptos, Segoe UI, Arial, sans-serif", size=11, color="#60758C"),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.035,
                    xanchor="right",
                    x=1,
                    font=dict(size=10, color="#536B84"),
                ),
                hoverlabel=dict(bgcolor="#102A43", font_color="#FFFFFF", bordercolor="#102A43"),
            )
            fig.update_xaxes(
                title="Reach",
                rangemode="tozero",
                showgrid=True,
                gridcolor="#EDF2F7",
                gridwidth=1,
                zeroline=False,
                linecolor="#E1E8F0",
                tickfont=dict(size=9, color="#7B8DA3"),
                title_font=dict(size=9, color="#657B92"),
                automargin=True,
            )
            fig.update_yaxes(
                title="",
                categoryorder="array",
                categoryarray=campus_order,
                autorange="reversed",
                showgrid=False,
                linecolor="#E1E8F0",
                tickfont=dict(size=10, color="#365777"),
                automargin=True,
            )
            st.plotly_chart(fig, width="stretch", config=CHART_CONFIG)

    zero_signal = (
        f"{zero_actual_count} campus{'es' if zero_actual_count != 1 else ''} currently show planned reach but no actual reach."
        if zero_actual_count
        else "All campuses with a plan currently have some actual reach captured."
    )

    priority_action = (
        f"Close the {largest_gap:,.0f} reach gap in {gap_campus} first; then protect delivery momentum in {best_campus}."
        if largest_gap > 0
        else f"Maintain delivery momentum in {best_campus} and keep actual-reach capture current across campuses."
    )

    with reach_right:
        with st.container(border=True):
            st.markdown('<span class="reach-insight-marker"></span>', unsafe_allow_html=True)
            insight_html = (
                '<div class="reach-intel">'
                '<div class="reach-intel-top">'
                '<div>'
                '<div class="reach-intel-title">Reach Intelligence</div>'
                '<div class="reach-intel-sub">Executive readout derived directly from the chart and current filters.</div>'
                '</div>'
                f'<span class="reach-health-badge" style="border-color:{health_accent}33;color:{health_accent};">{escape(health_label)}</span>'
                '</div>'
                '<div class="reach-kpi-grid">'
                f'<div class="reach-kpi" style="--reach-accent:{health_accent};"><div class="reach-kpi-label">Overall achievement</div><div class="reach-kpi-value">{overall_pct:.0f}%</div><div class="reach-kpi-note">{overall_actual:,.0f} delivered of {overall_planned:,.0f} planned</div></div>'
                f'<div class="reach-kpi" style="--reach-accent:#18A36F;"><div class="reach-kpi-label">Best efficiency</div><div class="reach-kpi-value">{escape(best_campus)}</div><div class="reach-kpi-note">{best_pct:.1f}% of plan achieved</div></div>'
                f'<div class="reach-kpi" style="--reach-accent:#E9A11B;"><div class="reach-kpi-label">Largest gap</div><div class="reach-kpi-value">{largest_gap:,.0f}</div><div class="reach-kpi-note">{escape(gap_campus)} planned vs actual shortfall</div></div>'
                f'<div class="reach-kpi" style="--reach-accent:#6A67E8;"><div class="reach-kpi-label">Actual reach leader</div><div class="reach-kpi-value">{escape(actual_leader)}</div><div class="reach-kpi-note">{actual_leader_value:,.0f} reach · {actual_share:.1f}% of actual</div></div>'
                '</div>'
                '<div class="reach-readout">'
                '<div class="reach-readout-title">Management Readout</div>'
                '<div class="reach-signal"><span class="reach-signal-num">1</span>'
                f'<span class="reach-signal-text"><strong>{escape(best_campus)}</strong> is the most efficient campus at {best_pct:.1f}% achievement, while <strong>{escape(weakest_campus)}</strong> is lowest at {weakest_pct:.1f}%.</span></div>'
                '<div class="reach-signal"><span class="reach-signal-num">2</span>'
                f'<span class="reach-signal-text"><strong>{escape(gap_campus)}</strong> carries the largest absolute shortfall of {largest_gap:,.0f}, making it the biggest current reach recovery opportunity.</span></div>'
                '<div class="reach-signal"><span class="reach-signal-num">3</span>'
                f'<span class="reach-signal-text">{escape(zero_signal)}</span></div>'
                '</div>'
                f'<div class="reach-action"><strong>Priority action:</strong> {escape(priority_action)}</div>'
                '</div>'
            )
            st.markdown(insight_html, unsafe_allow_html=True)


# =========================================================
# MONTHLY CAMPUS-WISE ACTIVITY & EVENT SUMMARY — RESTORED
# Placed directly below Campus Reach Achievement
# =========================================================

st.markdown(
    """
    <style>
    .month-report-shell {
        position: relative;
        overflow: hidden;
        margin: .62rem 0 .72rem 0;
        padding: .78rem .82rem .80rem .82rem;
        border: 1px solid #DDE6F1;
        border-radius: 18px;
        background:
            radial-gradient(circle at 98% 0%, rgba(108, 76, 224, .055), transparent 22%),
            linear-gradient(180deg, #FFFFFF 0%, #FBFCFF 100%);
        box-shadow: 0 12px 32px rgba(22, 49, 88, .065), inset 0 1px 0 rgba(255,255,255,.96);
    }
    .month-report-shell::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg,#2D6CDF,#7453C6,#F1A12B,#19A38D);
    }
    .month-report-head {
        display:flex;
        align-items:flex-start;
        justify-content:space-between;
        gap:1rem;
        margin-bottom:.54rem;
    }
    .month-report-title {
        color:#12365F;
        font-size:1.02rem;
        font-weight:950;
        line-height:1.15;
        letter-spacing:-.015em;
    }
    .month-report-sub {
        color:#7589A3;
        font-size:.64rem;
        margin-top:.11rem;
    }
    .month-range-pill {
        display:inline-flex;
        align-items:center;
        gap:.28rem;
        padding:.25rem .48rem;
        border-radius:999px;
        color:#4A4DA2;
        font-size:.52rem;
        font-weight:900;
        white-space:nowrap;
        border:1px solid #DEDDF4;
        background:linear-gradient(135deg,#F7F6FF,#FFF8EB);
        box-shadow:0 4px 11px rgba(48,68,112,.045);
    }
    .month-range-pill::before {
        content:"";
        width:6px;
        height:6px;
        border-radius:50%;
        background:#6B5CE7;
        box-shadow:0 0 0 3px rgba(107,92,231,.10);
    }
    .month-table-wrap {
        width:100%;
        overflow-x:auto;
        border:1px solid #E1E8F2;
        border-radius:13px;
        background:#FFFFFF;
        scrollbar-width:thin;
        scrollbar-color:#C7D4E4 transparent;
    }
    .month-report-table {
        width:100%;
        min-width:1220px;
        border-collapse:separate;
        border-spacing:0;
        table-layout:auto;
        color:#244565;
        font-size:.53rem;
    }
    .month-report-table th,
    .month-report-table td {
        text-align:center;
        padding:.31rem .30rem;
        border-right:1px solid #E6ECF4;
        border-bottom:1px solid #E6ECF4;
        white-space:nowrap;
        font-variant-numeric:tabular-nums;
    }
    .month-report-table th:last-child,
    .month-report-table td:last-child { border-right:none; }
    .month-report-table thead tr:first-child th {
        background:linear-gradient(180deg,#EFF5FC 0%,#E8F0F9 100%);
        color:#173A67;
        font-size:.55rem;
        font-weight:950;
    }
    .month-report-table thead tr:nth-child(2) th {
        color:#506A87;
        background:#F9FBFD;
        font-size:.50rem;
        font-weight:900;
    }
    .month-report-table .m-completed { background:#2F9D68 !important; color:#FFFFFF !important; }
    .month-report-table .m-confirmed { background:#2F6FBC !important; color:#FFFFFF !important; }
    .month-report-table .m-planned   { background:#82BDE2 !important; color:#FFFFFF !important; }
    .month-report-table .m-cancelled { background:#E25B58 !important; color:#FFFFFF !important; }
    .month-report-table .month-col {
        position:sticky;
        left:0;
        z-index:2;
        text-align:left;
        padding-left:.48rem;
        background:#FAFCFF;
        color:#173A67;
        font-weight:900;
    }
    .month-report-table tbody tr:hover td { background:#F8FBFF; }
    .month-report-table tbody tr:hover .month-col { background:#F1F7FF; }
    .month-report-table .total-row td {
        background:#FFF8E9;
        color:#163960;
        font-weight:950;
        border-bottom:none;
    }
    .month-report-table .total-row .month-col { background:#FFF4D9; }

    .month-insight-grid {
        display:grid;
        grid-template-columns:1.08fr 1fr 1.08fr;
        gap:.58rem;
        margin-top:.62rem;
    }
    .month-insight-card {
        position:relative;
        overflow:hidden;
        min-height:172px;
        padding:.66rem .70rem .62rem .70rem;
        border:1px solid #E0E8F2;
        border-radius:14px;
        background:linear-gradient(150deg,#FFFFFF 0%,#FAFCFF 100%);
        box-shadow:0 7px 18px rgba(22,49,88,.045);
        transition:transform .20s ease, box-shadow .20s ease;
    }
    .month-insight-card:hover {
        transform:translateY(-2px);
        box-shadow:0 12px 25px rgba(22,49,88,.075);
    }
    .month-insight-card::before {
        content:"";
        position:absolute;
        left:0;
        right:0;
        top:0;
        height:2px;
        background:linear-gradient(90deg,#2D6CDF,#7B53D8,#F0A12A);
        opacity:.80;
    }
    .month-card-title {
        display:flex;
        align-items:center;
        gap:.40rem;
        color:#16385F;
        font-size:.73rem;
        font-weight:950;
        margin-bottom:.48rem;
    }
    .month-card-icon {
        width:25px;
        height:25px;
        border-radius:9px;
        display:inline-flex;
        align-items:center;
        justify-content:center;
        font-size:.72rem;
        flex:0 0 25px;
        box-shadow:0 5px 11px rgba(28,57,101,.06);
    }
    .month-card-icon.insight { background:#FFF4D9; color:#D78A11; }
    .month-card-icon.performance { background:#EAF2FF; color:#2D6CDF; }
    .month-card-icon.action { background:#FFF0F2; color:#DB4053; }
    .month-point {
        display:grid;
        grid-template-columns:20px 1fr;
        gap:.38rem;
        align-items:start;
        margin-bottom:.39rem;
    }
    .month-point:last-child { margin-bottom:0; }
    .month-point-num {
        width:20px;
        height:20px;
        border-radius:50%;
        display:flex;
        align-items:center;
        justify-content:center;
        color:#FFFFFF;
        background:linear-gradient(145deg,#3476EE,#4C4DD1);
        font-size:.49rem;
        font-weight:950;
        box-shadow:0 4px 10px rgba(52,90,208,.18);
    }
    .month-point-text {
        color:#5B718B;
        font-size:.54rem;
        line-height:1.42;
    }
    .month-perf-table {
        width:100%;
        border-collapse:collapse;
        font-size:.51rem;
        color:#284866;
    }
    .month-perf-table th {
        color:#75869A;
        font-size:.46rem;
        font-weight:950;
        text-align:left;
        padding:.15rem .12rem .27rem .12rem;
        border-bottom:1px solid #E6ECF3;
        white-space:nowrap;
    }
    .month-perf-table td {
        padding:.28rem .12rem;
        border-bottom:1px solid #EDF1F6;
        font-weight:720;
        vertical-align:middle;
    }
    .month-perf-table tr:last-child td { font-weight:950; border-bottom:none; }
    .month-progress-wrap { display:flex; align-items:center; gap:.24rem; min-width:80px; }
    .month-progress-track {
        height:8px;
        flex:1;
        border-radius:999px;
        overflow:hidden;
        background:#E9EEF5;
    }
    .month-progress-fill {
        height:100%;
        border-radius:999px;
        background:linear-gradient(90deg,#18A45F,#48C989);
    }
    .month-progress-pct {
        color:#218B58;
        font-size:.47rem;
        font-weight:950;
        min-width:25px;
        text-align:right;
    }
    @media (max-width:1100px) {
        .month-insight-grid { grid-template-columns:1fr; }
    }
    @media (prefers-reduced-motion:reduce) {
        .month-insight-card { transition:none !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def _month_status_clean(value):
    if pd.isna(value):
        return ""
    return str(value).strip().title()


def _month_safe_pct(num, den):
    try:
        num = float(num)
        den = float(den)
        return (num / den * 100.0) if den else 0.0
    except Exception:
        return 0.0


def _month_progress(pct):
    pct = max(0.0, min(100.0, float(pct)))
    return (
        '<div class="month-progress-wrap">'
        '<div class="month-progress-track">'
        f'<div class="month-progress-fill" style="width:{pct:.1f}%"></div>'
        '</div>'
        f'<span class="month-progress-pct">{pct:.0f}%</span>'
        '</div>'
    )


if "Activity Date" not in filtered.columns or filtered["Activity Date"].dropna().empty:
    st.info("Monthly campus summary is unavailable because Activity Date is missing for the selected filters.")
else:
    monthly_base = filtered.dropna(subset=["Activity Date"]).copy()
    monthly_base["Month Start"] = monthly_base["Activity Date"].dt.to_period("M").dt.to_timestamp()
    multiple_years = monthly_base["Month Start"].dt.year.nunique() > 1
    monthly_base["Month Label"] = monthly_base["Month Start"].dt.strftime("%b %Y" if multiple_years else "%b")
    monthly_base["Campus"] = monthly_base["Campus"].fillna("Unknown").astype(str).str.strip()
    monthly_base["Status Clean"] = (
        monthly_base["Status"].apply(_month_status_clean)
        if "Status" in monthly_base.columns
        else ""
    )
    monthly_base["Has Event"] = (
        monthly_base["Event"].fillna("").astype(str).str.strip().ne("")
        if "Event" in monthly_base.columns
        else False
    )

    preferred_campuses = ["Noida", "Lucknow", "Jaipur", "Indore"]
    campus_values = monthly_base["Campus"].dropna().astype(str).unique().tolist()
    campuses = [c for c in preferred_campuses if c in campus_values]
    campuses += sorted(c for c in campus_values if c not in campuses)

    months_order = (
        monthly_base[["Month Start", "Month Label"]]
        .drop_duplicates()
        .sort_values("Month Start")
        .reset_index(drop=True)
    )

    rows = []
    for _, month_row in months_order.iterrows():
        month_slice = monthly_base[monthly_base["Month Start"].eq(month_row["Month Start"])]
        row = {"Month": month_row["Month Label"]}
        for campus in campuses:
            cdf = month_slice[month_slice["Campus"].eq(campus)]
            row[(campus, "Activities")] = int(len(cdf))
            row[(campus, "Events")] = int(cdf["Has Event"].sum())
            row[(campus, "Completed")] = int(cdf["Status Clean"].eq("Completed").sum())
            row[(campus, "Confirmed")] = int(cdf["Status Clean"].eq("Confirmed").sum())
            row[(campus, "Planned")] = int(cdf["Status Clean"].eq("Planned").sum())
            row[(campus, "Cancelled")] = int(cdf["Status Clean"].eq("Cancelled").sum())
        rows.append(row)

    total_row = {"Month": "Total"}
    campus_perf = []
    for campus in campuses:
        cdf = monthly_base[monthly_base["Campus"].eq(campus)]
        activities = int(len(cdf))
        events = int(cdf["Has Event"].sum())
        completed = int(cdf["Status Clean"].eq("Completed").sum())
        confirmed = int(cdf["Status Clean"].eq("Confirmed").sum())
        planned = int(cdf["Status Clean"].eq("Planned").sum())
        cancelled = int(cdf["Status Clean"].eq("Cancelled").sum())

        total_row[(campus, "Activities")] = activities
        total_row[(campus, "Events")] = events
        total_row[(campus, "Completed")] = completed
        total_row[(campus, "Confirmed")] = confirmed
        total_row[(campus, "Planned")] = planned
        total_row[(campus, "Cancelled")] = cancelled

        campus_perf.append({
            "Campus": campus,
            "Activities": activities,
            "Events": events,
            "Completed": completed,
            "Completion %": _month_safe_pct(completed, events),
        })
    rows.append(total_row)

    month_stats = []
    for _, month_row in months_order.iterrows():
        mdf = monthly_base[monthly_base["Month Start"].eq(month_row["Month Start"])]
        month_stats.append({
            "Month": month_row["Month Label"],
            "Activities": int(len(mdf)),
            "Events": int(mdf["Has Event"].sum()),
            "Completed": int(mdf["Status Clean"].eq("Completed").sum()),
            "Confirmed": int(mdf["Status Clean"].eq("Confirmed").sum()),
            "Planned": int(mdf["Status Clean"].eq("Planned").sum()),
        })
    month_stats_df = pd.DataFrame(month_stats)
    campus_perf_df = pd.DataFrame(campus_perf)

    peak_activity = month_stats_df.sort_values(["Activities", "Events"], ascending=False).iloc[0]
    month_stats_df["Ready"] = month_stats_df["Completed"] + month_stats_df["Confirmed"]
    peak_execution = month_stats_df.sort_values(["Ready", "Events"], ascending=False).iloc[0]
    leader = campus_perf_df.sort_values(["Activities", "Events"], ascending=False).iloc[0]

    total_month_activities = int(len(monthly_base))
    total_month_events = int(monthly_base["Has Event"].sum())
    total_month_completed = int(monthly_base["Status Clean"].eq("Completed").sum())
    total_month_planned = int(monthly_base["Status Clean"].eq("Planned").sum())

    leader_activity_share = _month_safe_pct(leader["Activities"], total_month_activities)
    leader_event_share = _month_safe_pct(leader["Events"], total_month_events)

    positive_event_perf = campus_perf_df[campus_perf_df["Events"] > 0].copy()
    if not positive_event_perf.empty:
        median_completion = positive_event_perf["Completion %"].median()
        weak = positive_event_perf[positive_event_perf["Completion %"] < median_completion]
        weak_text = ", ".join(weak["Campus"].tolist()[:2]) if not weak.empty else "lower-completion campuses"
    else:
        weak_text = "campuses with pending event execution"

    first_month = str(months_order.iloc[0]["Month Label"])
    last_month = str(months_order.iloc[-1]["Month Label"])
    range_text = first_month if first_month == last_month else f"{first_month} – {last_month}"

    parts = [
        '<div class="month-report-shell">',
        '<div class="month-report-head">',
        '<div>',
        '<div class="month-report-title">Monthly Campus-wise Activity &amp; Event Summary</div>',
        '<div class="month-report-sub">Detailed count of activities, events and execution status by campus and month.</div>',
        '</div>',
        f'<div class="month-range-pill">{html.escape(range_text)}</div>',
        '</div>',
        '<div class="month-table-wrap">',
        '<table class="month-report-table">',
        '<thead><tr>',
        '<th rowspan="2" style="min-width:70px;text-align:left;padding-left:.48rem;">Month</th>',
    ]

    for campus in campuses:
        parts.append(f'<th colspan="6">{html.escape(str(campus))}</th>')
    parts.append('</tr><tr>')
    for _ in campuses:
        parts.extend([
            '<th>Activities</th>',
            '<th>Events</th>',
            '<th class="m-completed">Completed</th>',
            '<th class="m-confirmed">Confirmed</th>',
            '<th class="m-planned">Planned</th>',
            '<th class="m-cancelled">Cancelled</th>',
        ])
    parts.append('</tr></thead><tbody>')

    metrics = ["Activities", "Events", "Completed", "Confirmed", "Planned", "Cancelled"]
    for i, row in enumerate(rows):
        is_total = i == len(rows) - 1
        parts.append('<tr class="total-row">' if is_total else '<tr>')
        parts.append(f'<td class="month-col">{html.escape(str(row["Month"]))}</td>')
        for campus in campuses:
            for metric in metrics:
                parts.append(f'<td>{int(row.get((campus, metric), 0))}</td>')
        parts.append('</tr>')
    parts.extend(['</tbody></table>', '</div>'])

    key_points = [
        f'{peak_activity["Month"]} has the highest activity volume ({int(peak_activity["Activities"]):,}) across all campuses.',
        f'Event execution (Completed + Confirmed) is strongest in {peak_execution["Month"]} ({int(peak_execution["Ready"]):,} activities).',
        f'{leader["Campus"]} contributes the highest activity share ({leader_activity_share:.1f}%) and {leader_event_share:.1f}% of event records.',
        f'Keep monthly event conversion under review where activity volume rises faster than event execution.',
    ]

    action_points = [
        f'Prioritize closure of {total_month_planned:,} planned-status activities across the current selection.',
        f'Focus completion improvement on {weak_text}.',
        'Increase event outcomes in high-activity months where event volume remains comparatively low.',
        f'Review the latest visible month ({last_month}) for ownership, event readiness and timely execution.',
    ]

    parts.append('<div class="month-insight-grid">')

    parts.append('<div class="month-insight-card">')
    parts.append('<div class="month-card-title"><span class="month-card-icon insight">💡</span>Key Insights</div>')
    for idx, text_value in enumerate(key_points, 1):
        parts.append(
            '<div class="month-point">'
            f'<span class="month-point-num">{idx}</span>'
            f'<span class="month-point-text">{html.escape(text_value)}</span>'
            '</div>'
        )
    parts.append('</div>')

    parts.append('<div class="month-insight-card">')
    parts.append(f'<div class="month-card-title"><span class="month-card-icon performance">▥</span>Campus Performance Total ({html.escape(range_text)})</div>')
    parts.append('<table class="month-perf-table"><thead><tr><th>Campus</th><th>Activities</th><th>Events</th><th>Completed</th><th>Completion %</th></tr></thead><tbody>')
    for _, perf in campus_perf_df.iterrows():
        parts.append(
            '<tr>'
            f'<td>{html.escape(str(perf["Campus"]))}</td>'
            f'<td>{int(perf["Activities"]):,}</td>'
            f'<td>{int(perf["Events"]):,}</td>'
            f'<td>{int(perf["Completed"]):,}</td>'
            f'<td>{_month_progress(perf["Completion %"])}</td>'
            '</tr>'
        )
    overall_completion = _month_safe_pct(total_month_completed, total_month_events)
    parts.append(
        '<tr>'
        '<td>Total</td>'
        f'<td>{total_month_activities:,}</td>'
        f'<td>{total_month_events:,}</td>'
        f'<td>{total_month_completed:,}</td>'
        f'<td>{_month_progress(overall_completion)}</td>'
        '</tr>'
    )
    parts.append('</tbody></table></div>')

    parts.append('<div class="month-insight-card">')
    parts.append('<div class="month-card-title"><span class="month-card-icon action">◎</span>Recommended Actions</div>')
    for idx, text_value in enumerate(action_points, 1):
        parts.append(
            '<div class="month-point">'
            f'<span class="month-point-num">{idx}</span>'
            f'<span class="month-point-text">{html.escape(text_value)}</span>'
            '</div>'
        )
    parts.append('</div>')

    parts.extend(['</div>', '</div>'])
    st.markdown(''.join(parts), unsafe_allow_html=True)


# =========================================================
# CAMPUS-WISE ACTIVITY DETAIL TABLE
# Management-ready master view matching the requested design.
# Uses the already-filtered Overview dataset; no existing logic is changed.
# =========================================================

def _detail_first_existing(frame, names):
    for name in names:
        if name in frame.columns:
            return frame[name]
    return pd.Series(pd.NA, index=frame.index, dtype="object")


def _detail_clean_text(value, fallback="—"):
    if pd.isna(value):
        return fallback
    text_value = str(value).strip()
    if not text_value or text_value.lower() in {"nan", "none", "<na>"}:
        return fallback
    return text_value


def _detail_date(value):
    if pd.isna(value):
        return "—"
    try:
        dt_value = pd.to_datetime(value, errors="coerce")
        if pd.isna(dt_value):
            return "—"
        return dt_value.strftime("%d %b %Y")
    except Exception:
        return "—"


def _detail_number(value):
    if pd.isna(value):
        return "—"
    try:
        number = float(value)
        if math.isnan(number):
            return "—"
        if number.is_integer():
            return f"{int(number):,}"
        return f"{number:,.1f}"
    except Exception:
        return _detail_clean_text(value)


def _detail_class_token(value):
    raw = _detail_clean_text(value, "").lower()
    return "".join(ch if ch.isalnum() else "-" for ch in raw).strip("-")


_detail_source = filtered.copy()

# Standardise only for this visual. Source data remains unchanged.
_detail_table = pd.DataFrame(index=_detail_source.index)
_detail_table["Campus"] = _detail_first_existing(_detail_source, ["Campus"])
_detail_table["State"] = _detail_first_existing(
    _detail_source,
    ["State", "Correspondence State", "Present State"],
)
_detail_table["City"] = _detail_first_existing(
    _detail_source,
    ["City", "Present City", "Correspondence City"],
)
_detail_table["Activity Date"] = _detail_first_existing(_detail_source, ["Activity Date"])
_detail_table["Activity Type"] = _detail_first_existing(_detail_source, ["Activity Type"])
_detail_table["Event"] = _detail_first_existing(_detail_source, ["Event"])
_detail_table["Status"] = _detail_first_existing(_detail_source, ["Status"])
_detail_table["Event Date"] = _detail_first_existing(_detail_source, ["Event Date"])
_detail_table["Institution / Event Name"] = _detail_first_existing(
    _detail_source,
    ["Institution / Event Name", "Institution/Event Name", "Institution Name", "Event Name"],
)
_detail_table["Activity Owner"] = _detail_first_existing(_detail_source, ["Activity Owner", "Owner"])
_detail_table["Supporting Team Member"] = _detail_first_existing(
    _detail_source,
    [
        "Supporting Team Member",
        "Supporting Team   Member",
        "Supporting Team member",
        "Supporting Team",
    ],
)
_detail_table["Priority"] = _detail_first_existing(_detail_source, ["Priority"])
_detail_table["Relationship Strength"] = _detail_first_existing(
    _detail_source,
    ["Relationship Strength", "Relationship   Strength"],
)
_detail_table["Participation Type"] = _detail_first_existing(
    _detail_source,
    ["Participation Type", "Participation   Type"],
)
_detail_table["Planned Reach"] = _detail_first_existing(
    _detail_source,
    [
        "Planned Student Reach",
        "Planned Student / faculty Reach",
        "Planned Student / Faculty Reach",
        "Planned Student   / faculty Reach",
    ],
)
_detail_table["Actual Reach"] = _detail_first_existing(
    _detail_source,
    [
        "Actual Student Reach",
        "Actual Student / Faculty Reach",
        "Actual Student / faculty Reach",
        "Actual Student   / Faculty Reach",
    ],
)

_detail_table = _detail_table.reset_index(drop=True)
_detail_table.insert(0, "Sr. No", range(1, len(_detail_table) + 1))

_detail_total_records = int(len(_detail_table))
_detail_campuses = [
    str(value)
    for value in _detail_table["Campus"].dropna().astype(str).str.strip().unique().tolist()
    if str(value).strip()
]
_detail_campus_count = len(_detail_campuses)
_detail_completed = int(
    _detail_table["Status"].astype("string").str.strip().str.casefold().eq("completed").sum()
)
_detail_high_priority = int(
    _detail_table["Priority"].astype("string").str.strip().str.casefold().eq("high").sum()
)
_detail_completed_pct = _pct(_detail_completed, _detail_total_records)
_detail_high_pct = _pct(_detail_high_priority, _detail_total_records)

_detail_campus_order = ["Noida", "Lucknow", "Jaipur", "Indore"]
_detail_present_campuses = [campus for campus in _detail_campus_order if campus in _detail_campuses]
_detail_extra_campuses = sorted([campus for campus in _detail_campuses if campus not in _detail_present_campuses])
_detail_badge_campuses = _detail_present_campuses + _detail_extra_campuses

st.markdown(
    r"""
    <style>
    .campus-master-shell {
        position: relative;
        overflow: hidden;
        margin: .82rem 0 .28rem 0;
        padding: .94rem .96rem .86rem .96rem;
        border: 1px solid #DDE6F1;
        border-radius: 20px;
        background:
            radial-gradient(circle at 98% 0%, rgba(45,108,223,.055), transparent 22%),
            radial-gradient(circle at 3% 100%, rgba(28,169,110,.035), transparent 24%),
            linear-gradient(180deg,#FFFFFF 0%,#FBFCFF 100%);
        box-shadow: 0 16px 36px rgba(22,49,88,.075), inset 0 1px 0 rgba(255,255,255,.96);
    }
    .campus-master-shell::before {
        content:"";
        position:absolute;
        top:0;
        left:-32%;
        width:28%;
        height:3px;
        z-index:5;
        background:linear-gradient(90deg,rgba(45,108,223,0),#2D6CDF,#7655E6,#F1A12B,#20A99A,rgba(32,169,154,0));
        animation: campusMasterSweep 7s ease-in-out infinite;
    }
    @keyframes campusMasterSweep {
        0%,14%{left:-32%;opacity:0;}
        25%{opacity:1;}
        58%{left:108%;opacity:.95;}
        70%,100%{left:108%;opacity:0;}
    }
    .campus-master-head {
        display:flex;
        align-items:flex-start;
        justify-content:space-between;
        gap:1.2rem;
        margin-bottom:.72rem;
    }
    .campus-master-kicker {
        color:#7650A2;
        font-size:.63rem;
        font-weight:950;
        letter-spacing:.12em;
        text-transform:uppercase;
        margin-bottom:.14rem;
    }
    .campus-master-title {
        color:#12365F;
        font-size:1.20rem;
        font-weight:950;
        line-height:1.08;
        letter-spacing:-.02em;
    }
    .campus-master-sub {
        margin-top:.18rem;
        color:#7387A0;
        font-size:.64rem;
        line-height:1.38;
    }
    .campus-master-tabs {
        display:flex;
        align-items:center;
        justify-content:flex-end;
        flex-wrap:wrap;
        gap:7px;
        padding-top:.10rem;
    }
    .campus-master-tab {
        display:inline-flex;
        align-items:center;
        gap:6px;
        min-height:30px;
        padding:.30rem .62rem;
        border-radius:999px;
        border:1px solid #DCE5F1;
        background:#FFFFFF;
        color:#49637E;
        font-size:.54rem;
        font-weight:900;
        box-shadow:0 5px 13px rgba(25,55,95,.045);
        white-space:nowrap;
        transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease;
    }
    .campus-master-tab:hover {
        transform:translateY(-2px);
        box-shadow:0 9px 18px rgba(25,55,95,.085);
        border-color:#C7D7EC;
    }
    .campus-master-tab.active {
        color:#1D63D5;
        border-color:#9EC0FF;
        background:linear-gradient(135deg,#EDF5FF,#F7FAFF);
        box-shadow:0 6px 15px rgba(45,108,223,.10);
    }
    .campus-tab-dot {width:8px;height:8px;border-radius:50%;box-shadow:0 0 0 4px rgba(47,128,237,.08);}
    .campus-tab-dot.all {background:#2F80ED;}
    .campus-tab-dot.noida {background:#2DA9D6;}
    .campus-tab-dot.lucknow {background:#8A5AE8;}
    .campus-tab-dot.jaipur {background:#F0A12B;}
    .campus-tab-dot.indore {background:#28B4AE;}
    .campus-tab-dot.other {background:#7890A8;}

    .campus-master-kpis {
        display:grid;
        grid-template-columns:repeat(4,minmax(0,1fr));
        gap:12px;
        margin-bottom:.78rem;
    }
    .campus-master-kpi {
        position:relative;
        overflow:hidden;
        min-height:92px;
        display:grid;
        grid-template-columns:46px 1fr;
        gap:.68rem;
        align-items:center;
        padding:.72rem .78rem;
        border:1px solid #DBE5F1;
        border-radius:14px;
        background:#FFFFFF;
        box-shadow:0 8px 19px rgba(26,54,91,.045);
        transition:transform .22s ease,box-shadow .22s ease;
    }
    .campus-master-kpi:hover {transform:translateY(-3px);box-shadow:0 14px 28px rgba(26,54,91,.09);}
    .campus-master-kpi::before {content:"";position:absolute;left:0;top:0;bottom:0;width:4px;border-radius:14px 0 0 14px;}
    .campus-master-kpi.blue {background:linear-gradient(135deg,#F8FBFF,#EDF5FF);}
    .campus-master-kpi.teal {background:linear-gradient(135deg,#FAFFFF,#EBFAFB);}
    .campus-master-kpi.violet {background:linear-gradient(135deg,#FCFAFF,#F4EFFF);}
    .campus-master-kpi.amber {background:linear-gradient(135deg,#FFFDF8,#FFF5E6);}
    .campus-master-kpi.blue::before{background:#2F80ED;}
    .campus-master-kpi.teal::before{background:#22B4B2;}
    .campus-master-kpi.violet::before{background:#8B5CE8;}
    .campus-master-kpi.amber::before{background:#F0A12B;}
    .campus-master-kpi-icon {
        width:43px;height:43px;border-radius:12px;display:flex;align-items:center;justify-content:center;
        font-size:1.05rem;font-weight:950;border:1px solid rgba(255,255,255,.75);box-shadow:0 6px 14px rgba(30,62,104,.055);
    }
    .campus-master-kpi.blue .campus-master-kpi-icon{background:#E8F2FF;color:#2F80ED;}
    .campus-master-kpi.teal .campus-master-kpi-icon{background:#DFF8F7;color:#20A5A2;}
    .campus-master-kpi.violet .campus-master-kpi-icon{background:#EEE6FF;color:#8154DC;}
    .campus-master-kpi.amber .campus-master-kpi-icon{background:#FFF0D5;color:#E39318;}
    .campus-master-kpi-label{color:#607690;font-size:.51rem;font-weight:950;letter-spacing:.055em;text-transform:uppercase;}
    .campus-master-kpi-value{color:#16385F;font-size:1.15rem;font-weight:950;line-height:1;margin-top:.13rem;}
    .campus-master-kpi-note{color:#7B8EA5;font-size:.53rem;line-height:1.25;margin-top:.18rem;}

    .campus-detail-wrap {
        position:relative;
        width:100%;
        max-height:590px;
        overflow:auto;
        border:1px solid #DDE6F1;
        border-radius:14px;
        background:#FFFFFF;
        box-shadow:0 7px 17px rgba(24,54,94,.035);
        scrollbar-width:thin;
        scrollbar-color:#BFD0E5 #F4F7FB;
    }
    .campus-detail-table {
        width:100%;
        min-width:2050px;
        border-collapse:separate;
        border-spacing:0;
        table-layout:fixed;
        color:#294B6D;
        font-family:"Aptos", "Segoe UI", Arial, sans-serif;
        font-size:11.5px;
    }
    .campus-detail-table col.sr{width:54px;}
    .campus-detail-table col.campus{width:92px;}
    .campus-detail-table col.state{width:118px;}
    .campus-detail-table col.city{width:110px;}
    .campus-detail-table col.date{width:102px;}
    .campus-detail-table col.activity{width:118px;}
    .campus-detail-table col.event{width:115px;}
    .campus-detail-table col.status{width:105px;}
    .campus-detail-table col.inst{width:190px;}
    .campus-detail-table col.owner{width:126px;}
    .campus-detail-table col.support{width:145px;}
    .campus-detail-table col.priority{width:93px;}
    .campus-detail-table col.relationship{width:118px;}
    .campus-detail-table col.participation{width:115px;}
    .campus-detail-table col.reach{width:126px;}

    .campus-detail-table th,
    .campus-detail-table td {
        border-right:1px solid #E3EAF2;
        border-bottom:1px solid #E6EDF5;
        vertical-align:middle;
    }
    .campus-detail-table th:last-child,.campus-detail-table td:last-child{border-right:none;}
    .campus-detail-table thead th {position:sticky;z-index:3;}
    .campus-detail-table thead tr:first-child th {top:0;}
    .campus-detail-table thead tr:nth-child(2) th {top:36px;}
    .campus-group-head {
        height:36px;
        padding:.42rem .30rem;
        font-size:11px;
        font-weight:950;
        text-align:center;
        letter-spacing:.015em;
        color:#29486B;
    }
    .campus-group-head.location{background:linear-gradient(180deg,#EDF5FF,#E8F1FC);color:#1F59A5;}
    .campus-group-head.activity{background:linear-gradient(180deg,#F6F0FF,#EEE6FD);color:#7441C4;}
    .campus-group-head.ownership{background:linear-gradient(180deg,#FFF7E6,#FFF0D2);color:#A76506;}
    .campus-group-head.reach{background:linear-gradient(180deg,#E9FAFB,#DDF5F6);color:#137B81;}
    .campus-detail-head {
        height:58px;
        padding:.44rem .34rem;
        background:linear-gradient(180deg,#F8FBFF,#F3F7FC);
        color:#23486F;
        font-size:10.5px;
        font-weight:950;
        line-height:1.18;
        text-align:center;
    }
    .campus-detail-head.left{text-align:left;}
    .campus-detail-table tbody tr {
        opacity:0;
        transform:translateY(8px);
        animation:campusRowIn .46s cubic-bezier(.2,.8,.2,1) forwards;
    }
    @keyframes campusRowIn {to{opacity:1;transform:translateY(0);}}
    .campus-detail-table tbody td {
        padding:.50rem .42rem;
        background:#FFFFFF;
        color:#405F7D;
        font-size:11.3px;
        line-height:1.28;
        transition:background .17s ease,color .17s ease,box-shadow .17s ease;
    }
    .campus-detail-table tbody tr:nth-child(even) td {background:#FBFCFE;}
    .campus-detail-table tbody tr:hover td {
        background:#F1F7FF;
        color:#244A70;
        box-shadow:inset 0 1px 0 rgba(47,128,237,.06),inset 0 -1px 0 rgba(47,128,237,.06);
    }
    .campus-detail-table tbody tr:hover td:first-child {box-shadow:inset 4px 0 0 #2F80ED;}
    .detail-sr {text-align:center;font-weight:950;color:#173B62!important;font-variant-numeric:tabular-nums;}
    .detail-campus {font-weight:950;color:#183F68!important;}
    .detail-nowrap{white-space:nowrap;}
    .detail-wrap{white-space:normal;word-break:normal;overflow-wrap:anywhere;}
    .detail-muted{color:#8A9AAF!important;font-style:italic;}
    .detail-reach{text-align:center;font-weight:850;color:#315777!important;font-variant-numeric:tabular-nums;}

    .detail-chip {
        display:inline-flex;
        align-items:center;
        justify-content:center;
        min-height:24px;
        padding:.20rem .48rem;
        border-radius:7px;
        border:1px solid transparent;
        font-size:10px;
        font-weight:950;
        line-height:1;
        white-space:nowrap;
        box-shadow:inset 0 1px 0 rgba(255,255,255,.75);
    }
    .status-planned{color:#2165C7;background:#E4F0FF;border-color:#D2E4FA;}
    .status-confirmed{color:#087F72;background:#DFF7F0;border-color:#C9EEE4;}
    .status-completed{color:#11814B;background:#DDF6E9;border-color:#CBEEDB;}
    .status-cancelled{color:#C93A45;background:#FFE5E8;border-color:#FAD2D7;}
    .status-rescheduled{color:#A76B08;background:#FFF0CF;border-color:#F6DFAD;}
    .status-other{color:#60748A;background:#EEF2F6;border-color:#E1E7EE;}

    .priority-high{color:#C83A4A;background:#FFE3E8;border-color:#FAD1D8;}
    .priority-medium{color:#A46908;background:#FFF1D3;border-color:#F8E0AB;}
    .priority-low{color:#15805A;background:#E2F7ED;border-color:#CEEFE0;}
    .priority-other{color:#667A90;background:#EEF2F6;border-color:#E0E7EF;}

    .relationship-strong{color:#147D49;background:#DDF5E8;border-color:#CBECD9;}
    .relationship-moderate{color:#2868C6;background:#E4EEFF;border-color:#D2E2FA;}
    .relationship-new{color:#A66A08;background:#FFF1D3;border-color:#F7E0B0;}
    .relationship-other{color:#65798F;background:#EEF2F6;border-color:#E0E6EE;}

    .participation-student{color:#2167C9;background:#E5F0FF;border-color:#D4E4FA;}
    .participation-faculty{color:#7440C4;background:#EFE5FF;border-color:#E2D3FA;}
    .participation-mixed{color:#684CC6;background:#ECEAFF;border-color:#DDD8FA;}
    .participation-other{color:#60758B;background:#EEF2F6;border-color:#E0E6EE;}

    .campus-detail-footer {
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:1rem;
        padding:.63rem .12rem .02rem .12rem;
        color:#70869E;
        font-size:.57rem;
        line-height:1.3;
    }
    .campus-detail-footer strong{color:#234A72;}
    .campus-detail-legend{display:flex;align-items:center;gap:10px;flex-wrap:wrap;justify-content:flex-end;}
    .campus-detail-legend span{display:inline-flex;align-items:center;gap:5px;white-space:nowrap;}
    .campus-detail-legend i{width:7px;height:7px;border-radius:50%;display:inline-block;}

    @media(max-width:1100px){
        .campus-master-head{flex-direction:column;}
        .campus-master-tabs{justify-content:flex-start;}
        .campus-master-kpis{grid-template-columns:repeat(2,minmax(0,1fr));}
    }
    @media(max-width:680px){.campus-master-kpis{grid-template-columns:1fr;}}
    @media(prefers-reduced-motion:reduce){
        .campus-master-shell::before,.campus-detail-table tbody tr{animation:none!important;opacity:1!important;transform:none!important;}
        .campus-master-kpi,.campus-master-tab{transition:none!important;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)

_detail_campus_tabs_html = [
    '<span class="campus-master-tab active"><span class="campus-tab-dot all"></span>All Campuses</span>'
]
for _campus_name in _detail_badge_campuses:
    _campus_class = _detail_class_token(_campus_name)
    if _campus_class not in {"noida", "lucknow", "jaipur", "indore"}:
        _campus_class = "other"
    _detail_campus_tabs_html.append(
        f'<span class="campus-master-tab"><span class="campus-tab-dot {_campus_class}"></span>{html.escape(_campus_name)}</span>'
    )

_detail_table_rows = []
for _row_idx, _row in _detail_table.iterrows():
    _campus = _detail_clean_text(_row["Campus"])
    _state = _detail_clean_text(_row["State"])
    _city = _detail_clean_text(_row["City"])
    _activity_date = _detail_date(_row["Activity Date"])
    _activity_type = _detail_clean_text(_row["Activity Type"])
    _event = _detail_clean_text(_row["Event"], "No Event")
    _status = _detail_clean_text(_row["Status"])
    _event_date = _detail_date(_row["Event Date"])
    _institution = _detail_clean_text(_row["Institution / Event Name"])
    _owner = _detail_clean_text(_row["Activity Owner"])
    _support = _detail_clean_text(_row["Supporting Team Member"])
    _priority = _detail_clean_text(_row["Priority"])
    _relationship = _detail_clean_text(_row["Relationship Strength"])
    _participation = _detail_clean_text(_row["Participation Type"])
    _planned_reach = _detail_number(_row["Planned Reach"])
    _actual_reach = _detail_number(_row["Actual Reach"])

    _status_token = _detail_class_token(_status)
    if _status_token not in {"planned", "confirmed", "completed", "cancelled", "rescheduled"}:
        _status_token = "other"
    _priority_token = _detail_class_token(_priority)
    if _priority_token not in {"high", "medium", "low"}:
        _priority_token = "other"
    _relationship_token = _detail_class_token(_relationship)
    if _relationship_token not in {"strong", "moderate", "new"}:
        _relationship_token = "other"
    _participation_token = _detail_class_token(_participation)
    if _participation_token not in {"student", "faculty", "mixed"}:
        _participation_token = "other"

    _delay = min((_row_idx % 18) * 0.025, 0.40)
    _event_class = "detail-muted" if _event == "No Event" else ""

    _detail_table_rows.append(
        f'<tr style="animation-delay:{_delay:.3f}s">'
        f'<td class="detail-sr">{int(_row["Sr. No"]):,}</td>'
        f'<td class="detail-campus detail-nowrap">{html.escape(_campus)}</td>'
        f'<td class="detail-wrap">{html.escape(_state)}</td>'
        f'<td class="detail-wrap">{html.escape(_city)}</td>'
        f'<td class="detail-nowrap">{html.escape(_activity_date)}</td>'
        f'<td class="detail-wrap">{html.escape(_activity_type)}</td>'
        f'<td class="detail-wrap {_event_class}">{html.escape(_event)}</td>'
        f'<td><span class="detail-chip status-{_status_token}">{html.escape(_status)}</span></td>'
        f'<td class="detail-nowrap">{html.escape(_event_date)}</td>'
        f'<td class="detail-wrap">{html.escape(_institution)}</td>'
        f'<td class="detail-wrap">{html.escape(_owner)}</td>'
        f'<td class="detail-wrap">{html.escape(_support)}</td>'
        f'<td><span class="detail-chip priority-{_priority_token}">{html.escape(_priority)}</span></td>'
        f'<td><span class="detail-chip relationship-{_relationship_token}">{html.escape(_relationship)}</span></td>'
        f'<td><span class="detail-chip participation-{_participation_token}">{html.escape(_participation)}</span></td>'
        f'<td class="detail-reach">{html.escape(_planned_reach)}</td>'
        f'<td class="detail-reach">{html.escape(_actual_reach)}</td>'
        '</tr>'
    )

_detail_html = (
    '<div class="campus-master-shell">'
        '<div class="campus-master-head">'
            '<div>'
                '<div class="campus-master-kicker">Campus Outreach Master View</div>'
                '<div class="campus-master-title">Campus-wise Activity Detail Table</div>'
                '<div class="campus-master-sub">Detailed activity-level records across campuses for management review. The table follows the active Overview filters.</div>'
            '</div>'
            '<div class="campus-master-tabs">'
                + ''.join(_detail_campus_tabs_html) +
            '</div>'
        '</div>'
        '<div class="campus-master-kpis">'
            '<div class="campus-master-kpi blue">'
                '<div class="campus-master-kpi-icon">▣</div>'
                '<div><div class="campus-master-kpi-label">Total Records</div>'
                f'<div class="campus-master-kpi-value">{_detail_total_records:,}</div>'
                '<div class="campus-master-kpi-note">Campus outreach activities</div></div>'
            '</div>'
            '<div class="campus-master-kpi teal">'
                '<div class="campus-master-kpi-icon">●</div>'
                '<div><div class="campus-master-kpi-label">Campuses Covered</div>'
                f'<div class="campus-master-kpi-value">{_detail_campus_count:,}</div>'
                f'<div class="campus-master-kpi-note">{html.escape(", ".join(_detail_badge_campuses) if _detail_badge_campuses else "No campus available")}</div></div>'
            '</div>'
            '<div class="campus-master-kpi violet">'
                '<div class="campus-master-kpi-icon">✓</div>'
                '<div><div class="campus-master-kpi-label">Completed Activities</div>'
                f'<div class="campus-master-kpi-value">{_detail_completed:,}</div>'
                f'<div class="campus-master-kpi-note">{_detail_completed_pct:.1f}% of total records</div></div>'
            '</div>'
            '<div class="campus-master-kpi amber">'
                '<div class="campus-master-kpi-icon">!</div>'
                '<div><div class="campus-master-kpi-label">High Priority</div>'
                f'<div class="campus-master-kpi-value">{_detail_high_priority:,}</div>'
                f'<div class="campus-master-kpi-note">{_detail_high_pct:.1f}% of total records</div></div>'
            '</div>'
        '</div>'
        '<div class="campus-detail-wrap">'
            '<table class="campus-detail-table">'
                '<colgroup>'
                    '<col class="sr"><col class="campus"><col class="state"><col class="city">'
                    '<col class="date"><col class="activity"><col class="event"><col class="status"><col class="date"><col class="inst">'
                    '<col class="owner"><col class="support"><col class="priority"><col class="relationship"><col class="participation">'
                    '<col class="reach"><col class="reach">'
                '</colgroup>'
                '<thead>'
                    '<tr>'
                        '<th class="campus-group-head location" rowspan="2">Sr.<br>No</th>'
                        '<th class="campus-group-head location" colspan="3">Location</th>'
                        '<th class="campus-group-head activity" colspan="6">Activity Details</th>'
                        '<th class="campus-group-head ownership" colspan="5">Ownership &amp; Priority</th>'
                        '<th class="campus-group-head reach" colspan="2">Reach</th>'
                    '</tr>'
                    '<tr>'
                        '<th class="campus-detail-head left">Campus</th>'
                        '<th class="campus-detail-head left">State</th>'
                        '<th class="campus-detail-head left">City</th>'
                        '<th class="campus-detail-head">Activity<br>Date</th>'
                        '<th class="campus-detail-head left">Activity Type</th>'
                        '<th class="campus-detail-head left">Event</th>'
                        '<th class="campus-detail-head">Status</th>'
                        '<th class="campus-detail-head">Event Date</th>'
                        '<th class="campus-detail-head left">Institution / Event Name</th>'
                        '<th class="campus-detail-head left">Activity Owner</th>'
                        '<th class="campus-detail-head left">Supporting Team Member</th>'
                        '<th class="campus-detail-head">Priority</th>'
                        '<th class="campus-detail-head">Relationship Strength</th>'
                        '<th class="campus-detail-head">Participation Type</th>'
                        '<th class="campus-detail-head">Planned<br>Student / Faculty Reach</th>'
                        '<th class="campus-detail-head">Actual<br>Student / Faculty Reach</th>'
                    '</tr>'
                '</thead>'
                '<tbody>'
                    + ''.join(_detail_table_rows) +
                '</tbody>'
            '</table>'
        '</div>'
        '<div class="campus-detail-footer">'
            f'<span>Showing <strong>{_detail_total_records:,}</strong> filtered activity records · scroll vertically and horizontally for full detail.</span>'
            '<div class="campus-detail-legend">'
                '<span><i style="background:#2F80ED"></i>Planned</span>'
                '<span><i style="background:#18A56B"></i>Completed</span>'
                '<span><i style="background:#EF5B64"></i>Cancelled</span>'
                '<span><i style="background:#F0A12B"></i>Priority / Rescheduled</span>'
            '</div>'
        '</div>'
    '</div>'
)

st.markdown(_detail_html, unsafe_allow_html=True)


# =========================================================
# FINAL TYPOGRAPHY + KPI ALIGNMENT SYSTEM
# One font family, stronger hierarchy, readable dashboard text.
# =========================================================
st.markdown(
    r"""
    <style>
    :root {
        --dashboard-font: "Aptos", "Segoe UI", Arial, sans-serif;
        --dashboard-navy: #12365F;
        --dashboard-muted: #71849B;
    }

    html,
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stSidebar"],
    .block-container,
    button,
    input,
    textarea,
    select,
    table {
        font-family: var(--dashboard-font) !important;
    }

    /* Keep the same font inside all custom dashboard components. */
    .overview-header,
    .overview-section-kicker,
    .overview-section-title,
    .overview-section-sub,
    .custom-filter-deck-marker,
    .pro-kpi,
    .chart-title,
    .chart-subtitle,
    .chart-insight,
    .q1-matrix-shell,
    .q1-exec-insight,
    .aev-shell,
    .activity-bubble-board,
    .reach-left-card,
    .reach-intel-panel,
    .month-report-shell,
    .campus-master-shell,
    .upcoming-table-shell {
        font-family: var(--dashboard-font) !important;
    }

    /* ---------- Main visual hierarchy ---------- */
    .overview-eyebrow {
        font-size: .69rem !important;
        font-weight: 900 !important;
        letter-spacing: .12em !important;
    }
    .overview-title {
        font-size: 1.38rem !important;
        font-weight: 950 !important;
        line-height: 1.05 !important;
    }
    .overview-subtitle {
        font-size: .82rem !important;
        line-height: 1.35 !important;
    }

    .overview-section-kicker {
        font-size: .66rem !important;
        font-weight: 950 !important;
        letter-spacing: .105em !important;
    }
    .overview-section-title {
        font-size: 1.08rem !important;
        font-weight: 950 !important;
        line-height: 1.14 !important;
        color: var(--dashboard-navy) !important;
    }
    .overview-section-sub {
        font-size: .71rem !important;
        line-height: 1.38 !important;
        color: var(--dashboard-muted) !important;
    }

    .chart-title,
    .table-title,
    .q1-table-heading .title {
        font-size: 1.02rem !important;
        font-weight: 950 !important;
        line-height: 1.15 !important;
        color: var(--dashboard-navy) !important;
    }
    .chart-subtitle,
    .table-subtitle,
    .q1-table-heading .sub {
        font-size: .70rem !important;
        line-height: 1.35 !important;
        color: var(--dashboard-muted) !important;
    }

    /* ======================================================
       KPI CARDS — exact icon/content vertical alignment
       ====================================================== */
    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi {
        position: relative !important;
        overflow: hidden !important;
        width: 100% !important;
        height: 88px !important;
        min-height: 88px !important;
        padding: 0 12px !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 12px !important;
        border-radius: 15px !important;
        background: linear-gradient(135deg,#FFFFFF 0%,#FFFFFF 55%,var(--wash) 145%) !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 8px 20px rgba(27,53,91,.07), inset 0 1px 0 rgba(255,255,255,.98) !important;
        animation: kpiFinalFloat 5.5s ease-in-out infinite !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .kpi-icon-zone {
        width: 46px !important;
        min-width: 46px !important;
        height: 100% !important;
        flex: 0 0 46px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .icon {
        position: relative !important;
        z-index: 2 !important;
        width: 44px !important;
        height: 44px !important;
        min-width: 44px !important;
        min-height: 44px !important;
        flex: 0 0 44px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 !important;
        margin: 0 !important;
        border-radius: 13px !important;
        background: linear-gradient(145deg,#FFFFFF 0%,var(--iconbg) 100%) !important;
        color: var(--accent) !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 6px 15px rgba(27,53,91,.085), inset 0 1px 0 rgba(255,255,255,.95) !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .icon svg {
        display: block !important;
        width: 22px !important;
        height: 22px !important;
        min-width: 22px !important;
        min-height: 22px !important;
        max-width: 22px !important;
        max-height: 22px !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .kpi-content {
        flex: 1 1 auto !important;
        min-width: 0 !important;
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: flex-start !important;
        gap: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .value {
        position: static !important;
        display: block !important;
        margin: 0 !important;
        padding: 0 !important;
        color: #0E315C !important;
        font-size: 1.42rem !important;
        font-weight: 950 !important;
        line-height: 1 !important;
        letter-spacing: -.025em !important;
        white-space: nowrap !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .label {
        position: static !important;
        display: block !important;
        width: 100% !important;
        margin: 5px 0 0 0 !important;
        padding: 0 !important;
        color: #294A70 !important;
        font-size: .56rem !important;
        font-weight: 900 !important;
        line-height: 1.08 !important;
        letter-spacing: 0 !important;
        text-transform: none !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .sub {
        position: static !important;
        display: block !important;
        width: 100% !important;
        margin: 4px 0 0 0 !important;
        padding: 0 !important;
        color: #8194AA !important;
        font-size: .46rem !important;
        font-weight: 550 !important;
        line-height: 1.12 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi::before {
        width: 100% !important;
        height: 3px !important;
        background: linear-gradient(90deg,var(--accent),var(--accent2),rgba(255,255,255,0)) !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi:hover {
        transform: translateY(-3px) scale(1.006) !important;
        box-shadow: 0 14px 28px rgba(27,53,91,.11), inset 0 1px 0 rgba(255,255,255,.98) !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi:hover .icon {
        transform: translateY(-1px) scale(1.035) !important;
    }

    /* ---------- Activity / event matrix readability ---------- */
    .aev-title {
        font-size: 1.05rem !important;
        font-weight: 950 !important;
    }
    .aev-sub {
        font-size: .62rem !important;
        line-height: 1.38 !important;
    }
    .aev-left-head { font-size: .59rem !important; font-weight: 950 !important; }
    .aev-campus-head { font-size: .66rem !important; font-weight: 950 !important; }
    .aev-status-head { font-size: .46rem !important; font-weight: 950 !important; }
    .aev-activity-cell { font-size: .60rem !important; font-weight: 900 !important; }
    .aev-event-main { font-size: .57rem !important; font-weight: 800 !important; }
    .aev-count { font-size: .49rem !important; }
    .aev-total-row td { font-size: .57rem !important; font-weight: 950 !important; }
    .aev-total-label { font-size: .59rem !important; font-weight: 950 !important; }

    /* ---------- Bubble matrix ---------- */
    .activity-bubble-kicker {
        font-size: .64rem !important;
        font-weight: 950 !important;
    }
    .activity-bubble-title {
        font-size: 1.05rem !important;
        font-weight: 950 !important;
        color: var(--dashboard-navy) !important;
    }
    .activity-bubble-sub {
        font-size: .62rem !important;
        line-height: 1.36 !important;
    }

    /* ---------- Reach intelligence ---------- */
    .reach-intel-title {
        font-size: 1.08rem !important;
        font-weight: 950 !important;
        color: var(--dashboard-navy) !important;
    }
    .reach-intel-sub {
        font-size: .61rem !important;
        line-height: 1.36 !important;
    }
    .reach-metric-label {
        font-size: .49rem !important;
        font-weight: 950 !important;
    }
    .reach-metric-value {
        font-size: 1rem !important;
        font-weight: 950 !important;
    }
    .reach-readout-title {
        font-size: .68rem !important;
        font-weight: 950 !important;
    }

    /* ---------- Monthly report ---------- */
    .month-report-title {
        font-size: 1.06rem !important;
        font-weight: 950 !important;
        color: var(--dashboard-navy) !important;
    }
    .month-report-sub {
        font-size: .65rem !important;
        line-height: 1.35 !important;
    }
    .month-report-table th {
        font-weight: 950 !important;
    }
    .month-card-title {
        font-size: .73rem !important;
        font-weight: 950 !important;
    }

    /* ---------- Campus master detail table ---------- */
    .campus-master-kicker {
        font-size: .66rem !important;
        font-weight: 950 !important;
    }
    .campus-master-title {
        font-size: 1.22rem !important;
        font-weight: 950 !important;
        color: var(--dashboard-navy) !important;
    }
    .campus-master-sub {
        font-size: .68rem !important;
        line-height: 1.38 !important;
    }
    .campus-master-kpi-label {
        font-size: .55rem !important;
        font-weight: 950 !important;
    }
    .campus-master-kpi-value {
        font-size: 1.20rem !important;
        font-weight: 950 !important;
    }
    .campus-master-kpi-note {
        font-size: .56rem !important;
        line-height: 1.28 !important;
    }
    .campus-group-head {
        font-size: 11.5px !important;
        font-weight: 950 !important;
    }
    .campus-detail-head {
        font-size: 11px !important;
        font-weight: 950 !important;
    }
    .campus-detail-table tbody td {
        font-size: 11.5px !important;
        line-height: 1.30 !important;
    }
    .detail-chip {
        font-size: 10.5px !important;
        font-weight: 900 !important;
    }

    /* Filter labels / buttons stay readable without increasing card height. */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.custom-filter-deck-marker) div[data-testid="stPopover"] > button p,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.custom-filter-deck-marker) div[data-testid="stButton"] button {
        font-size: .73rem !important;
        font-weight: 850 !important;
    }

    @media (max-width: 1250px) {
        div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi {
            gap: 9px !important;
            padding: 0 10px !important;
        }
        div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .kpi-icon-zone {
            width: 42px !important;
            min-width: 42px !important;
            flex-basis: 42px !important;
        }
        div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .icon {
            width: 40px !important;
            height: 40px !important;
            min-width: 40px !important;
            min-height: 40px !important;
        }
        div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .value {
            font-size: 1.27rem !important;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi,
        div[data-testid="stHorizontalBlock"]:has(.snapshot-motion-marker) .pro-kpi .icon {
            animation: none !important;
            transition: none !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)
