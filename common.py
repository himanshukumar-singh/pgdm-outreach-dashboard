import html
import time
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components


CLOSED_STATUSES = {"Completed", "Cancelled"}

PAGE_LINKS = [
    ("app.py", "Overview", "🏠"),
    ("pages/1_Outreach_Calendar.py", "Outreach Calendar", "📅"),
    ("pages/2_Campus_Analysis.py", "Campus Analysis", "🏫"),
    ("pages/3_Institution_Coverage.py", "Institution Coverage", "🏢"),
    ("pages/4_Geography_Segments.py", "Geography & Segments", "🗺️"),
    ("pages/5_Team_Resources.py", "Team & Resources", "👥"),
    ("pages/6_Action_Center.py", "Action Center", "⚡"),
]


def page_config(title):
    st.set_page_config(
        page_title=f"{title} | PGDM Outreach",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def enable_auto_refresh(seconds=60):
    """
    Automatically refresh the complete Streamlit page every N seconds
    while the dashboard session is active.
    """
    refresh_key = "_outreach_last_auto_refresh"

    if refresh_key not in st.session_state:
        st.session_state[refresh_key] = time.monotonic()

    @st.fragment(run_every=f"{seconds}s")
    def _auto_refresh_fragment():
        now = time.monotonic()

        if now - st.session_state[refresh_key] >= seconds - 1:
            st.session_state[refresh_key] = now
            st.rerun()

    _auto_refresh_fragment()



def hide_streamlit_cloud_branding():
    """Hide Streamlit Community Cloud viewer/hosting badges and app chrome."""

    # Elements rendered inside the Streamlit app DOM.
    st.markdown(
        """
        <style>
        [data-testid="stToolbar"],
        [data-testid="stAppToolbar"],
        [data-testid="stStatusWidget"],
        [data-testid="stDecoration"],
        [data-testid="stHeaderActionElements"],
        [data-testid="stAppDeployButton"],
        #MainMenu,
        footer,
        [class*="viewerBadge"],
        [class*="ViewerBadge"],
        a[href*="share.streamlit.io/user/"],
        a[href*="streamlit.io/cloud"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Community Cloud can render the bottom-right badge outside the app's
    # normal DOM. This small script also checks the parent page and removes
    # only Streamlit Cloud controls in the bottom-right area.
    components.html(
        """
        <script>
        (() => {
            const hideCloudBranding = () => {
                try {
                    const doc = window.parent.document;
                    const win = window.parent;

                    const hide = (el) => {
                        if (!el) return;
                        el.style.setProperty('display', 'none', 'important');
                        el.style.setProperty('visibility', 'hidden', 'important');
                        el.style.setProperty('opacity', '0', 'important');
                        el.style.setProperty('pointer-events', 'none', 'important');
                    };

                    const isBottomRight = (el) => {
                        try {
                            const r = el.getBoundingClientRect();
                            return r.right >= win.innerWidth - 500 &&
                                   r.bottom >= win.innerHeight - 260;
                        } catch (_) {
                            return false;
                        }
                    };

                    const hideClosestFloatingParent = (el) => {
                        let target = el;
                        for (let i = 0; i < 7 && target && target.parentElement; i++) {
                            const style = win.getComputedStyle(target);
                            const r = target.getBoundingClientRect();

                            if (style.position === 'fixed' ||
                                style.position === 'sticky' ||
                                (r.right >= win.innerWidth - 500 &&
                                 r.bottom >= win.innerHeight - 260 &&
                                 r.width <= 520 && r.height <= 320)) {
                                hide(target);
                                return;
                            }

                            if (target.parentElement === doc.body) break;
                            target = target.parentElement;
                        }
                        hide(el);
                    };

                    // Known/likely Streamlit controls.
                    doc.querySelectorAll(`
                        [data-testid="stToolbar"],
                        [data-testid="stAppToolbar"],
                        [data-testid="stStatusWidget"],
                        [data-testid="stDecoration"],
                        [data-testid="stHeaderActionElements"],
                        [data-testid="stAppDeployButton"],
                        [class*="viewerBadge"],
                        [class*="ViewerBadge"],
                        a[href*="share.streamlit.io/user/"],
                        a[href*="streamlit.io/cloud"]
                    `).forEach((el) => {
                        if (isBottomRight(el) ||
                            String(el.className || '').toLowerCase().includes('viewerbadge') ||
                            (el.getAttribute('href') || '').includes('share.streamlit.io/user/')) {
                            hideClosestFloatingParent(el);
                        }
                    });

                    // Text fallback for current Community Cloud badge/popup.
                    doc.querySelectorAll('a, button, div, span').forEach((el) => {
                        const txt = (el.innerText || el.textContent || '')
                            .replace(/\\s+/g, ' ')
                            .trim()
                            .toLowerCase();

                        if ((txt === 'hosted with streamlit' || txt === 'manage app') &&
                            isBottomRight(el)) {
                            hideClosestFloatingParent(el);
                        }
                    });
                } catch (_) {
                    // If Community Cloud changes its DOM/sandbox, leave app running normally.
                }
            };

            hideCloudBranding();
            setTimeout(hideCloudBranding, 250);
            setTimeout(hideCloudBranding, 750);
            setTimeout(hideCloudBranding, 1500);
            setTimeout(hideCloudBranding, 3000);

            try {
                const observer = new MutationObserver(hideCloudBranding);
                observer.observe(window.parent.document.body, {
                    childList: true,
                    subtree: true,
                    attributes: true
                });
            } catch (_) {}
        })();
        </script>
        """,
        height=0,
        width=0,
    )

def inject_css():
    enable_auto_refresh(60)
    st.markdown(
        """
        <style>
        /* ---------------- App shell ---------------- */
        .stApp, [data-testid="stAppViewContainer"] {
            background: #f4f7fb;
        }

        .block-container {
            max-width: none !important;
            padding-top: 0.35rem !important;
            padding-bottom: 1.5rem !important;
            padding-left: 2.0rem !important;
            padding-right: 1.8rem !important;
        }

        header[data-testid="stHeader"] {
            background: rgba(244, 247, 251, 0.92);
        }

        [data-testid="stMainBlockContainer"] {
            padding-top: 0.25rem !important;
        }

        hr {
            border-color: #e4ebf3;
            margin: 0.9rem 0 1rem 0 !important;
        }

        /* ---------------- Sidebar ---------------- */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #082546 0%, #0d315a 100%);
            min-width: 280px !important;
            max-width: 280px !important;
            border-right: 0;
        }

        [data-testid="stSidebar"] * {
            color: #ffffff;
        }

        [data-testid="stSidebarUserContent"] {
            padding-top: 0.75rem !important;
        }

        [data-testid="stSidebarNav"] {
            display: none;
        }

        .brand-wrap {
            margin-top: 0.10rem;
            margin-bottom: 1.15rem;
        }

        .brand-name {
            font-size: 2.0rem;
            font-weight: 800;
            line-height: 1.0;
            margin: 0;
        }

        .brand-sub {
            margin-top: 0.55rem;
            opacity: 0.92;
            font-size: 0.80rem;
            line-height: 1.45;
        }

        .side-section {
            margin-top: 1.00rem;
            margin-bottom: 0.55rem;
            font-size: 0.70rem;
            font-weight: 800;
            letter-spacing: 0.11em;
            opacity: 0.70;
        }

        [data-testid="stSidebar"] .stPageLink a {
            border-radius: 12px;
            padding: 0.70rem 0.80rem;
            margin-bottom: 0.22rem;
            text-decoration: none;
            font-weight: 700;
        }

        [data-testid="stSidebar"] .stPageLink a:hover {
            background: rgba(255,255,255,0.12);
        }

        [data-testid="stSidebar"] .stPageLink a[aria-current="page"] {
            background: rgba(255,255,255,0.14);
        }

        /* ---------------- Top header ---------------- */
        .topbar-wrap {
            background: transparent;
            padding: 0.05rem 0 0.15rem 0;
            margin-bottom: 0.20rem;
        }

        .page-kicker {
            color: #4b7bec;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: .10em;
            text-transform: uppercase;
            margin-bottom: .10rem;
        }

        .page-title {
            color: #102a43;
            font-size: 2.15rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin: 0;
            line-height: 1.05;
        }

        .page-subtitle {
            color: #73849b;
            font-size: 0.96rem;
            margin-top: .35rem;
            margin-bottom: 0;
        }

        .live-badge {
            display: inline-block;
            padding: .42rem .72rem;
            border-radius: 999px;
            background: #e8f7ee;
            color: #16794c;
            font-weight: 800;
            font-size: .72rem;
            border: 1px solid #cbeed9;
            margin-top: 0.30rem;
        }

        /* ---------------- Filter region ---------------- */
        .filter-wrap {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 0.95rem 1rem 0.10rem 1rem;
            box-shadow: 0 6px 20px rgba(15, 23, 42, 0.035);
            margin-top: 0.30rem;
            margin-bottom: 0.90rem;
        }

        .filter-title {
            color: #102a43;
            font-size: 1.04rem;
            font-weight: 800;
            margin: 0 0 0.35rem 0;
        }

        div[data-testid="stSelectbox"] label,
        div[data-testid="stDateInput"] label,
        div[data-testid="stMultiSelect"] label {
            color: #17365d !important;
            font-weight: 700 !important;
            font-size: 0.77rem !important;
        }

        div[data-baseweb="select"] > div,
        div[data-testid="stDateInput"] input {
            border-radius: 10px !important;
            border-color: #e3e9f1 !important;
            background: #fbfcfe !important;
            min-height: 2.85rem !important;
        }

        /* ---------------- Metrics ---------------- */
        .metric-row-gap {
            margin-top: 0.1rem;
            margin-bottom: 0.55rem;
        }

        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 0.95rem 1rem 0.95rem 1rem;
            box-shadow: 0 5px 16px rgba(16, 42, 67, 0.04);
        }

        div[data-testid="stMetric"] label {
            color: #708399 !important;
            font-weight: 700 !important;
            font-size: 0.78rem !important;
        }

        div[data-testid="stMetricValue"] {
            color: #102a43 !important;
            font-weight: 800 !important;
            font-size: 2.1rem !important;
        }

        /* ---------------- Section titles ---------------- */
        .section-title {
            color: #102a43;
            font-size: 1.18rem;
            font-weight: 800;
            margin: 0.20rem 0 0.15rem 0;
        }

        .section-sub {
            color: #7c8ea7;
            font-size: .81rem;
            margin-top: 0;
            margin-bottom: .65rem;
        }

        /* ---------------- Insight cards ---------------- */
        .insight-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #2563eb;
            border-radius: 12px;
            padding: 0.95rem 1rem;
            min-height: 112px;
            box-shadow: 0 5px 18px rgba(16,42,67,.04);
        }

        .insight-card .title {
            color: #17365d;
            font-weight: 800;
            font-size: .84rem;
            margin-bottom: .38rem;
        }

        .insight-card .body {
            color: #52657d;
            font-size: .84rem;
            line-height: 1.52;
        }

        [data-testid="stDataFrame"] {
            background: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }

        .table-note {
            color: #7a8ba3;
            font-size: .76rem;
            margin-top: .30rem;
        }

        /* ---------------- Hide Streamlit Cloud top-right toolbar ---------------- */
        [data-testid="stToolbar"],
        [data-testid="stAppToolbar"],
        [data-testid="stStatusWidget"],
        [data-testid="stDecoration"],
        [data-testid="stHeaderActionElements"],
        #MainMenu {
            display: none !important;
            visibility: hidden !important;
        }

        header[data-testid="stHeader"] {
            height: 0 !important;
            min-height: 0 !important;
            background: transparent !important;
        }

        /* Extra safety for Share / GitHub / Edit controls */
        button[title="Share"],
        button[aria-label="Share"],
        a[aria-label="GitHub"],
        a[title="GitHub"] {
            display: none !important;
            visibility: hidden !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # Remove Streamlit Community Cloud bottom-right branding/viewer badge.
    hide_streamlit_cloud_branding()


def sidebar_nav():
    with st.sidebar:

        logo_path = (
            Path(__file__).resolve().parent
            / "assets"
            / "jaipuria_logo.png"
        )

        if logo_path.exists():
            st.image(
                str(logo_path),
                width=230
            )
        else:
            st.warning("Jaipuria logo not found.")

        st.markdown(
            '<div class="side-section">DASHBOARD PAGES</div>',
            unsafe_allow_html=True
        )

        for path, label, icon in PAGE_LINKS:
            st.page_link(
                path,
                label=label,
                icon=icon
            )

        st.markdown(
            '<div class="side-section">DATA SOURCE</div>',
            unsafe_allow_html=True
        )

        st.caption("● Live Google Sheet")
        st.caption("↻ Auto-sync every 60 sec")



def header(title, subtitle):
    st.markdown('<div class="topbar-wrap">', unsafe_allow_html=True)
    c1, c2 = st.columns([8.4, 1.2])
    with c1:
        st.markdown('<div class="page-kicker">PGDM Outreach Intelligence</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="page-title">{html.escape(title)}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="page-subtitle">{html.escape(subtitle)}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div style="text-align:right;"><span class="live-badge">● LIVE</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def section(title, subtitle=None):
    st.markdown(f'<div class="section-title">{html.escape(title)}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-sub">{html.escape(subtitle)}</div>', unsafe_allow_html=True)


def insight(title, body):
    st.markdown(
        (
            '<div class="insight-card">'
            f'<div class="title">{html.escape(str(title))}</div>'
            f'<div class="body">{html.escape(str(body))}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def clean_data(df):
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()

    text_cols = [
        "Campus", "Month", "Activity Type", "Institution / Event Name", "City",
        "State", "Target Segment", "Activity Owner", "Supporting Team Member",
        "Resource Person", "Status", "Priority", "Relationship Strength",
        "Participation Type", "Follow-up Required", "Repeat Next Year?",
        "Key Outcome / Learning", "Remarks"
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = (
                df[col].astype("string").str.strip()
                .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA})
            )

    if "Activity Date" in df.columns:
        df["Activity Date"] = pd.to_datetime(df["Activity Date"], dayfirst=True, errors="coerce")

    if "Month" in df.columns:
        df["Month"] = df["Month"].str.title()
    if "Status" in df.columns:
        df["Status"] = df["Status"].str.title()
    if "Priority" in df.columns:
        df["Priority"] = df["Priority"].str.title()
    if "Relationship Strength" in df.columns:
        df["Relationship Strength"] = df["Relationship Strength"].str.title()

    for col in ["Planned Student Reach", "Actual Student Reach", "Event Cost ₹"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def load_data():
    from google_sheets import load_outreach_data
    try:
        df = load_outreach_data()
    except Exception as exc:
        st.error(f"Google Sheet data load nahi ho paya: {exc}")
        st.stop()

    if df is None or df.empty:
        st.error("Google Sheet connected hai, lekin outreach data available nahi hai.")
        st.stop()

    return clean_data(df)


def top_filters(df, show_date=True):
    st.markdown('<div class="filter-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="filter-title">Filters</div>', unsafe_allow_html=True)

    layout = [1.0, 1.05, 1.05, 1.0, 1.0, 0.95, 1.15] if show_date else [1,1,1,1,1,1]
    cols = st.columns(layout, gap="medium")

    with cols[0]:
        campuses = ["All"] + sorted(df["Campus"].dropna().unique().tolist()) if "Campus" in df.columns else ["All"]
        campus = st.selectbox("Campus", campuses, index=0)

    with cols[1]:
        activities = ["All"] + sorted(df["Activity Type"].dropna().unique().tolist()) if "Activity Type" in df.columns else ["All"]
        activity = st.selectbox("Activity Type", activities, index=0)

    with cols[2]:
        segments = ["All"] + sorted(df["Target Segment"].dropna().unique().tolist()) if "Target Segment" in df.columns else ["All"]
        segment = st.selectbox("Target Segment", segments, index=0)

    with cols[3]:
        owners = ["All"] + sorted(df["Activity Owner"].dropna().unique().tolist()) if "Activity Owner" in df.columns else ["All"]
        owner = st.selectbox("Owner", owners, index=0)

    with cols[4]:
        statuses = ["All"] + sorted(df["Status"].dropna().unique().tolist()) if "Status" in df.columns else ["All"]
        status = st.selectbox("Status", statuses, index=0)

    with cols[5]:
        priorities = ["All"] + sorted(df["Priority"].dropna().unique().tolist()) if "Priority" in df.columns else ["All"]
        priority = st.selectbox("Priority", priorities, index=0)

    date_range = None
    if show_date:
        with cols[6]:
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

    st.markdown('</div>', unsafe_allow_html=True)

    f = df.copy()
    if campus != "All" and "Campus" in f.columns:
        f = f[f["Campus"] == campus]
    if activity != "All" and "Activity Type" in f.columns:
        f = f[f["Activity Type"] == activity]
    if segment != "All" and "Target Segment" in f.columns:
        f = f[f["Target Segment"] == segment]
    if owner != "All" and "Activity Owner" in f.columns:
        f = f[f["Activity Owner"] == owner]
    if status != "All" and "Status" in f.columns:
        f = f[f["Status"] == status]
    if priority != "All" and "Priority" in f.columns:
        f = f[f["Priority"] == priority]

    if show_date and date_range and isinstance(date_range, (list, tuple)) and len(date_range) == 2 and "Activity Date" in f.columns:
        start = pd.Timestamp(date_range[0])
        end = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
        f = f[(f["Activity Date"] >= start) & (f["Activity Date"] <= end)]

    return f


def metric_row(df):
    today = pd.Timestamp.today().normalize()

    total = len(df)
    institutions = df["Institution / Event Name"].dropna().nunique() if "Institution / Event Name" in df.columns else 0
    cities = df["City"].dropna().nunique() if "City" in df.columns else 0
    planned = df["Planned Student Reach"].sum(min_count=1) if "Planned Student Reach" in df.columns else 0
    actual = df["Actual Student Reach"].sum(min_count=1) if "Actual Student Reach" in df.columns else 0

    if pd.isna(planned):
        planned = 0
    if pd.isna(actual):
        actual = 0

    if "Activity Date" in df.columns:
        upcoming = df["Activity Date"].ge(today)
        if "Status" in df.columns:
            upcoming &= ~df["Status"].isin(CLOSED_STATUSES)
        upcoming = int(upcoming.sum())
    else:
        upcoming = 0

    st.markdown('<div class="metric-row-gap">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Activities", f"{total:,}")
    c2.metric("Upcoming", f"{upcoming:,}")
    c3.metric("Institutions", f"{institutions:,}")
    c4.metric("Cities Covered", f"{cities:,}")
    c5.metric("Planned Reach", f"{int(planned):,}")
    c6.metric("Actual Reach", f"{int(actual):,}")
    st.markdown('</div>', unsafe_allow_html=True)


def plotly_clean(fig, height=360):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=18, b=10),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#53657a"),
        legend_title_text="",
    )
    return fig
