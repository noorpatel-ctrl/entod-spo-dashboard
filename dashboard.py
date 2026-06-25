"""
ENTOD Division Sales Summary Dashboard
======================================
A Streamlit dashboard built for the Apr–May 2026 Division Sales Summary Excel sheet.
Visual style mirrors the original "ENTOD Sales Insight" dashboard (dark theme, red accents,
heroicons, KPI cards, plotly charts, sidebar filters).

Run with:
    streamlit run dashboard.py
"""

import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────────────────────
# SVG ICON CONSTANTS  (Heroicons stroke style, ENTOD red)
# ─────────────────────────────────────────────────────────────────────────────
_H = "xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24'"


def _svg(paths, w=22, sw="1.6"):
    return (f"<svg {_H} width='{w}' height='{w}' "
            f"stroke='#f50f12' stroke-width='{sw}'>{paths}</svg>")


ICO_REVENUE   = _svg("<circle cx='12' cy='12' r='9'/><path stroke-linecap='round' d='M12 7v1m0 8v1m-3-5h4a1.5 1.5 0 0 1 0 3H9m0 0h6M9 12h4a1.5 1.5 0 0 0 0-3H9v3Z'/>")
ICO_QTY       = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M20 7l-8-4-8 4m16 0v10l-8 4m0-14v14M4 7v10l8 4'/>")
ICO_PILL      = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M9.5 3.5a6 6 0 0 1 8.485 8.485L5.984 14.015A6 6 0 0 1 9.5 3.5Zm5 17a6 6 0 0 1-8.485-8.485L18.016 9.98A6 6 0 0 1 14.5 20.5Z'/>")
ICO_PIN       = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M12 2C8.686 2 6 4.686 6 8c0 5.25 6 12 6 12s6-6.75 6-12c0-3.314-2.686-6-6-6Zm0 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4Z'/>")
ICO_TRENDLINE = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M3 17l5-5 4 4 9-9M21 7h-4V3'/>")
ICO_BUILDING  = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M3 21h18M9 21V9l6-4v16M3 21V11l6-2M15 21V5'/>")
ICO_TROPHY    = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M6 3h12M6 3v6a6 6 0 0 0 12 0V3M6 3H4a2 2 0 0 0 0 4h2m12 0h2a2 2 0 0 0 0-4h-2m-6 12v3m0 0H9m3 0h3'/>")
ICO_STAR      = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2Z'/>")
ICO_BANKNOTE  = _svg("<rect x='2' y='6' width='20' height='12' rx='2'/><path stroke-linecap='round' d='M12 10v4m-2-2h4'/>")
ICO_CALENDAR  = _svg("<rect x='3' y='4' width='18' height='18' rx='2'/><path stroke-linecap='round' d='M16 2v4M8 2v4M3 10h18'/>")
ICO_MAP       = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M9 3L3 6v15l6-3 6 3 6-3V3l-6 3-6-3Z'/><path stroke-linecap='round' d='M9 3v15m6-12v15'/>")
ICO_OFFICE    = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M3 21h18V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v16Zm6 0V13h6v8'/><path stroke-linecap='round' d='M9 7h2m4 0h-2M9 11h2m4 0h-2'/>")
ICO_USERS     = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm13 10v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75'/>")

# Section icons (15px)
SICO_KPI   = _svg("<path stroke-linecap='round' d='M3 3v18h18'/><path stroke-linecap='round' d='M7 16l4-4 4 4 4-6'/>", w=15, sw="1.8")
SICO_TREND = _svg("<path stroke-linecap='round' d='M3 17l5-5 4 4 9-9M21 7h-4V3'/>", w=15, sw="1.8")
SICO_PERF  = _svg("<path stroke-linecap='round' d='M6 3h12M6 3v6a6 6 0 0 0 12 0V3M6 3H4a2 2 0 0 0 0 4h2m12 0h2a2 2 0 0 0 0-4h-2m-6 12v3m0 0H9m3 0h3'/>", w=15, sw="1.8")
SICO_TERR  = _svg("<path stroke-linecap='round' d='M12 2C8.686 2 6 4.686 6 8c0 5.25 6 12 6 12s6-6.75 6-12c0-3.314-2.686-6-6-6Zm0 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4Z'/>", w=15, sw="1.8")
SICO_DIV   = _svg("<rect x='8' y='2' width='8' height='4' rx='1'/><rect x='3' y='4' width='18' height='17' rx='2'/><path stroke-linecap='round' d='M8 11h8M8 15h5'/>", w=15, sw="1.8")
SICO_ADV   = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M9.5 3.5L14 8m-4.5-4.5l-3 3 6 6 3-3-6-6ZM4 20h16M12 14v6'/>", w=15, sw="1.8")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ENTOD Division Sales",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Kill Streamlit top whitespace */
#root > div:first-child { margin-top: 0 !important; }
.block-container {
    padding-top: 0.6rem !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
}
header[data-testid="stHeader"] { height: 0 !important; min-height: 0 !important; display: none !important; }
div[data-testid="stToolbar"]  { display: none !important; }
.stDeployButton               { display: none !important; }

