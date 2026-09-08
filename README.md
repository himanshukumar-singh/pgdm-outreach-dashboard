# PGDM Outreach Professional Dashboard v2

This version applies the requested UI refinements across all pages:

- Jaipuria branding pushed to the top-left of the sidebar
- Page title shifted upward
- Main content stretched left-to-right automatically
- Compact top filters
- Reduced whitespace between filters and KPI cards
- More professional background, cards and colors
- Same live Google Sheet integration

## Replace in your local project
Copy and replace:
- `app.py`
- `common.py`
- entire `pages` folder

Keep your existing:
- `google_sheets.py`
- `google_credentials.json`

Run:
    py -m streamlit run app.py
