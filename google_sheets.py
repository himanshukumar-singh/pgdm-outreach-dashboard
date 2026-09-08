from pathlib import Path

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials


SPREADSHEET_ID = "1mvsB0Ql-tSyzuNIZgxRxQXhh1tfukvGvtyaOOpPMqSo"

SHEET_NAMES = [
    "Lucknow",
    "Noida",
    "Jaipur",
    "Indore",
]


def _get_credentials(scopes):
    """
    Cloud: reads credentials from Streamlit Secrets.
    Local: falls back to google_credentials.json in the project root.
    """
    try:
        service_account_info = dict(st.secrets["gcp_service_account"])

        return Credentials.from_service_account_info(
            service_account_info,
            scopes=scopes,
        )
    except Exception:
        local_credentials = Path(__file__).resolve().parent / "google_credentials.json"

        if not local_credentials.exists():
            raise FileNotFoundError(
                "Google credentials not found. "
                "For local use, keep google_credentials.json in the project root. "
                "For Streamlit Cloud, add [gcp_service_account] in App Secrets."
            )

        return Credentials.from_service_account_file(
            str(local_credentials),
            scopes=scopes,
        )


@st.cache_data(ttl=45, show_spinner=False)
def load_outreach_data():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ]

    credentials = _get_credentials(scopes)
    client = gspread.authorize(credentials)
    workbook = client.open_by_key(SPREADSHEET_ID)

    all_data = []

    for campus in SHEET_NAMES:
        worksheet = workbook.worksheet(campus)
        records = worksheet.get_all_records()
        campus_df = pd.DataFrame(records)

        if not campus_df.empty:
            campus_df["Campus"] = campus
            all_data.append(campus_df)

    if not all_data:
        return pd.DataFrame()

    return pd.concat(
        all_data,
        ignore_index=True,
    )