/* Base */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0f0f0f; }

/* Ticker */
.ticker-outer {
    width: 100%; overflow: hidden;
    background: linear-gradient(90deg, #b30000, #f50f12, #b30000);
    border-radius: 6px; padding: 7px 0; margin: 6px 0 18px 0;
}
.ticker-inner {
    display: inline-block; white-space: nowrap;
    animation: slide 12s ease-in-out infinite;
    color: #fff; font-weight: 600; font-size: 0.82rem;
    letter-spacing: 0.04em; padding-left: 100%;
}
@keyframes slide {
    0%   { transform: translateX(0%); }
    100% { transform: translateX(-100%); }
}

/* KPI cards */
.kpi-wrap {
    background: #1a1a1a; border: 1px solid #2a2a2a;
    border-top: 3px solid #f50f12; border-radius: 10px;
    padding: 16px 14px 14px 14px; text-align: center;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.kpi-wrap:hover {
    border-top-color: #ff4444;
    box-shadow: 0 4px 20px rgba(245,15,18,0.15);
}
.kpi-icon  { height:26px; display:flex; align-items:center; justify-content:center; margin-bottom:7px; }
.kpi-icon svg { display:block; }
.kpi-label {
    font-size: 0.65rem; font-weight: 600; color: #666;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 6px;
}
.kpi-value {
    font-size: 1.55rem; font-weight: 800; color: #f0f0f0; line-height: 1;
    margin-bottom: 4px;
}
.kpi-value.sm { font-size: 1.1rem; }
.kpi-sub   { font-size: 0.65rem; color: #555; }
.kpi-green { color: #22c55e !important; }
.kpi-red   { color: #f50f12 !important; }

/* Section header */
.sec-hdr {
    display: flex; align-items: center; gap: 8px;
    margin: 28px 0 12px 0; padding-bottom: 8px;
    border-bottom: 1px solid #2a2a2a;
}
.sec-hdr span {
    font-size: 0.95rem; font-weight: 700; color: #e0e0e0;
    letter-spacing: 0.01em;
}
.chart-label {
    font-size: 0.75rem; color: #666; margin-bottom: 4px;
    font-weight: 500; letter-spacing: 0.02em;
}

/* Sidebar — narrow */
[data-testid="stSidebar"] {
    background: #111 !important; border-right: 1px solid #1f1f1f !important;
    min-width: 220px !important; max-width: 220px !important; width: 220px !important;
}
[data-testid="stSidebar"] > div:first-child {
    width: 220px !important; padding: 0.75rem 0.65rem !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stCaption { color: #888 !important; font-size: 11.5px !important; }
[data-testid="stSidebar"] .stMultiSelect { font-size: 11px !important; }

/* Sidebar logo block */
.sb-logo-wrap {
    display: flex; align-items: center; gap: 10px;
    padding: 4px 0 12px 0;
}
.sb-logo-pill {
    width: 44px; height: 44px; border-radius: 8px;
    background: linear-gradient(135deg, #b30000, #f50f12);
    display: flex; align-items: center; justify-content: center;
    color: #fff; font-weight: 800; font-size: 1.05rem; letter-spacing: -0.5px;
}
.sb-brand-name { font-size: 0.95rem; font-weight: 800; color: #f50f12; line-height: 1.15; }
.sb-brand-sub  { font-size: 0.65rem; color: #555; margin-top: 1px; }

/* General */
h1, h2, h3, h4 { color: #f0f0f0 !important; }
.stDataFrame    { border-radius: 8px; overflow: hidden; }
div[data-testid="stMetric"] { background: transparent; }

/* Download button */
.stDownloadButton > button {
    background: #1a0000 !important; border: 1px solid #f50f12 !important;
    color: #f50f12 !important; border-radius: 8px !important; font-weight: 600 !important;
}
.stDownloadButton > button:hover { background: #f50f12 !important; color: #fff !important; }

/* Multiselect tag */
.stMultiSelect span[data-baseweb="tag"] {
    background: #3a0000 !important; color: #ff6666 !important;
}

/* Precision alignment */
div[data-testid="column"] { padding: 0 4px; }
div[data-testid="stHorizontalBlock"] { gap: 12px; }
.rank-badge {
    display:inline-grid; place-items:center; width:20px; height:20px;
    border-radius:6px; background:#3a0000; color:#f50f12;
    font-weight:800; font-size:10.5px;
}
[data-testid="stDataFrame"] table td:first-child,
[data-testid="stDataFrame"] table th:first-child { text-align:center; }
.stMultiSelect, .stDownloadButton { margin-bottom: 2px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="⏳ Loading Division Sales Summary…", ttl=3600)
def load_data():
    """Load the Division Sales Summary Excel file from any of the common names."""
    candidates = [
        "Data.xlsx", "data.xlsx", "Data.xlsb",
        "8286185e__f171ff12-a157-43e8-a392-d1f785be50be.xlsx",
        "data_xlsx.xlsx", "ENTOD_Division_Sales_Summary.xlsx",
    ]
    df = None
    for fname in candidates:
        if os.path.exists(fname):
            engine = "pyxlsb" if fname.endswith(".xlsb") else "openpyxl"
            # The file has 3 leading junk rows: title, summary, blank.
            # The real header sits on the 4th row (0-indexed = 3).
            df = pd.read_excel(fname, engine=engine, skiprows=3, header=0)
            break

    if df is None:
        # Last resort: try the first .xlsx / .xlsb in cwd
        for f in os.listdir("."):
            if f.lower().endswith((".xlsx", ".xlsb")):
                engine = "pyxlsb" if f.endswith(".xlsb") else "openpyxl"
                df = pd.read_excel(f, engine=engine, skiprows=3, header=0)
                break

    if df is None:
        return None

    # Normalise column names — the source uses Unnamed: 0..9 if skiprows is wrong
    expected = ["Division", "HQs", "SPOs", "Qty Apr", "Amt Apr (₹)",
                "Qty May", "Amt May (₹)", "Total Qty", "Total Amt (₹)", "MoM %"]
    if list(df.columns) != expected:
        # If we ended up with the "Unnamed: 0..9" columns, the file was read
        # with the wrong skiprows. Re-read with the correct offset.
        for fname in candidates:
            if os.path.exists(fname):
                engine = "pyxlsb" if fname.endswith(".xlsb") else "openpyxl"
                df = pd.read_excel(fname, engine=engine, skiprows=3, header=0)
                break
        if list(df.columns) != expected:
            df.columns = expected

    # Drop TOTAL row (recomputed by dashboard)
    df = df[df["Division"].astype(str).str.upper() != "TOTAL"].copy()
    df = df.dropna(subset=["Division"])

    for col in ["HQs", "SPOs"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    for col in ["Qty Apr", "Amt Apr (₹)", "Qty May", "Amt May (₹)",
                "Total Qty", "Total Amt (₹)"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df["MoM %"] = pd.to_numeric(df["MoM %"], errors="coerce")

    # Convenience columns
    df["Avg Order Value (₹)"] = df["Total Amt (₹)"] / df["Total Qty"].replace(0, pd.NA)
    df["Avg Order Value (₹)"] = df["Avg Order Value (₹)"].fillna(0)

    return df.reset_index(drop=True)


df_full = load_data()
if df_full is None:
    st.error("❌ Could not find the Excel data file. Place it next to dashboard.py "
             "(any of: Data.xlsx, data.xlsx, Data.xlsb, 8286185e__f171ff12-a157-43e8-a392-d1f785be50be.xlsx).")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-logo-wrap">
        <div class="sb-logo-pill">EN</div>
        <div>
            <div class="sb-brand-name">ENTOD Sales</div>
            <div class="sb-brand-sub">Division Summary · Apr–May 2026</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='border-bottom:1px solid #222; margin-bottom:14px;'></div>",
                unsafe_allow_html=True)
    st.markdown("**Filters**")

    all_divisions = sorted(df_full["Division"].dropna().unique())
    sel_divisions = st.multiselect("🏢 Division", all_divisions,
                                   default=[], placeholder="All divisions")

    months_avail = ["Apr 2026", "May 2026"]
    sel_months = st.multiselect("📅 Month", months_avail,
                               default=[], placeholder="Both months")

    st.markdown("<div style='border-bottom:1px solid #222; margin:14px 0 10px 0;'></div>",
                unsafe_allow_html=True)
    st.caption(f"📊 Divisions in file: **{len(all_divisions)}**")
    st.caption(f"📅 Period covered: **Apr–May 2026**")
    st.caption("ℹ️ Leave blank to include all.")


# ─────────────────────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────────────────────
df = df_full.copy()
if sel_divisions:
    df = df[df["Division"].isin(sel_divisions)]

# When a single month is picked, we still show the row, but the Apr/May columns
# downstream respect the choice via the "current view" totals.
def _view_qty(r):
    if sel_months == ["Apr 2026"]: return r["Qty Apr"]
    if sel_months == ["May 2026"]: return r["Qty May"]
    return r["Total Qty"]

def _view_amt(r):
    if sel_months == ["Apr 2026"]: return r["Amt Apr (₹)"]
    if sel_months == ["May 2026"]: return r["Amt May (₹)"]
    return r["Total Amt (₹)"]


# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
c_logo, c_title = st.columns([1, 10])
with c_logo:
    st.markdown(
        "<div style='width:62px;height:62px;border-radius:10px;"
        "background:linear-gradient(135deg,#b30000,#f50f12);"
        "display:flex;align-items:center;justify-content:center;"
        "color:#fff;font-weight:800;font-size:1.4rem;margin-top:6px;'>EN</div>",
        unsafe_allow_html=True,
    )
with c_title:
    st.markdown("""
    <div style="padding-top:2px;">
        <div style="font-size:1.85rem;font-weight:800;color:#f0f0f0;line-height:1.1;
                    letter-spacing:-0.01em;">
            ENTOD <span style="color:#f50f12;">Division Sales Summary</span>
        </div>
        <div style="font-size:0.78rem;color:#555;margin-top:3px;">
            Ophthalmic &nbsp;·&nbsp; ENT &nbsp;·&nbsp; Dermatology &nbsp;|&nbsp;
            Apr–May 2026 &nbsp;·&nbsp; Quality, Innovation & Research Since 1977
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="ticker-outer">
    <div class="ticker-inner">
        ⚠️&nbsp; This Dashboard Reflects Apr–May 2026 Division Sales Summary
    </div>
</div>
""", unsafe_allow_html=True)

if df.empty:
    st.warning("⚠️ No data matches your filters. Please broaden your selection.")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def fmt_inr(val):
    if pd.isna(val) or val == 0:
        return "₹0"
    if val >= 1e7:  return f"₹{val/1e7:.2f} Cr"
    if val >= 1e5:  return f"₹{val/1e5:.2f} L"
    return f"₹{val:,.0f}"


def fmt_int(val):
    if pd.isna(val): return "0"
    if val >= 1e5:   return f"{val/1e5:.2f} L"
    return f"{int(val):,}"


def sec(icon, title):
    st.markdown(
        f"<div class='sec-hdr'><span>{icon}&nbsp; {title}</span></div>",
        unsafe_allow_html=True,
    )


def clabel(text):
    st.markdown(f"<div class='chart-label'>{text}</div>", unsafe_allow_html=True)


# Plotly theme constants
RED    = "#f50f12"
BG     = "rgba(0,0,0,0)"
PAPER  = "rgba(0,0,0,0)"
FONT   = "#aaaaaa"
GRID   = "rgba(255,255,255,0.05)"
REDS   = [[0, "#3a0000"], [0.4, "#990000"], [0.7, RED], [1, "#ff6060"]]

BASE_LAYOUT = dict(
    paper_bgcolor=PAPER, plot_bgcolor=BG,
    font=dict(color=FONT, family="Inter", size=11),
    hoverlabel=dict(bgcolor="#1a1a1a", bordercolor="#333",
                    font=dict(color="#eee", size=12)),
)
DEFAULT_MARGIN = dict(l=8, r=8, t=16, b=8)

# Shared Plotly modebar config — keep charts clean & enable PNG export
CHART_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": [
        "select2d", "lasso2d", "toggleSpikelines",
        "hoverClosestCartesian", "hoverCompareCartesian",
    ],
    "modeBarButtonsToAdd": ["hoverclosest", "hovercompare"],
    "toImageButtonOptions": {
        "format": "png", "filename": "ENTOD_chart",
        "height": 600, "width": 1200, "scale": 2,
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────────────────────────────────────
total_amt = float(df["Total Amt (₹)"].sum())
total_qty = float(df["Total Qty"].sum())
amt_apr   = float(df["Amt Apr (₹)"].sum())
amt_may   = float(df["Amt May (₹)"].sum())
qty_apr   = float(df["Qty Apr"].sum())
qty_may   = float(df["Qty May"].sum())
mom_rev   = ((amt_may - amt_apr) / amt_apr * 100) if amt_apr else 0
mom_qty   = ((qty_may - qty_apr) / qty_apr * 100) if qty_apr else 0
num_div   = int(df["Division"].nunique())
num_hq    = int(df["HQs"].sum())
num_spo   = int(df["SPOs"].sum())

top_div_row = df.loc[df["Total Amt (₹)"].idxmax()] if not df.empty else None
top_div   = top_div_row["Division"]   if top_div_row is not None else "—"
top_div_amt = top_div_row["Total Amt (₹)"] if top_div_row is not None else 0
top_div_pct = (top_div_amt / total_amt * 100) if total_amt else 0
top_div_s   = (top_div[:14] + "…") if len(str(top_div)) > 14 else top_div

avg_aov = (total_amt / total_qty) if total_qty else 0
avg_rev_per_hq = (total_amt / num_hq) if num_hq else 0

# Per-division MoM list (for MoM Growth card)
if num_div > 0:
    div_mom = ((amt_may - amt_apr) / amt_apr * 100) if amt_apr else 0
    div_mom_str = f"{'▲' if div_mom >= 0 else '▼'} {abs(div_mom):.1f}%"
    div_mom_cls = "kpi-green" if div_mom >= 0 else "kpi-red"
else:
    div_mom_str, div_mom_cls = "—", ""

mom_qty_str = f"{'▲' if mom_qty >= 0 else '▼'} {abs(mom_qty):.1f}%"
mom_qty_cls = "kpi-green" if mom_qty >= 0 else "kpi-red"

sec(SICO_KPI, "Key Performance Indicators")

cols = st.columns(6)
kpis = [
    (ICO_REVENUE,    "Total Revenue",       fmt_inr(total_amt),   "Apr + May 2026",      ""),
    (ICO_QTY,        "Units Sold",          fmt_int(total_qty),   "Sales quantity",      ""),
    (ICO_PILL,       "Active Divisions",    str(num_div),         "Business divisions",  ""),
    (ICO_USERS,      "Active Territories",  f"{num_hq} / {num_spo}", "HQs / SPOs",        ""),
    (ICO_TRENDLINE,  "MoM Revenue Growth",  div_mom_str,          "Apr → May",           div_mom_cls),
    (ICO_BUILDING,   "Avg Revenue / HQ",    fmt_inr(avg_rev_per_hq), "Per territory",     ""),
]
for col, (icon, label, value, sub, extra_cls) in zip(cols, kpis):
    sm = " sm" if len(str(value)) > 9 else ""
    with col:
        st.markdown(f"""
        <div class="kpi-wrap">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value{sm} {extra_cls}">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

cols2 = st.columns(6)
kpis2 = [
    (ICO_TROPHY,    "Top Division",         str(top_div_s),       f"{top_div_pct:.1f}% of revenue", ""),
    (ICO_STAR,      "MoM Qty Growth",        mom_qty_str,          "Apr → May",                       mom_qty_cls),
    (ICO_BANKNOTE,  "Avg Order Value",       fmt_inr(avg_aov),     "Per unit sold",                   ""),
    (ICO_CALENDAR,  "Period Covered",        "Apr–May 2026",       "2 months",                        ""),
    (ICO_MAP,       "April Revenue",         fmt_inr(amt_apr),     "Month 1",                         ""),
    (ICO_OFFICE,    "May Revenue",           fmt_inr(amt_may),     "Month 2",                         ""),
]
for col, (icon, label, value, sub, extra_cls) in zip(cols2, kpis2):
    sm = " sm" if len(str(value)) > 9 else ""
    with col:
        st.markdown(f"""
        <div class="kpi-wrap">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value{sm} {extra_cls}">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# APR vs MAY REVENUE TREND + MoM GROWTH
# ─────────────────────────────────────────────────────────────────────────────
sec(SICO_TREND, "Apr vs May Revenue & MoM Growth")

# Build per-division "Apr → May" trend frame
trend = df[["Division", "Amt Apr (₹)", "Amt May (₹)", "MoM %"]].copy()
trend = trend.sort_values("Amt Apr (₹)", ascending=False).reset_index(drop=True)
trend["MoM %"] = pd.to_numeric(trend["MoM %"], errors="coerce")

cl, cr = st.columns(2)

with cl:
    clabel("Apr vs May Revenue by Division (₹)")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Apr 2026", x=trend["Division"], y=trend["Amt Apr (₹)"],
        marker_color="#990000",
        hovertemplate="<b>%{x}</b><br>Apr: ₹%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="May 2026", x=trend["Division"], y=trend["Amt May (₹)"],
        marker_color=RED,
        hovertemplate="<b>%{x}</b><br>May: ₹%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(**BASE_LAYOUT, height=320, margin=DEFAULT_MARGIN,
        barmode="group",
        xaxis=dict(showgrid=False, tickangle=-30, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f",
                   title=dict(text="Revenue (₹)", font=dict(size=10))),
        legend=dict(font=dict(size=9), bgcolor="rgba(20,20,20,0.8)",
                    bordercolor="#333", borderwidth=1),
        hovermode="x unified",
    )
    st.plotly_chart(fig, width='stretch', config=CHART_CONFIG)

with cr:
    clabel("Month-over-Month Growth % (Apr → May)")
    bar_colors = ["#22c55e" if (pd.notna(v) and v >= 0) else RED
                  for v in trend["MoM %"]]
    fig2 = go.Figure(go.Bar(
        x=trend["Division"], y=trend["MoM %"].round(1),
        marker_color=bar_colors,
        text=trend["MoM %"].apply(
            lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A"),
        textposition="outside", textfont=dict(size=9, color=FONT),
        hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>",
    ))
    fig2.update_layout(**BASE_LAYOUT, height=320, margin=DEFAULT_MARGIN,
        xaxis=dict(showgrid=False, tickangle=-30, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor=GRID,
                   zeroline=True, zerolinecolor="#333", zerolinewidth=1,
                   title=dict(text="MoM %", font=dict(size=10))),
    )
    st.plotly_chart(fig2, width='stretch', config=CHART_CONFIG)


# ─────────────────────────────────────────────────────────────────────────────
# TOP DIVISIONS — REVENUE & QUANTITY
# ─────────────────────────────────────────────────────────────────────────────
sec(SICO_PERF, "Top Divisions — Revenue & Quantity")

cl2, cr2 = st.columns(2)

with cl2:
    clabel("Divisions Ranked by Total Revenue (₹)")
    top_rev = df[["Division", "Total Amt (₹)"]].sort_values("Total Amt (₹)").reset_index(drop=True)
    fig3 = go.Figure(go.Bar(
        x=top_rev["Total Amt (₹)"], y=top_rev["Division"], orientation="h",
        marker=dict(color=top_rev["Total Amt (₹)"].astype(float),
                    colorscale=REDS, showscale=False),
        text=[fmt_inr(v) for v in top_rev["Total Amt (₹)"]],
        textposition="outside", textfont=dict(size=9, color=FONT),
        hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
    ))
    fig3.update_layout(**BASE_LAYOUT, height=340,
        xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
        yaxis=dict(showgrid=False, tickfont=dict(size=10)),
        margin=dict(l=8, r=80, t=16, b=8),
    )
    st.plotly_chart(fig3, width='stretch', config=CHART_CONFIG)

with cr2:
    clabel("Divisions Ranked by Total Quantity (Units)")
    top_qty = df[["Division", "Total Qty"]].sort_values("Total Qty").reset_index(drop=True)
    fig4 = go.Figure(go.Bar(
        x=top_qty["Total Qty"], y=top_qty["Division"], orientation="h",
        marker=dict(color=top_qty["Total Qty"].astype(float),
                    colorscale=REDS, showscale=False),
        text=[fmt_int(v) for v in top_qty["Total Qty"]],
        textposition="outside", textfont=dict(size=9, color=FONT),
        hovertemplate="<b>%{y}</b><br>%{x:,.0f} units<extra></extra>",
    ))
    fig4.update_layout(**BASE_LAYOUT, height=340,
        xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
        yaxis=dict(showgrid=False, tickfont=dict(size=10)),
        margin=dict(l=8, r=80, t=16, b=8),
    )
    st.plotly_chart(fig4, width='stretch', config=CHART_CONFIG)


# ─────────────────────────────────────────────────────────────────────────────
# TERRITORY (HQ / SPO) ANALYSIS + DIVISION DONUT
# ─────────────────────────────────────────────────────────────────────────────
sec(SICO_TERR, "Territory Coverage & Division Mix")

cl3, cr3 = st.columns(2)

with cl3:
    clabel("Head Quarters & SPOs by Division")
    terr = df[["Division", "HQs", "SPOs"]].sort_values("HQs", ascending=False).reset_index(drop=True)
    fig5 = make_subplots(specs=[[{"secondary_y": True}]])
    fig5.add_trace(go.Bar(
        x=terr["Division"], y=terr["HQs"].astype(float),
        name="HQs", marker_color=RED, opacity=0.9,
        hovertemplate="<b>%{x}</b><br>HQs: %{y}<extra></extra>",
    ), secondary_y=False)
    fig5.add_trace(go.Scatter(
        x=terr["Division"], y=terr["SPOs"].astype(float),
        name="SPOs", mode="lines+markers",
        line=dict(color="#ff9999", width=2),
        marker=dict(size=6, color="#ff9999", line=dict(color="#fff", width=1)),
        hovertemplate="<b>%{x}</b><br>SPOs: %{y}<extra></extra>",
    ), secondary_y=True)
    fig5.update_layout(**BASE_LAYOUT, height=320,
        xaxis=dict(showgrid=False, tickangle=-30, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor=GRID,
                   title=dict(text="HQs", font=dict(size=9))),
        yaxis2=dict(showgrid=False,
                    title=dict(text="SPOs", font=dict(size=9))),
        legend=dict(font=dict(size=9), bgcolor="rgba(20,20,20,0.8)",
                    bordercolor="#333", borderwidth=1),
        margin=dict(l=8, r=10, t=16, b=56),
    )
    st.plotly_chart(fig5, width='stretch', config=CHART_CONFIG)

with cr3:
    clabel("Division-wise Revenue Share")
    div_d = df.groupby("Division", as_index=False)["Total Amt (₹)"].sum()
    n     = len(div_d)
    reds  = [RED, "#cc0000", "#ff4444", "#990000", "#ff6666",
             "#800000", "#ff8080", "#660000", "#ffaaaa", "#4d0000"]
    fig6 = go.Figure(go.Pie(
        labels=div_d["Division"], values=div_d["Total Amt (₹)"].round(2),
        hole=0.54,
        marker=dict(colors=reds[:n], line=dict(color="#111", width=2)),
        textinfo="label+percent",
        textfont=dict(size=10, color="#ddd"),
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>",
        insidetextorientation="radial",
    ))
    fig6.add_annotation(
        text=f"<b>{n}</b><br>Divisions",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=14, color="#e0e0e0", family="Inter"),
    )
    fig6.update_layout(**BASE_LAYOUT, height=320, showlegend=False,
        margin=DEFAULT_MARGIN,
    )
    st.plotly_chart(fig6, width='stretch', config=CHART_CONFIG)


# ─────────────────────────────────────────────────────────────────────────────
# DIVISION APR vs MAY + RANKINGS TABLE
# ─────────────────────────────────────────────────────────────────────────────
sec(SICO_DIV, "Division Apr vs May Performance & HQ Coverage")

cl4, cr4 = st.columns([1.4, 1])

with cl4:
    clabel("Division Apr → May Stacked Revenue (₹)")
    div_t = df[["Division", "Amt Apr (₹)", "Amt May (₹)"]].copy()
    div_t = div_t.sort_values("Amt Apr (₹)", ascending=False).reset_index(drop=True)
    fig7 = go.Figure()
    fig7.add_trace(go.Bar(
        x=div_t["Division"], y=div_t["Amt Apr (₹)"],
        name="Apr 2026", marker_color="#990000",
        hovertemplate="<b>%{x}</b><br>Apr: ₹%{y:,.0f}<extra></extra>",
    ))
    fig7.add_trace(go.Bar(
        x=div_t["Division"], y=div_t["Amt May (₹)"],
        name="May 2026", marker_color=RED,
        hovertemplate="<b>%{x}</b><br>May: ₹%{y:,.0f}<extra></extra>",
    ))
    fig7.update_layout(**BASE_LAYOUT, height=320,
        barmode="stack",
        xaxis=dict(showgrid=False, tickangle=-30, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f",
                   title=dict(text="Revenue (₹)", font=dict(size=9))),
        legend=dict(font=dict(size=9), bgcolor="rgba(20,20,20,0.8)",
                    bordercolor="#333", borderwidth=1, x=0, y=1),
        hovermode="x unified",
        margin=dict(l=8, r=8, t=16, b=40),
    )
    st.plotly_chart(fig7, width='stretch', config=CHART_CONFIG)

with cr4:
    clabel("Division Rankings — Revenue & Coverage")
    hq_tbl = (
        df[["Division", "Total Amt (₹)", "Total Qty", "HQs", "SPOs"]]
          .sort_values("Total Amt (₹)", ascending=False)
          .head(15).reset_index(drop=True)
    )
    hq_tbl.insert(0, "#", range(1, len(hq_tbl) + 1))
    hq_tbl["Total Amt (₹)"] = hq_tbl["Total Amt (₹)"].apply(fmt_inr)
    hq_tbl["Total Qty"]     = hq_tbl["Total Qty"].apply(lambda x: f"{int(x):,}")
    hq_tbl.columns          = ["#", "Division", "Revenue", "Qty Sold", "HQs", "SPOs"]
    st.dataframe(
        hq_tbl, width='stretch', height=320, hide_index=True,
        column_config={
            "#":        st.column_config.NumberColumn("#",        width="small"),
            "Revenue":  st.column_config.TextColumn("Revenue",    width="small"),
            "Qty Sold": st.column_config.TextColumn("Qty Sold",   width="small"),
            "HQs":      st.column_config.NumberColumn("HQs",      width="small"),
            "SPOs":     st.column_config.NumberColumn("SPOs",     width="small"),
        },
    )


# ─────────────────────────────────────────────────────────────────────────────
# ADVANCED — Scatter  +  Dual-axis
# ─────────────────────────────────────────────────────────────────────────────
sec(SICO_ADV, "Advanced Analytics")

cl5, cr5 = st.columns(2)

with cl5:
    clabel("Division Revenue vs Qty (bubble size = HQs)")
    fig8 = go.Figure(go.Scatter(
        x=df["Total Qty"], y=df["Total Amt (₹)"],
        mode="markers+text",
        text=df["Division"],
        textposition="top center",
        textfont=dict(size=9, color=FONT),
        marker=dict(
            size=(df["HQs"].astype(float) + 1).clip(lower=8, upper=46),
            color=df["Total Amt (₹)"].astype(float),
            colorscale=REDS, showscale=False,
            line=dict(color="rgba(255,255,255,0.18)", width=1),
        ),
        hovertemplate="<b>%{text}</b><br>Qty: %{x:,}<br>Revenue: ₹%{y:,.0f}<extra></extra>",
    ))
    fig8.update_layout(**BASE_LAYOUT, height=320, margin=DEFAULT_MARGIN,
        xaxis=dict(showgrid=True, gridcolor=GRID,
                   title=dict(text="Sales Qty", font=dict(size=10))),
        yaxis=dict(showgrid=True, gridcolor=GRID,
                   title=dict(text="Revenue (₹)", font=dict(size=10))),
    )
    st.plotly_chart(fig8, width='stretch', config=CHART_CONFIG)

with cr5:
    clabel("Top Divisions — Revenue vs Qty (dual axis)")
    hq2 = (df[["Division", "Total Amt (₹)", "Total Qty"]]
             .sort_values("Total Amt (₹)", ascending=False).head(10)
             .sort_values("Total Amt (₹)").reset_index(drop=True))
    fig9 = make_subplots(specs=[[{"secondary_y": True}]])
    fig9.add_trace(go.Bar(
        x=hq2["Division"], y=hq2["Total Amt (₹)"].astype(float),
        name="Revenue", marker_color=RED, opacity=0.9,
        hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>",
    ), secondary_y=False)
    fig9.add_trace(go.Scatter(
        x=hq2["Division"], y=hq2["Total Qty"].astype(float),
        name="Qty Sold", mode="lines+markers",
        line=dict(color="#ff9999", width=2),
        marker=dict(size=6, color="#ff9999", line=dict(color="#fff", width=1)),
        hovertemplate="<b>%{x}</b><br>Qty: %{y:,}<extra></extra>",
    ), secondary_y=True)
    fig9.update_layout(**BASE_LAYOUT, height=320,
        xaxis=dict(showgrid=False, tickangle=-30, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f",
                   title=dict(text="Revenue (₹)", font=dict(size=9))),
        yaxis2=dict(showgrid=False,
                    title=dict(text="Qty Sold", font=dict(size=9))),
        legend=dict(font=dict(size=9), bgcolor="rgba(20,20,20,0.8)",
                    bordercolor="#333", borderwidth=1),
        barmode="group",
    )
    st.plotly_chart(fig9, width='stretch', config=CHART_CONFIG)


# ─────────────────────────────────────────────────────────────────────────────
# RAW DATA PREVIEW + CSV DOWNLOAD
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
with st.expander("🔍 Raw Data Preview (filtered)", expanded=False):
    preview = df.copy()
    st.caption(f"Showing **{len(preview):,}** filtered divisions.")
    st.dataframe(preview, width='stretch')
    st.markdown("---")
    csv_bytes = preview.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️  Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="ENTOD_Division_Sales_Filtered.csv",
        mime="text/csv",
    )


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    "<p style='text-align:center;color:#2a2a2a;font-size:0.72rem;"
    "margin-top:28px;'>© 2026 ENTOD Pharmaceuticals · Division Sales Summary · "
    "Quality, Innovation & Research Since 1977</p>",
    unsafe_allow_html=True,
)
