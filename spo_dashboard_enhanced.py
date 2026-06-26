import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── SVG icon helpers ───────────────────────────────────────────────────────────
_H = "xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24'"
def _svg(paths, w=22, sw="1.6"):
    return (f"<svg {_H} width='{w}' height='{w}' "
            f"stroke='#f50f12' stroke-width='{sw}'>{paths}</svg>")

ICO_REVENUE  = _svg("<circle cx='12' cy='12' r='9'/><path stroke-linecap='round' d='M12 7v1m0 8v1m-3-5h4a1.5 1.5 0 0 1 0 3H9m0 0h6M9 12h4a1.5 1.5 0 0 0 0-3H9v3Z'/>")
ICO_QTY      = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M20 7l-8-4-8 4m16 0v10l-8 4m0-14v14M4 7v10l8 4'/>")
ICO_SPO      = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z'/>")
ICO_HQ       = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M12 2C8.686 2 6 4.686 6 8c0 5.25 6 12 6 12s6-6.75 6-12c0-3.314-2.686-6-6-6Zm0 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4Z'/>")
ICO_PRODUCT  = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M9.5 3.5a6 6 0 0 1 8.485 8.485L5.984 14.015A6 6 0 0 1 9.5 3.5Zm5 17a6 6 0 0 1-8.485-8.485L18.016 9.98A6 6 0 0 1 14.5 20.5Z'/>")
ICO_DIV      = _svg("<rect x='8' y='2' width='8' height='4' rx='1'/><rect x='3' y='4' width='18' height='17' rx='2'/><path stroke-linecap='round' d='M8 11h8M8 15h5'/>")
ICO_TREND    = _svg("<path stroke-linecap='round' d='M3 17l5-5 4 4 9-9M21 7h-4V3'/>")
ICO_TEAM     = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M18 18.72a9.094 9.094 0 0 0-3.741-.679 9.09 9.09 0 0 0-3.741.679m12 0a9.094 9.094 0 0 0 3.741-.679 3 3 0 0 0-4.406-4.107 6 6 0 0 0-1.334 1.334 6 6 0 0 0-1.334-1.334 3 3 0 0 0-4.406 4.107A9.1 9.1 0 0 0 12 18.72v0m12 0V13.5a1.5 1.5 0 0 0-1.5-1.5h-.5m-12 0h-.5a1.5 1.5 0 0 0-1.5 1.5v5.22m12 0a3 3 0 1 0 5.8 1.5A3 3 0 0 0 22.5 13.5m-12 0a3 3 0 1 0 5.8 1.5A3 3 0 0 0 13.5 13.5'/>")
ICO_REPORTING = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5m.75-9 3-3 2.148 2.148A12.061 12.061 0 0 1 16.5 7.605'/>")

SICO_SPO     = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z'/>", w=15, sw="1.8")
SICO_PERF    = _svg("<path stroke-linecap='round' d='M6 3h12M6 3v6a6 6 0 0 0 12 0V3M6 3H4a2 2 0 0 0 0 4h2m12 0h2a2 2 0 0 0 0-4h-2m-6 12v3m0 0H9m3 0h3'/>", w=15, sw="1.8")
SICO_TREND   = _svg("<path stroke-linecap='round' d='M3 17l5-5 4 4 9-9M21 7h-4V3'/>", w=15, sw="1.8")
SICO_TABLE   = _svg("<rect x='3' y='3' width='18' height='18' rx='2'/><path stroke-linecap='round' d='M3 9h18M9 9v12'/>", w=15, sw="1.8")
SICO_DIV     = _svg("<rect x='8' y='2' width='8' height='4' rx='1'/><rect x='3' y='4' width='18' height='17' rx='2'/><path stroke-linecap='round' d='M8 11h8M8 15h5'/>", w=15, sw="1.8")
SICO_KPI     = _svg("<path stroke-linecap='round' d='M3 3v18h18'/><path stroke-linecap='round' d='M7 16l4-4 4 4 4-6'/>", w=15, sw="1.8")
SICO_HQ      = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M12 2C8.686 2 6 4.686 6 8c0 5.25 6 12 6 12s6-6.75 6-12c0-3.314-2.686-6-6-6Zm0 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4Z'/>", w=15, sw="1.8")
SICO_TEAM    = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M18 18.72a9.094 9.094 0 0 0-3.741-.679 9.09 9.09 0 0 0-3.741.679m12 0a9.094 9.094 0 0 0 3.741-.679 3 3 0 0 0-4.406-4.107 6 6 0 0 0-1.334 1.334 6 6 0 0 0-1.334-1.334 3 3 0 0 0-4.406 4.107A9.1 9.1 0 0 0 12 18.72v0m12 0V13.5a1.5 1.5 0 0 0-1.5-1.5h-.5m-12 0h-.5a1.5 1.5 0 0 0-1.5 1.5v5.22m12 0a3 3 0 1 0 5.8 1.5A3 3 0 0 0 22.5 13.5m-12 0a3 3 0 1 0 5.8 1.5A3 3 0 0 0 13.5 13.5'/>", w=15, sw="1.8")

st.set_page_config(page_title="ENTOD SPO Insight", layout="wide", page_icon="🔴")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
#root > div:first-child { margin-top: 0 !important; }
.block-container { padding-top: 0.6rem !important; padding-bottom: 1rem !important; max-width: 100% !important; }
header[data-testid="stHeader"] { height: 0 !important; min-height: 0 !important; display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }
.stDeployButton { display: none !important; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0f0f0f; }
.ticker-outer { width:100%; overflow:hidden; background:linear-gradient(90deg,#b30000,#f50f12,#b30000); border-radius:6px; padding:7px 0; margin:6px 0 18px 0; }
.ticker-inner { display:inline-block; white-space:nowrap; animation:slide 14s linear infinite; color:#fff; font-weight:600; font-size:0.82rem; letter-spacing:0.04em; padding-left:100%; }
@keyframes slide { 0%{transform:translateX(0%);} 100%{transform:translateX(-100%);} }
.kpi-wrap { background:#1a1a1a; border:1px solid #2a2a2a; border-top:3px solid #f50f12; border-radius:10px; padding:16px 14px 14px 14px; text-align:center; transition:border-color 0.2s,box-shadow 0.2s; }
.kpi-wrap:hover { border-top-color:#ff4444; box-shadow:0 4px 20px rgba(245,15,18,0.15); }
.kpi-icon { height:26px; display:flex; align-items:center; justify-content:center; margin-bottom:7px; }
.kpi-label { font-size:0.65rem; font-weight:600; color:#666; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:6px; }
.kpi-value { font-size:1.55rem; font-weight:800; color:#f0f0f0; line-height:1; margin-bottom:4px; }
.kpi-sub { font-size:0.65rem; color:#555; }
.kpi-green { color:#22c55e !important; }
.kpi-red { color:#f50f12 !important; }
.trophy-card { background:#1a1a1a; border:1px solid #333; border-radius:12px; padding:18px 16px; text-align:center; }
.trophy-name { font-size:1.05rem; font-weight:700; color:#f0f0f0; margin:6px 0 4px 0; word-break:break-word; }
.trophy-val { font-size:1.4rem; font-weight:800; color:#f50f12; }
.trophy-sub { font-size:0.7rem; color:#555; margin-top:4px; }
.sec-hdr { display:flex; align-items:center; gap:8px; margin:28px 0 12px 0; padding-bottom:8px; border-bottom:1px solid #2a2a2a; }
.sec-hdr span { font-size:0.95rem; font-weight:700; color:#e0e0e0; letter-spacing:0.01em; }
.chart-label { font-size:0.75rem; color:#666; margin-bottom:4px; font-weight:500; letter-spacing:0.02em; }
[data-testid="stSidebar"] { background:#111 !important; border-right:1px solid #1f1f1f !important; min-width:210px !important; max-width:210px !important; width:210px !important; }
[data-testid="stSidebar"] > div:first-child { width:210px !important; padding:0.75rem 0.65rem !important; }
[data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stCaption { color:#888 !important; font-size:11.5px !important; }
.sb-logo-wrap { display:flex; align-items:center; gap:10px; padding:4px 0 12px 0; }
.sb-logo-wrap img { height:44px; width:44px; object-fit:contain; border-radius:6px; }
.sb-brand-name { font-size:0.95rem; font-weight:800; color:#f50f12; line-height:1.15; }
.sb-brand-sub { font-size:0.65rem; color:#555; margin-top:1px; }
h1, h2, h3, h4 { color:#f0f0f0 !important; }
.stDataFrame { border-radius:8px; overflow:hidden; }
.stDownloadButton > button { background:#1a0000 !important; border:1px solid #f50f12 !important; color:#f50f12 !important; border-radius:8px !important; font-weight:600 !important; }
.stDownloadButton > button:hover { background:#f50f12 !important; color:#fff !important; }
.stMultiSelect span[data-baseweb="tag"] { background:#3a0000 !important; color:#ff6666 !important; }
div[data-testid="column"] { padding:0 4px; }
div[data-testid="stHorizontalBlock"] { gap:12px; }
.team-card { background:#1a1a1a; border:1px solid #2a2a2a; border-radius:10px; padding:14px 12px; transition:border-color 0.2s,box-shadow 0.2s; }
.team-card:hover { border-color:#444; box-shadow:0 4px 20px rgba(245,15,18,0.1); }
.team-name { font-size:0.78rem; font-weight:700; color:#e0e0e0; line-height:1.3; margin-bottom:6px; }
.team-metrics { display:flex; justify-content:space-between; align-items:center; }
.team-rev { font-size:1.1rem; font-weight:800; color:#f50f12; }
.team-count { font-size:0.65rem; color:#555; background:#222; padding:2px 8px; border-radius:4px; }
.team-mom { font-size:0.7rem; font-weight:600; }
.div-card { background:linear-gradient(180deg,#1a1a1a 0%,#161616 100%); border:1px solid #2a2a2a; border-left:3px solid #f50f12; border-radius:10px; padding:16px 14px; }
.div-name { font-size:0.8rem; font-weight:700; color:#f0f0f0; letter-spacing:0.05em; text-transform:uppercase; }
.div-rev { font-size:1.35rem; font-weight:800; color:#f50f12; margin:6px 0 4px 0; }
.div-sub { font-size:0.65rem; color:#555; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_inr(val):
    if val >= 1e7:  return f"\u20b9{val/1e7:.2f} Cr"
    if val >= 1e5:  return f"\u20b9{val/1e5:.1f} L"
    return f"\u20b9{val:,.0f}"

def sec(icon, title):
    st.markdown(f"<div class='sec-hdr'><span>{icon}&nbsp; {title}</span></div>", unsafe_allow_html=True)

def clabel(text):
    st.markdown(f"<div class='chart-label'>{text}</div>", unsafe_allow_html=True)

def kpi(col, icon, label, value, sub="", cls=""):
    with col:
        st.markdown(f"""
        <div class='kpi-wrap'>
          <div class='kpi-icon'>{icon}</div>
          <div class='kpi-label'>{label}</div>
          <div class='kpi-value {cls}'>{value}</div>
          <div class='kpi-sub'>{sub}</div>
        </div>""", unsafe_allow_html=True)

RED   = "#f50f12"
BG    = "rgba(0,0,0,0)"
PAPER = "rgba(0,0,0,0)"
FONT  = "#aaaaaa"
GRID  = "rgba(255,255,255,0.05)"
REDS  = [[0,"#3a0000"],[0.4,"#990000"],[0.7,RED],[1,"#ff6060"]]
GREENS = [[0,"#1a3300"],[0.5,"#336600"],[1,"#66cc00"]]
BASE_LAYOUT = dict(
    paper_bgcolor=PAPER, plot_bgcolor=BG,
    font=dict(color=FONT, family="Inter", size=11),
    hoverlabel=dict(bgcolor="#1a1a1a", bordercolor="#333", font=dict(color="#eee", size=12)),
)
DEFAULT_MARGIN = dict(l=8, r=8, t=16, b=8)
CFG = {"displayModeBar":True,"displaylogo":False,
       "modeBarButtonsToRemove":["select2d","lasso2d","toggleSpikelines","hoverClosestCartesian","hoverCompareCartesian"],
       "toImageButtonOptions":{"format":"png","filename":"ENTOD_SPO","height":600,"width":1200,"scale":2}}

reds_pie = [RED,"#cc0000","#ff4444","#990000","#ff6666",
            "#800000","#ff8080","#660000","#ffaaaa","#4d0000",
            "#ff2222","#aa0000","#ff5555","#770000","#ff9999","#333333"]
greens_pie = ["#66cc00","#44aa00","#88dd00","#228800","#aaee00","#116600","#ccff33","#004400","#eeff66","#002200","#ddff00","#336600","#bbee00","#1a4400","#99cc00","#333333"]

# ── Division color mapping for Sales Reporting Divisions ──────────────────────
DIV_COLORS = {
    "OPHTHALMIC": "#f50f12",
    "ENSIGHT": "#ff6600",
    "G-TECK": "#66cc00",
    "GLOTEK": "#00ccff",
    "ENTOD BEAUTY": "#ff44aa",
    "FUR": "#ffcc00",
    "Export": "#888888",
}

# ── HQ name normalization mapping ─────────────────────────────────────────────
HQ_NAME_MAP = {
    'C. MUMBAI': 'CENTRAL MUMBAI',
    'CHH. SAMBHAJINAGAR': 'CHH.SAMBHAJINAGAR',
    'HYDERABAD 1': 'HYDERABAD-1',
    'HYDERABAD 2': 'HYDERABAD-2',
    'HYDERABAD 3': 'HYDERABAD-3',
    'HYDERABAD 4': 'HYDERABAD-4',
    'GUWAHATI-I': 'GUWAHATI',
    'GUWAHATI-II': 'GUWAHATI',
    'AMARAVATI': 'AMRAVATI',
    'ANANTPUR': 'ANANTAPUR',
    'BERHAMPUR': 'BEHRAMPUR',
    'ALAPPUZHA': 'ALLEPPEY',
    'WEST MUMBAI': 'W. MUMBAI',
    'AGARTALA': 'AGARTLA',
}

# ── Sales Division to Employee Sales Reporting Division mapping ───────────────
DIV_MAP = {
    'COSMERA': 'ENTOD BEAUTY',
    'ENSIGHT': 'ENSIGHT',
    'Export': 'Export',
    'FUR': 'FUR',
    'G-TECK': 'G-TECK',
    'GLOTEK': 'GLOTEK',
    'MEDEVA': 'ENTOD BEAUTY',
    'OPHTHALMIC': 'OPHTHALMIC'
}


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner="\u23f3 Loading ENTOD Data\u2026", ttl=3600)
def load_data():
    import os
    sales_file = "Sales_HQ_SPO_Mapped_AprMay2026_Fixed.xlsx"
    emp_file = "Employee.xlsx"
    
    if not os.path.exists(sales_file):
        return None, None, None
    
    # Load raw sales data
    raw = pd.read_excel(sales_file, sheet_name="Raw Mapped Detail", header=2, skiprows=[3])
    raw.columns = ["State","Corrected_HQ","Orig_HQ","SPO","Division","Product","Pack",
                   "Qty_Apr","Amt_Apr","Qty_May","Amt_May","Total_Qty","Total_Amt"]
    raw = raw.dropna(subset=["SPO","Division"])
    raw["SPO"] = raw["SPO"].astype(str).str.strip()
    raw["Division"] = raw["Division"].astype(str).str.strip()
    raw["Corrected_HQ_Upper"] = raw["Corrected_HQ"].astype(str).str.strip().str.upper()
    
    # Load non-covering data
    nc = pd.read_excel(sales_file, sheet_name="Non-Covering HQs", header=2, skiprows=[3])
    nc.columns = ["Division","Orig_HQ","Qty_Apr","Amt_Apr","Qty_May","Amt_May","Total_Qty","Total_Amt"]
    nc = nc.dropna(subset=["Division"])
    nc["Division"] = nc["Division"].astype(str).str.strip()
    nc = nc[nc["Division"] != "TOTAL"]
    
    # Load Employee data
    emp = None
    if os.path.exists(emp_file):
        emp = pd.read_excel(emp_file)
        emp.columns = emp.columns.str.strip()
        # Normalize HQ names
        emp["H.Q."] = emp["H.Q."].astype(str).str.strip().str.upper()
        emp["TEAM"] = emp["TEAM"].astype(str).str.strip()
        emp["Sales Reporting Division"] = emp["Sales Reporting Division"].astype(str).str.strip()
    
    return raw, nc, emp

raw_full, nc_full, emp_full = load_data()
if raw_full is None:
    st.error("\u274c Data file not found. Place **Sales_HQ_SPO_Mapped_AprMay2026_Fixed.xlsx** in the same folder.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# ENRICH SALES DATA WITH TEAM & SALES REPORTING DIVISION
# ══════════════════════════════════════════════════════════════════════════════
if emp_full is not None:
    # Create division mapping column
    raw_full["Mapped_Division"] = raw_full["Division"].map(DIV_MAP)
    
    # Normalize HQ names for better matching
    raw_full["Corrected_HQ_Norm"] = raw_full["Corrected_HQ_Upper"].apply(lambda x: HQ_NAME_MAP.get(x, x))
    
    # Build (HQ, Division) -> TEAM lookup from Employee data
    team_lookup = emp_full.groupby(["H.Q.", "Sales Reporting Division"]).agg({
        "TEAM": lambda x: ", ".join(sorted(x.unique())),
        "NAMES": "count"
    }).reset_index()
    team_lookup.columns = ["HQ_Upper", "Emp_Division", "TEAM", "Staff_Count"]
    
    # Join sales data with team info
    raw_full = raw_full.merge(
        team_lookup,
        left_on=["Corrected_HQ_Norm", "Mapped_Division"],
        right_on=["HQ_Upper", "Emp_Division"],
        how="left"
    )
    
    # Handle Export division
    raw_full.loc[raw_full["Division"] == "Export", "TEAM"] = "Export"
    
    # For unmatched records, use Division as fallback TEAM label
    mask = raw_full["TEAM"].isna() & (raw_full["Division"] != "Export")
    raw_full.loc[mask, "TEAM"] = raw_full.loc[mask, "Division"].apply(lambda x: f"{x} (Unmapped)")
    
    # Also create Sales Reporting Division column (use Mapped_Division)
    raw_full["Sales_Reporting_Division"] = raw_full["Mapped_Division"].fillna(raw_full["Division"])
    
    # Clean unmapped labels for display
    raw_full["TEAM_Display"] = raw_full["TEAM"].str.replace(r" \(Unmapped\)$", "", regex=True)
else:
    raw_full["TEAM"] = "Unknown"
    raw_full["TEAM_Display"] = "Unknown"
    raw_full["Sales_Reporting_Division"] = raw_full["Division"]
    raw_full["Staff_Count"] = 0


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR FILTERS
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-logo-wrap">
      <div style='font-size:2rem;'>🔴</div>
      <div>
        <div class="sb-brand-name">ENTOD SPO Insight</div>
        <div class="sb-brand-sub">SPO-Wise + TEAM Analytics</div>
      </div>
    </div>
    <div style='border-bottom:1px solid #222; margin-bottom:14px;'></div>
    """, unsafe_allow_html=True)
    st.markdown("**Filters**")

    all_divs   = sorted(raw_full["Division"].dropna().unique())
    sel_divs   = st.multiselect("\U0001f3e2 Sales Division", all_divs, default=[], placeholder="All divisions")
    
    # Sales Reporting Division filter (from Employee file)
    all_srd = sorted(raw_full["Sales_Reporting_Division"].dropna().unique())
    sel_srd = st.multiselect("📋 Sales Reporting Division", all_srd, default=[], placeholder="All reporting divisions")
    
    # TEAM filter (from Employee file)
    all_teams = sorted([t for t in raw_full["TEAM"].dropna().unique() if "(Unmapped)" not in t])
    sel_teams = st.multiselect("👥 TEAM", all_teams, default=[], placeholder="All teams")
    
    all_states = sorted(raw_full["State"].dropna().unique())
    sel_states = st.multiselect("\U0001f5fa\ufe0f State", all_states, default=[], placeholder="All states")
    
    all_hqs    = sorted(raw_full["Corrected_HQ"].dropna().unique())
    sel_hqs    = st.multiselect("\U0001f4cd HQ", all_hqs, default=[], placeholder="All HQs")
    
    all_spos   = sorted(raw_full["SPO"].dropna().unique())
    sel_spos   = st.multiselect("\U0001f464 SPO / MR (Sales ID)", all_spos, default=[], placeholder="All SPOs")

    st.markdown("<div style='border-bottom:1px solid #222; margin:14px 0 10px 0;'></div>", unsafe_allow_html=True)
    st.caption(f"\U0001f4ca Total SPOs: **{raw_full['SPO'].nunique():,}**")
    st.caption(f"\U0001f4cd Total HQs: **{raw_full['Corrected_HQ'].nunique():,}**")
    if emp_full is not None:
        st.caption(f"👥 Total Employees: **{len(emp_full):,}**")
        st.caption(f"📋 TEAMs: **{emp_full['TEAM'].nunique()}**")
        st.caption(f"📊 Reporting Divisions: **{emp_full['Sales Reporting Division'].nunique()}**")
    st.caption("\u2139\ufe0f Leave blank to include all.")

# ── Apply filters
df = raw_full.copy()
if sel_divs:   df = df[df["Division"].isin(sel_divs)]
if sel_srd:    df = df[df["Sales_Reporting_Division"].isin(sel_srd)]
if sel_teams:  df = df[df["TEAM"].isin(sel_teams)]
if sel_states: df = df[df["State"].isin(sel_states)]
if sel_hqs:    df = df[df["Corrected_HQ"].isin(sel_hqs)]
if sel_spos:   df = df[df["SPO"].isin(sel_spos)]

nc_df = nc_full.copy()
if sel_divs:   nc_df = nc_df[nc_df["Division"].isin(sel_divs)]


# ══════════════════════════════════════════════════════════════════════════════
# HEADER + TICKER
# ══════════════════════════════════════════════════════════════════════════════
c_logo, c_title = st.columns([1, 10])
with c_logo:
    st.markdown("<div style='font-size:52px; margin-top:4px;'>🔴</div>", unsafe_allow_html=True)
with c_title:
    filter_parts = []
    if sel_divs:   filter_parts.append(f"Div: {', '.join(sel_divs)}")
    if sel_srd:    filter_parts.append(f"Reporting Div: {', '.join(sel_srd)}")
    if sel_teams:  filter_parts.append(f"Team: {', '.join(sel_teams[:2])}{'...' if len(sel_teams)>2 else ''}")
    if sel_states: filter_parts.append(f"State: {', '.join(sel_states)}")
    if sel_hqs:    filter_parts.append(f"HQ: {', '.join(sel_hqs[:3])}{'...' if len(sel_hqs)>3 else ''}")
    if sel_spos:   filter_parts.append(f"SPO: {', '.join(sel_spos[:3])}{'...' if len(sel_spos)>3 else ''}")
    filter_txt = " | ".join(filter_parts) or "All SPOs · All HQs · All Divisions · All Teams"
    
    st.markdown(f"""
    <div style='padding-top:6px;'>
      <div style='font-size:1.55rem;font-weight:800;color:#f0f0f0;letter-spacing:-0.02em;'>
        ENTOD SPO-Wise Sales + TEAM Analytics &nbsp;
        <span style='font-size:0.85rem;font-weight:500;color:#555;'>Apr–May 2026</span>
      </div>
      <div style='font-size:0.72rem;color:#555;margin-top:2px;'>{filter_txt}</div>
    </div>""", unsafe_allow_html=True)

# ── Aggregations
total_rev   = df["Total_Amt"].sum()
total_qty   = df["Total_Qty"].sum()
n_spos      = df["SPO"].nunique()
n_hqs       = df["Corrected_HQ"].nunique()
n_prods     = df["Product"].nunique()
n_states    = df["State"].nunique()
n_teams     = df["TEAM"].nunique() if "TEAM" in df.columns else 0
rev_apr     = df["Amt_Apr"].sum()
rev_may     = df["Amt_May"].sum()
mom_pct     = round((rev_may - rev_apr) / rev_apr * 100, 1) if rev_apr else 0
mom_cls     = "kpi-green" if mom_pct >= 0 else "kpi-red"

spo_rev     = df.groupby("SPO")["Total_Amt"].sum()
avg_spo_rev = spo_rev.mean() if len(spo_rev) else 0
top_spo     = spo_rev.idxmax() if len(spo_rev) else "—"
top_spo_rev = spo_rev.max() if len(spo_rev) else 0

hq_rev      = df.groupby("Corrected_HQ")["Total_Amt"].sum()
top_hq      = hq_rev.idxmax() if len(hq_rev) else "—"
top_hq_rev  = hq_rev.max() if len(hq_rev) else 0

ticker_items = [
    f"\U0001f4b0 Total Revenue: {fmt_inr(total_rev)}",
    f"\U0001f4e6 Total Qty: {int(total_qty):,}",
    f"\U0001f464 SPOs: {n_spos}",
    f"\U0001f4cd HQs: {n_hqs}",
    f"👥 TEAMs: {n_teams}",
    f"\U0001f3c6 Top SPO: {top_spo[:20]}",
    f"\U0001f48a Products: {n_prods}",
    f"\U0001f5fa\ufe0f States: {n_states}",
]
ticker_str = "  ·  ".join(ticker_items * 3)
st.markdown(f"<div class='ticker-outer'><div class='ticker-inner'>{ticker_str}</div></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_KPI, "Key Metrics")
k1,k2,k3,k4,k5,k6 = st.columns(6)
kpi(k1, ICO_REVENUE, "Total Revenue",  fmt_inr(total_rev),   "Apr + May 2026")
kpi(k2, ICO_QTY,     "Total Qty Sold", f"{int(total_qty):,}", "All products")
kpi(k3, ICO_SPO,     "Active SPOs",    f"{n_spos}",           "Mapped & covered")
kpi(k4, ICO_HQ,      "HQs Covered",   f"{n_hqs}",            "Corrected HQs")
kpi(k5, ICO_TREND,   "MoM Growth",    f"{mom_pct:+.1f}%",    f"Apr → May", mom_cls)
kpi(k6, ICO_TEAM,    "TEAMs Active",  f"{n_teams}",           "From Employee Data")

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SALES REPORTING DIVISION SUMMARY CARDS
# ══════════════════════════════════════════════════════════════════════════════
sec(ICO_REPORTING, "Sales Reporting Division Summary (from Employee Master)")

# Aggregate by Sales Reporting Division
div_agg = df.groupby("Sales_Reporting_Division").agg({
    "Total_Amt": "sum",
    "Total_Qty": "sum",
    "Amt_Apr": "sum",
    "Amt_May": "sum",
    "SPO": "nunique",
    "Corrected_HQ": "nunique",
    "Product": "nunique"
}).reset_index().sort_values("Total_Amt", ascending=False)
div_agg["MoM_%"] = div_agg.apply(
    lambda r: round((r["Amt_May"] - r["Amt_Apr"]) / r["Amt_Apr"] * 100, 1) if r["Amt_Apr"] > 0 else None, axis=1
)

div_cols = st.columns(min(len(div_agg), 7))
for i, (_, row) in enumerate(div_agg.iterrows()):
    if i < len(div_cols):
        dcolor = DIV_COLORS.get(row["Sales_Reporting_Division"], RED)
        mom_str = f"{row['MoM_%']:+.1f}%" if pd.notna(row["MoM_%"]) else "N/A"
        mom_color = "#22c55e" if (row["MoM_%"] or 0) >= 0 else RED
        with div_cols[i]:
            st.markdown(f"""
            <div class='div-card' style='border-left-color:{dcolor};'>
                <div class='div-name' style='color:{dcolor};'>{row['Sales_Reporting_Division']}</div>
                <div class='div-rev'>{fmt_inr(row['Total_Amt'])}</div>
                <div class='div-sub'>{int(row['SPO'])} SPOs · {int(row['Corrected_HQ'])} HQs · <span style='color:{mom_color};'>{mom_str}</span></div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LEADERBOARD
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_PERF, "Leaderboard — Top Performers")

top5_spo = spo_rev.nlargest(5).reset_index(); top5_spo.columns = ["SPO","Revenue"]
top5_hq  = hq_rev.nlargest(5).reset_index();  top5_hq.columns  = ["HQ","Revenue"]
medals = ["\U0001f947","\U0001f948","\U0001f949","4\ufe0f\u20e3","5\ufe0f\u20e3"]

st.markdown("<div style='font-size:0.7rem;color:#555;font-weight:600;letter-spacing:0.08em;margin-bottom:6px;'>TOP 5 SPOs (MRs)</div>", unsafe_allow_html=True)
col_spo_cards = st.columns(5)
for i, (_, row) in enumerate(top5_spo.iterrows()):
    with col_spo_cards[i]:
        st.markdown(f"""
        <div class="trophy-card">
          <div style="font-size:1.6rem;">{medals[i]}</div>
          <div class="trophy-name">{row["SPO"]}</div>
          <div class="trophy-val">{fmt_inr(row["Revenue"])}</div>
          <div class="trophy-sub">SPO / MR</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
st.markdown("<div style='font-size:0.7rem;color:#555;font-weight:600;letter-spacing:0.08em;margin-bottom:6px;'>TOP 5 HQs</div>", unsafe_allow_html=True)
col_hq_cards = st.columns(5)
for i, (_, row) in enumerate(top5_hq.iterrows()):
    with col_hq_cards[i]:
        st.markdown(f"""
        <div class="trophy-card" style="border-top:3px solid #f5c518;">
          <div style="font-size:1.6rem;">{medals[i]}</div>
          <div class="trophy-name">{row["HQ"]}</div>
          <div class="trophy-val" style="color:#f5c518;">{fmt_inr(row["Revenue"])}</div>
          <div class="trophy-sub">HQ</div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SPO SUMMARY TABLE (enriched with TEAM info)
# ══════════════════════════════════════════════════════════════════════════════
spo_sum = (
    df.groupby("SPO", as_index=False)
      .agg(
          HQ        = ("Corrected_HQ", "first"),
          Division  = ("Division",    lambda x: ", ".join(sorted(x.unique()))),
          TEAM      = ("TEAM",        lambda x: ", ".join(sorted(x.dropna().unique())) if x.notna().any() else "—"),
          Sales_Reporting_Division = ("Sales_Reporting_Division", lambda x: ", ".join(sorted(x.dropna().unique())) if x.notna().any() else "—"),
          State     = ("State",        "first"),
          Amt_Apr   = ("Amt_Apr",      "sum"),
          Amt_May   = ("Amt_May",      "sum"),
          Total_Qty = ("Total_Qty",    "sum"),
          Total_Amt = ("Total_Amt",    "sum"),
          Products  = ("Product",      "nunique"),
      )
      .sort_values("Total_Amt", ascending=False)
      .reset_index(drop=True)
)
spo_sum["MoM_%"] = spo_sum.apply(
    lambda r: round((r["Amt_May"] - r["Amt_Apr"]) / r["Amt_Apr"] * 100, 1)
    if r["Amt_Apr"] > 0 else None, axis=1)

# HQ summary
hq_sum = (
    df.groupby("Corrected_HQ", as_index=False)
      .agg(
          Total_Amt = ("Total_Amt", "sum"),
          Total_Qty = ("Total_Qty", "sum"),
          Amt_Apr   = ("Amt_Apr",   "sum"),
          Amt_May   = ("Amt_May",   "sum"),
          SPO_Count = ("SPO",       "nunique"),
          Products  = ("Product",   "nunique"),
          State     = ("State",     "first"),
          TEAM      = ("TEAM",      lambda x: ", ".join(sorted(set(t.strip() for t in ", ".join(x.dropna().unique()).split(",") if t.strip()))) if x.notna().any() else "—"),
      )
      .sort_values("Total_Amt", ascending=False)
      .reset_index(drop=True)
)
hq_sum["MoM_%"] = hq_sum.apply(
    lambda r: round((r["Amt_May"] - r["Amt_Apr"]) / r["Amt_Apr"] * 100, 1)
    if r["Amt_Apr"] > 0 else None, axis=1)


# ══════════════════════════════════════════════════════════════════════════════
# TEAM-WISE SALES ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_TEAM, "TEAM-Wise Sales Analytics")

# TEAM-level aggregation (excluding unmapped for cleaner view)
team_agg = df[~df["TEAM"].str.contains("(Unmapped)", na=False)].groupby("TEAM").agg({
    "Total_Amt": "sum",
    "Total_Qty": "sum",
    "Amt_Apr": "sum",
    "Amt_May": "sum",
    "SPO": "nunique",
    "Corrected_HQ": "nunique",
    "Product": "nunique"
}).reset_index().sort_values("Total_Amt", ascending=False)
team_agg["MoM_%"] = team_agg.apply(
    lambda r: round((r["Amt_May"] - r["Amt_Apr"]) / r["Amt_Apr"] * 100, 1) if r["Amt_Apr"] > 0 else None, axis=1)

ct1, ct2 = st.columns(2)

with ct1:
    clabel("Top 20 TEAMs by Total Revenue")
    top20t = team_agg.head(20).sort_values("Total_Amt")
    fig_t1 = go.Figure(go.Bar(
        x=top20t["Total_Amt"], y=top20t["TEAM"], orientation="h",
        marker=dict(color=top20t["Total_Amt"].astype(float), colorscale=REDS, showscale=False),
        text=[fmt_inr(v) for v in top20t["Total_Amt"]],
        textposition="outside", textfont=dict(size=8, color=FONT),
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
    ))
    fig_t1.update_layout(**BASE_LAYOUT, height=540,
        xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
        yaxis=dict(showgrid=False, tickfont=dict(size=8)),
        margin=dict(l=8, r=80, t=16, b=8))
    st.plotly_chart(fig_t1, use_container_width=True, config=CFG)

with ct2:
    clabel("TEAM Revenue Share — Top 15 TEAMs")
    top15t = team_agg.head(15).copy()
    others_t = team_agg.iloc[15:]["Total_Amt"].sum() if len(team_agg) > 15 else 0
    if others_t > 0:
        top15t = pd.concat([top15t, pd.DataFrame({"TEAM":["Others"],"Total_Amt":[others_t]})], ignore_index=True)
    fig_t2 = go.Figure(go.Pie(
        labels=top15t["TEAM"], values=top15t["Total_Amt"].round(2), hole=0.52,
        marker=dict(colors=reds_pie[:len(top15t)], line=dict(color="#111", width=2)),
        textinfo="label+percent", textfont=dict(size=8, color="#ddd"),
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>",
        insidetextorientation="radial",
    ))
    fig_t2.add_annotation(text=f"<b>{len(team_agg)}</b><br>TEAMs", x=0.5, y=0.5, showarrow=False,
        font=dict(size=14, color="#e0e0e0", family="Inter"))
    fig_t2.update_layout(**BASE_LAYOUT, height=540, showlegend=False, margin=DEFAULT_MARGIN)
    st.plotly_chart(fig_t2, use_container_width=True, config=CFG)

# TEAM MoM Analysis
ct3, ct4 = st.columns(2)
with ct3:
    clabel("Top 15 TEAMs — Apr vs May Revenue")
    t15t = team_agg.head(15).sort_values("Total_Amt")
    fig_t3 = go.Figure()
    fig_t3.add_trace(go.Bar(name="Apr", x=t15t["Amt_Apr"], y=t15t["TEAM"], orientation="h",
        marker_color="#990000", opacity=0.85,
        hovertemplate="<b>%{y}</b><br>Apr: ₹%{x:,.0f}<extra></extra>"))
    fig_t3.add_trace(go.Bar(name="May", x=t15t["Amt_May"], y=t15t["TEAM"], orientation="h",
        marker_color=RED, opacity=0.85,
        hovertemplate="<b>%{y}</b><br>May: ₹%{x:,.0f}<extra></extra>"))
    fig_t3.update_layout(**BASE_LAYOUT, height=420, barmode="group",
        xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
        yaxis=dict(showgrid=False, tickfont=dict(size=8)),
        legend=dict(font=dict(size=9), bgcolor="rgba(20,20,20,0.8)", bordercolor="#333", borderwidth=1),
        margin=dict(l=8, r=8, t=16, b=8))
    st.plotly_chart(fig_t3, use_container_width=True, config=CFG)

with ct4:
    clabel("Top 20 TEAMs — MoM Revenue Growth %")
    mom_t = team_agg.head(20).dropna(subset=["MoM_%"]).sort_values("MoM_%")
    bar_cols_t = ["#22c55e" if v >= 0 else RED for v in mom_t["MoM_%"]]
    fig_t4 = go.Figure(go.Bar(
        x=mom_t["MoM_%"], y=mom_t["TEAM"], orientation="h",
        marker_color=bar_cols_t,
        text=mom_t["MoM_%"].apply(lambda x: f"{x:+.1f}%"),
        textposition="outside", textfont=dict(size=8, color=FONT),
        hovertemplate="<b>%{y}</b><br>MoM: %{x:+.1f}%<extra></extra>",
    ))
    fig_t4.update_layout(**BASE_LAYOUT, height=420,
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=True, zerolinecolor="#333", zerolinewidth=1),
        yaxis=dict(showgrid=False, tickfont=dict(size=8)),
        margin=dict(l=8, r=50, t=16, b=8))
    st.plotly_chart(fig_t4, use_container_width=True, config=CFG)


# ══════════════════════════════════════════════════════════════════════════════
# SALES REPORTING DIVISION CHARTS
# ══════════════════════════════════════════════════════════════════════════════
sec(ICO_DIV, "Sales Reporting Division Charts")
cd1, cd2 = st.columns(2)

with cd1:
    clabel("Revenue by Sales Reporting Division")
    div_chart = div_agg.sort_values("Total_Amt")
    bar_colors_div = [DIV_COLORS.get(d, RED) for d in div_chart["Sales_Reporting_Division"]]
    fig_d1 = go.Figure(go.Bar(
        x=div_chart["Total_Amt"], y=div_chart["Sales_Reporting_Division"], orientation="h",
        marker_color=bar_colors_div,
        text=[fmt_inr(v) for v in div_chart["Total_Amt"]],
        textposition="outside", textfont=dict(size=9, color=FONT),
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<br>SPOs: %{customdata}<extra></extra>",
        customdata=div_chart["SPO"],
    ))
    fig_d1.update_layout(**BASE_LAYOUT, height=380,
        xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
        yaxis=dict(showgrid=False, tickfont=dict(size=10)),
        margin=dict(l=8, r=80, t=16, b=8))
    st.plotly_chart(fig_d1, use_container_width=True, config=CFG)

with cd2:
    clabel("Sales Reporting Division — Apr vs May")
    fig_d2 = go.Figure()
    fig_d2.add_trace(go.Bar(name="Apr", x=div_agg["Sales_Reporting_Division"], y=div_agg["Amt_Apr"],
        marker_color="#990000", opacity=0.85,
        hovertemplate="<b>%{x}</b><br>Apr: ₹%{y:,.0f}<extra></extra>"))
    fig_d2.add_trace(go.Bar(name="May", x=div_agg["Sales_Reporting_Division"], y=div_agg["Amt_May"],
        marker_color=RED, opacity=0.85,
        hovertemplate="<b>%{x}</b><br>May: ₹%{y:,.0f}<extra></extra>"))
    fig_d2.update_layout(**BASE_LAYOUT, height=380, barmode="group",
        xaxis=dict(showgrid=False, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
        legend=dict(font=dict(size=9), bgcolor="rgba(20,20,20,0.8)", bordercolor="#333", borderwidth=1),
        margin=dict(l=8, r=8, t=16, b=8))
    st.plotly_chart(fig_d2, use_container_width=True, config=CFG)


# ══════════════════════════════════════════════════════════════════════════════
# SPO NAME-WISE SALES
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_SPO, "SPO Name-wise Sales")
c1, c2 = st.columns(2)

with c1:
    clabel("Top 20 SPOs by Total Revenue")
    top20 = spo_sum.head(20).sort_values("Total_Amt")
    fig1 = go.Figure(go.Bar(
        x=top20["Total_Amt"], y=top20["SPO"], orientation="h",
        marker=dict(color=top20["Total_Amt"].astype(float), colorscale=REDS, showscale=False),
        text=[fmt_inr(v) for v in top20["Total_Amt"]],
        textposition="outside", textfont=dict(size=8, color=FONT),
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
    ))
    fig1.update_layout(**BASE_LAYOUT, height=500,
        xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
        yaxis=dict(showgrid=False, tickfont=dict(size=8)),
        margin=dict(l=8, r=70, t=16, b=8))
    st.plotly_chart(fig1, use_container_width=True, config=CFG)

with c2:
    clabel("Revenue Share — Top 15 SPOs")
    top15 = spo_sum.head(15).copy()
    others_rev = spo_sum.iloc[15:]["Total_Amt"].sum() if len(spo_sum) > 15 else 0
    if others_rev > 0:
        top15 = pd.concat([top15, pd.DataFrame({"SPO":["Others"],"Total_Amt":[others_rev]})], ignore_index=True)
    fig2 = go.Figure(go.Pie(
        labels=top15["SPO"], values=top15["Total_Amt"].round(2), hole=0.52,
        marker=dict(colors=reds_pie[:len(top15)], line=dict(color="#111", width=2)),
        textinfo="label+percent", textfont=dict(size=8, color="#ddd"),
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>",
        insidetextorientation="radial",
    ))
    fig2.add_annotation(text=f"<b>{len(spo_sum)}</b><br>SPOs", x=0.5, y=0.5, showarrow=False,
        font=dict(size=14, color="#e0e0e0", family="Inter"))
    fig2.update_layout(**BASE_LAYOUT, height=500, showlegend=False, margin=DEFAULT_MARGIN)
    st.plotly_chart(fig2, use_container_width=True, config=CFG)


# ══════════════════════════════════════════════════════════════════════════════
# SPO MoM
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_TREND, "SPO Month-on-Month Analysis")
c3, c4 = st.columns(2)

with c3:
    clabel("Top 15 SPOs — Apr vs May Revenue")
    t15 = spo_sum.head(15).sort_values("Total_Amt")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name="Apr", x=t15["Amt_Apr"], y=t15["SPO"], orientation="h",
        marker_color="#990000", opacity=0.85,
        hovertemplate="<b>%{y}</b><br>Apr: ₹%{x:,.0f}<extra></extra>"))
    fig3.add_trace(go.Bar(name="May", x=t15["Amt_May"], y=t15["SPO"], orientation="h",
        marker_color=RED, opacity=0.85,
        hovertemplate="<b>%{y}</b><br>May: ₹%{x:,.0f}<extra></extra>"))
    fig3.update_layout(**BASE_LAYOUT, height=400, barmode="group",
        xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
        yaxis=dict(showgrid=False, tickfont=dict(size=8)),
        legend=dict(font=dict(size=9), bgcolor="rgba(20,20,20,0.8)", bordercolor="#333", borderwidth=1),
        margin=dict(l=8, r=8, t=16, b=8))
    st.plotly_chart(fig3, use_container_width=True, config=CFG)

with c4:
    clabel("Top 20 SPOs — MoM Revenue Growth %")
    mom_df = spo_sum.head(20).dropna(subset=["MoM_%"]).sort_values("MoM_%")
    bar_cols = ["#22c55e" if v >= 0 else RED for v in mom_df["MoM_%"]]
    fig4 = go.Figure(go.Bar(
        x=mom_df["MoM_%"], y=mom_df["SPO"], orientation="h",
        marker_color=bar_cols,
        text=mom_df["MoM_%"].apply(lambda x: f"{x:+.1f}%"),
        textposition="outside", textfont=dict(size=8, color=FONT),
        hovertemplate="<b>%{y}</b><br>MoM: %{x:+.1f}%<extra></extra>",
    ))
    fig4.update_layout(**BASE_LAYOUT, height=400,
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=True, zerolinecolor="#333", zerolinewidth=1),
        yaxis=dict(showgrid=False, tickfont=dict(size=8)),
        margin=dict(l=8, r=50, t=16, b=8))
    st.plotly_chart(fig4, use_container_width=True, config=CFG)


# ══════════════════════════════════════════════════════════════════════════════
# HQ-WISE SALES
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_HQ, "HQ-wise Sales Analysis")
c5, c6 = st.columns(2)

with c5:
    clabel("Top 25 HQs by Total Revenue")
    top25hq = hq_sum.head(25).sort_values("Total_Amt")
    fig5 = go.Figure(go.Bar(
        x=top25hq["Total_Amt"], y=top25hq["Corrected_HQ"], orientation="h",
        marker=dict(color=top25hq["Total_Amt"].astype(float), colorscale=GREENS, showscale=False),
        text=[fmt_inr(v) for v in top25hq["Total_Amt"]],
        textposition="outside", textfont=dict(size=8, color=FONT),
        customdata=top25hq[["SPO_Count","State","TEAM"]],
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<br>SPOs: %{customdata[0]}<br>State: %{customdata[1]}<br>TEAM: %{customdata[2]}<extra></extra>",
    ))
    fig5.update_layout(**BASE_LAYOUT, height=580,
        xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
        yaxis=dict(showgrid=False, tickfont=dict(size=8)),
        margin=dict(l=8, r=70, t=16, b=8))
    st.plotly_chart(fig5, use_container_width=True, config=CFG)

with c6:
    clabel("HQ Revenue Share — Top 15 HQs")
    top15hq = hq_sum.head(15).copy()
    others_hq_rev = hq_sum.iloc[15:]["Total_Amt"].sum() if len(hq_sum) > 15 else 0
    if others_hq_rev > 0:
        top15hq = pd.concat([top15hq, pd.DataFrame({"Corrected_HQ":["Others"],"Total_Amt":[others_hq_rev]})], ignore_index=True)
    fig6 = go.Figure(go.Pie(
        labels=top15hq["Corrected_HQ"], values=top15hq["Total_Amt"].round(2), hole=0.52,
        marker=dict(colors=greens_pie[:len(top15hq)], line=dict(color="#111", width=2)),
        textinfo="label+percent", textfont=dict(size=8, color="#ddd"),
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>",
        insidetextorientation="radial",
    ))
    fig6.add_annotation(text=f"<b>{len(hq_sum)}</b><br>HQs", x=0.5, y=0.5, showarrow=False,
        font=dict(size=14, color="#e0e0e0", family="Inter"))
    fig6.update_layout(**BASE_LAYOUT, height=580, showlegend=False, margin=DEFAULT_MARGIN)
    st.plotly_chart(fig6, use_container_width=True, config=CFG)


# ══════════════════════════════════════════════════════════════════════════════
# SPO DRILL-DOWN
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_SPO, "SPO Individual Drill-Down")
all_spo_list = sorted(df["SPO"].dropna().unique())
if len(all_spo_list) == 0:
    st.warning("No SPO data for current filters.")
else:
    selected_spo = st.selectbox("\U0001f50d Select an SPO / MR to explore:", all_spo_list, index=0)
    spo_df = df[df["SPO"] == selected_spo]
    spo_rev_val = spo_df["Total_Amt"].sum()
    spo_qty_val = spo_df["Total_Qty"].sum()
    spo_apr     = spo_df["Amt_Apr"].sum()
    spo_may     = spo_df["Amt_May"].sum()
    spo_hqs_cnt = spo_df["Corrected_HQ"].nunique()
    spo_prods   = spo_df["Product"].nunique()
    spo_state   = spo_df["State"].iloc[0] if len(spo_df) else "—"
    spo_mom     = round((spo_may - spo_apr) / spo_apr * 100, 1) if spo_apr else 0
    spo_mom_cls = "kpi-green" if spo_mom >= 0 else "kpi-red"
    spo_rank_rows = spo_sum[spo_sum["SPO"] == selected_spo]
    spo_rank    = spo_rank_rows.index[0] + 1 if len(spo_rank_rows) else "—"
    
    # Get TEAM and Reporting Division for this SPO
    spo_team = spo_df["TEAM"].iloc[0] if len(spo_df) and spo_df["TEAM"].notna().any() else "—"
    spo_srd  = spo_df["Sales_Reporting_Division"].iloc[0] if len(spo_df) and spo_df["Sales_Reporting_Division"].notna().any() else "—"

    dp1,dp2,dp3,dp4,dp5,dp6 = st.columns(6)
    kpi(dp1, ICO_REVENUE, "SPO Revenue",  fmt_inr(spo_rev_val),  f"Rank #{spo_rank}")
    kpi(dp2, ICO_QTY,     "Qty Sold",     f"{int(spo_qty_val):,}", "Total units")
    kpi(dp3, ICO_HQ,      "HQs Covered", f"{spo_hqs_cnt}",        spo_state)
    kpi(dp4, ICO_PRODUCT, "SKUs Sold",    f"{spo_prods}",          "Unique products")
    kpi(dp5, ICO_TEAM,    "TEAM",         spo_team[:25],           "From Employee Data")
    kpi(dp6, ICO_TREND,   "May Revenue",  fmt_inr(spo_may),        f"MoM: {spo_mom:+.1f}%", spo_mom_cls)
    
    # Show Sales Reporting Division badge
    st.markdown(f"""
    <div style='background:#1a1a1a;border:1px solid #2a2a2a;border-radius:8px;padding:8px 14px;margin:8px 0 4px 0;display:inline-block;'>
        <span style='font-size:0.65rem;font-weight:600;color:#555;letter-spacing:0.1em;text-transform:uppercase;'>Sales Reporting Division</span>
        <span style='font-size:0.8rem;font-weight:700;color:#f50f12;margin-left:12px;'>{spo_srd}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    dc1, dc2 = st.columns(2)
    with dc1:
        clabel(f"Top Products sold by {selected_spo[:30]}")
        spo_prod = (spo_df.groupby("Product", as_index=False)["Total_Amt"].sum()
                         .sort_values("Total_Amt", ascending=False).head(15).sort_values("Total_Amt"))
        fig_dp1 = go.Figure(go.Bar(
            x=spo_prod["Total_Amt"], y=spo_prod["Product"], orientation="h",
            marker=dict(color=spo_prod["Total_Amt"].astype(float), colorscale=REDS, showscale=False),
            text=[fmt_inr(v) for v in spo_prod["Total_Amt"]],
            textposition="outside", textfont=dict(size=8, color=FONT),
            hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
        ))
        fig_dp1.update_layout(**BASE_LAYOUT, height=360,
            xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
            yaxis=dict(showgrid=False, tickfont=dict(size=7)),
            margin=dict(l=8, r=70, t=16, b=8))
        st.plotly_chart(fig_dp1, use_container_width=True, config=CFG)
    with dc2:
        clabel(f"HQs covered by {selected_spo[:30]}")
        spo_hq_bd = (spo_df.groupby("Corrected_HQ", as_index=False)["Total_Amt"].sum()
                           .sort_values("Total_Amt", ascending=False).sort_values("Total_Amt"))
        fig_dp2 = go.Figure(go.Bar(
            x=spo_hq_bd["Total_Amt"], y=spo_hq_bd["Corrected_HQ"], orientation="h",
            marker=dict(color=spo_hq_bd["Total_Amt"].astype(float), colorscale=GREENS, showscale=False),
            text=[fmt_inr(v) for v in spo_hq_bd["Total_Amt"]],
            textposition="outside", textfont=dict(size=8, color=FONT),
            hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
        ))
        fig_dp2.update_layout(**BASE_LAYOUT, height=360,
            xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
            yaxis=dict(showgrid=False, tickfont=dict(size=8)),
            margin=dict(l=8, r=70, t=16, b=8))
        st.plotly_chart(fig_dp2, use_container_width=True, config=CFG)


# ══════════════════════════════════════════════════════════════════════════════
# HQ DRILL-DOWN
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_HQ, "HQ Individual Drill-Down")
all_hq_list = sorted(df["Corrected_HQ"].dropna().unique())
if len(all_hq_list) > 0:
    selected_hq = st.selectbox("\U0001f50d Select an HQ to explore:", all_hq_list, index=0)
    hq_df = df[df["Corrected_HQ"] == selected_hq]
    hq_rev_val  = hq_df["Total_Amt"].sum()
    hq_qty_val  = hq_df["Total_Qty"].sum()
    hq_apr      = hq_df["Amt_Apr"].sum()
    hq_may      = hq_df["Amt_May"].sum()
    hq_spo_cnt  = hq_df["SPO"].nunique()
    hq_prods    = hq_df["Product"].nunique()
    hq_state    = hq_df["State"].iloc[0] if len(hq_df) else "—"
    hq_mom      = round((hq_may - hq_apr) / hq_apr * 100, 1) if hq_apr else 0
    hq_mom_cls  = "kpi-green" if hq_mom >= 0 else "kpi-red"
    hq_rank_rows = hq_sum[hq_sum["Corrected_HQ"] == selected_hq]
    hq_rank     = hq_rank_rows.index[0] + 1 if len(hq_rank_rows) else "—"
    
    # Get TEAMs for this HQ
    hq_teams = ", ".join(sorted(set(t.strip() for t in ", ".join(hq_df["TEAM"].dropna().unique()).split(",") if t.strip()))) if hq_df["TEAM"].notna().any() else "—"

    hq1,hq2,hq3,hq4,hq5,hq6 = st.columns(6)
    kpi(hq1, ICO_REVENUE, "HQ Revenue",   fmt_inr(hq_rev_val),   f"Rank #{hq_rank}")
    kpi(hq2, ICO_QTY,     "Qty Sold",     f"{int(hq_qty_val):,}", "Total units")
    kpi(hq3, ICO_SPO,     "Active SPOs",  f"{hq_spo_cnt}",        hq_state)
    kpi(hq4, ICO_PRODUCT, "SKUs Sold",    f"{hq_prods}",          "Unique products")
    kpi(hq5, ICO_TEAM,    "TEAMs",        hq_teams[:25],         "From Employee Data")
    kpi(hq6, ICO_TREND,   "May Revenue",  fmt_inr(hq_may),        f"MoM: {hq_mom:+.1f}%", hq_mom_cls)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    hqc1, hqc2 = st.columns(2)
    with hqc1:
        clabel(f"SPOs operating in {selected_hq}")
        hq_spo_bd = (hq_df.groupby("SPO", as_index=False)["Total_Amt"].sum()
                          .sort_values("Total_Amt", ascending=False).sort_values("Total_Amt"))
        fig_hq1 = go.Figure(go.Bar(
            x=hq_spo_bd["Total_Amt"], y=hq_spo_bd["SPO"], orientation="h",
            marker=dict(color=hq_spo_bd["Total_Amt"].astype(float), colorscale=REDS, showscale=False),
            text=[fmt_inr(v) for v in hq_spo_bd["Total_Amt"]],
            textposition="outside", textfont=dict(size=8, color=FONT),
            hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
        ))
        fig_hq1.update_layout(**BASE_LAYOUT, height=360,
            xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
            yaxis=dict(showgrid=False, tickfont=dict(size=8)),
            margin=dict(l=8, r=70, t=16, b=8))
        st.plotly_chart(fig_hq1, use_container_width=True, config=CFG)
    with hqc2:
        clabel(f"Top Products in {selected_hq}")
        hq_prod_bd = (hq_df.groupby("Product", as_index=False)["Total_Amt"].sum()
                           .sort_values("Total_Amt", ascending=False).head(15).sort_values("Total_Amt"))
        fig_hq2 = go.Figure(go.Bar(
            x=hq_prod_bd["Total_Amt"], y=hq_prod_bd["Product"], orientation="h",
            marker=dict(color=hq_prod_bd["Total_Amt"].astype(float), colorscale=GREENS, showscale=False),
            text=[fmt_inr(v) for v in hq_prod_bd["Total_Amt"]],
            textposition="outside", textfont=dict(size=8, color=FONT),
            hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
        ))
        fig_hq2.update_layout(**BASE_LAYOUT, height=360,
            xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
            yaxis=dict(showgrid=False, tickfont=dict(size=7)),
            margin=dict(l=8, r=70, t=16, b=8))
        st.plotly_chart(fig_hq2, use_container_width=True, config=CFG)


# ══════════════════════════════════════════════════════════════════════════════
# SCATTER
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_PERF, "Revenue vs Qty — Scatter View")
c9, c10 = st.columns(2)
with c9:
    clabel("SPO Revenue vs Qty Sold (bubble = revenue size)")
    max_r = spo_sum["Total_Amt"].max() or 1
    sizes = (spo_sum["Total_Amt"] / max_r * 28 + 5).astype(float)
    fig_sc1 = go.Figure(go.Scatter(
        x=spo_sum["Total_Qty"], y=spo_sum["Total_Amt"], mode="markers",
        text=spo_sum["SPO"].apply(lambda x: x[:18]+"\u2026" if len(x)>18 else x),
        marker=dict(size=sizes, color=spo_sum["Total_Amt"].astype(float),
                    colorscale=REDS, showscale=False,
                    line=dict(color="rgba(255,255,255,0.12)", width=1)),
        hovertemplate="<b>%{text}</b><br>Qty: %{x:,}<br>Revenue: ₹%{y:,.0f}<extra></extra>",
    ))
    fig_sc1.update_layout(**BASE_LAYOUT, height=360, margin=DEFAULT_MARGIN,
        xaxis=dict(showgrid=True, gridcolor=GRID, title=dict(text="Sales Qty", font=dict(size=10))),
        yaxis=dict(showgrid=True, gridcolor=GRID, title=dict(text="Revenue (₹)", font=dict(size=10))))
    st.plotly_chart(fig_sc1, use_container_width=True, config=CFG)
with c10:
    clabel("HQ Revenue vs SPO Count (bubble = revenue size)")
    max_hr = hq_sum["Total_Amt"].max() or 1
    hq_sizes = (hq_sum["Total_Amt"] / max_hr * 28 + 5).astype(float)
    fig_sc2 = go.Figure(go.Scatter(
        x=hq_sum["SPO_Count"], y=hq_sum["Total_Amt"], mode="markers",
        text=hq_sum["Corrected_HQ"].apply(lambda x: x[:18]+"\u2026" if len(x)>18 else x),
        marker=dict(size=hq_sizes, color=hq_sum["Total_Amt"].astype(float),
                    colorscale=GREENS, showscale=False,
                    line=dict(color="rgba(255,255,255,0.12)", width=1)),
        hovertemplate="<b>%{text}</b><br>SPOs: %{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>",
    ))
    fig_sc2.update_layout(**BASE_LAYOUT, height=360, margin=DEFAULT_MARGIN,
        xaxis=dict(showgrid=True, gridcolor=GRID, title=dict(text="Active SPO Count", font=dict(size=10))),
        yaxis=dict(showgrid=True, gridcolor=GRID, title=dict(text="Revenue (₹)", font=dict(size=10))))
    st.plotly_chart(fig_sc2, use_container_width=True, config=CFG)


# ══════════════════════════════════════════════════════════════════════════════
# SPO RANKING TABLE (with TEAM & Sales Reporting Division)
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_TABLE, "SPO Full Ranking Table (with TEAM & Reporting Division)")
tbl = spo_sum.copy().reset_index(drop=True)
tbl.insert(0, "#", range(1, len(tbl)+1))
tbl["Revenue"] = tbl["Total_Amt"].apply(fmt_inr)
tbl["Qty"]     = tbl["Total_Qty"].apply(lambda x: f"{int(x):,}")
tbl["Apr Rev"] = tbl["Amt_Apr"].apply(fmt_inr)
tbl["May Rev"] = tbl["Amt_May"].apply(fmt_inr)
tbl["MoM %"]   = tbl["MoM_%"].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else "—")

# Clean TEAM column for display
tbl["TEAM_Clean"] = tbl["TEAM"].str.replace(r"\(Unmapped\)", "", regex=True).str.strip(", ").str.strip()

display_tbl = tbl[["#","SPO","HQ","TEAM_Clean","Sales_Reporting_Division","State","Apr Rev","May Rev","Revenue","Qty","Products","MoM %"]].copy()
display_tbl.columns = ["#","SPO / MR","HQ","TEAM","Reporting Division","State","Apr Rev","May Rev","Total Rev","Qty Sold","SKUs","MoM %"]
st.dataframe(display_tbl, use_container_width=True, height=420, hide_index=True,
    column_config={
        "#":         st.column_config.NumberColumn("#", width="small"),
        "SPO / MR":  st.column_config.TextColumn("SPO / MR"),
        "HQ":        st.column_config.TextColumn("HQ", width="small"),
        "TEAM":      st.column_config.TextColumn("TEAM", width="medium"),
        "Reporting Division": st.column_config.TextColumn("Reporting Division", width="small"),
        "State":     st.column_config.TextColumn("State", width="small"),
        "Apr Rev":   st.column_config.TextColumn("Apr Rev", width="small"),
        "May Rev":   st.column_config.TextColumn("May Rev", width="small"),
        "Total Rev": st.column_config.TextColumn("Total Rev", width="small"),
        "Qty Sold":  st.column_config.TextColumn("Qty Sold", width="small"),
        "SKUs":      st.column_config.NumberColumn("SKUs", width="small"),
        "MoM %":     st.column_config.TextColumn("MoM %", width="small"),
    })


# ══════════════════════════════════════════════════════════════════════════════
# TEAM RANKING TABLE
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_TEAM, "TEAM Ranking Table")
if len(team_agg) > 0:
    team_tbl = team_agg.copy().reset_index(drop=True)
    team_tbl.insert(0, "#", range(1, len(team_tbl)+1))
    team_tbl["Revenue"] = team_tbl["Total_Amt"].apply(fmt_inr)
    team_tbl["Qty"]     = team_tbl["Total_Qty"].apply(lambda x: f"{int(x):,}")
    team_tbl["Apr Rev"] = team_tbl["Amt_Apr"].apply(fmt_inr)
    team_tbl["May Rev"] = team_tbl["Amt_May"].apply(fmt_inr)
    team_tbl["MoM %"]   = team_tbl["MoM_%"].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else "—")
    
    team_display = team_tbl[["#","TEAM","SPO","Corrected_HQ","Apr Rev","May Rev","Revenue","Qty","Product","MoM %"]].copy()
    team_display.columns = ["#","TEAM","SPO Count","HQ Count","Apr Rev","May Rev","Total Rev","Qty Sold","Products","MoM %"]
    st.dataframe(team_display, use_container_width=True, height=400, hide_index=True,
        column_config={
            "#":         st.column_config.NumberColumn("#", width="small"),
            "TEAM":      st.column_config.TextColumn("TEAM", width="large"),
            "SPO Count": st.column_config.NumberColumn("SPOs", width="small"),
            "HQ Count":  st.column_config.NumberColumn("HQs", width="small"),
            "Apr Rev":   st.column_config.TextColumn("Apr Rev", width="small"),
            "May Rev":   st.column_config.TextColumn("May Rev", width="small"),
            "Total Rev": st.column_config.TextColumn("Total Rev", width="small"),
            "Qty Sold":  st.column_config.TextColumn("Qty", width="small"),
            "Products":  st.column_config.NumberColumn("Products", width="small"),
            "MoM %":     st.column_config.TextColumn("MoM %", width="small"),
        })


# ══════════════════════════════════════════════════════════════════════════════
# HQ RANKING TABLE
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_TABLE, "HQ Full Ranking Table")
hq_tbl = hq_sum.copy().reset_index(drop=True)
hq_tbl.insert(0, "#", range(1, len(hq_tbl)+1))
hq_tbl["Revenue"] = hq_tbl["Total_Amt"].apply(fmt_inr)
hq_tbl["Qty"]     = hq_tbl["Total_Qty"].apply(lambda x: f"{int(x):,}")
hq_tbl["Apr Rev"] = hq_tbl["Amt_Apr"].apply(fmt_inr)
hq_tbl["May Rev"] = hq_tbl["Amt_May"].apply(fmt_inr)
hq_tbl["MoM %"]   = hq_tbl["MoM_%"].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else "—")
display_hq = hq_tbl[["#","Corrected_HQ","State","SPO_Count","TEAM","Apr Rev","May Rev","Revenue","Qty","Products","MoM %"]].copy()
display_hq.columns = ["#","HQ","State","Active SPOs","TEAM","Apr Rev","May Rev","Total Rev","Qty Sold","SKUs","MoM %"]
st.dataframe(display_hq, use_container_width=True, height=400, hide_index=True,
    column_config={
        "#":           st.column_config.NumberColumn("#", width="small"),
        "HQ":          st.column_config.TextColumn("HQ"),
        "State":       st.column_config.TextColumn("State", width="small"),
        "Active SPOs": st.column_config.NumberColumn("SPOs", width="small"),
        "TEAM":        st.column_config.TextColumn("TEAM", width="medium"),
        "Apr Rev":     st.column_config.TextColumn("Apr Rev", width="small"),
        "May Rev":     st.column_config.TextColumn("May Rev", width="small"),
        "Total Rev":   st.column_config.TextColumn("Total Rev", width="small"),
        "Qty Sold":    st.column_config.TextColumn("Qty", width="small"),
        "SKUs":        st.column_config.NumberColumn("SKUs", width="small"),
        "MoM %":       st.column_config.TextColumn("MoM %", width="small"),
    })


# ══════════════════════════════════════════════════════════════════════════════
# RAW DATA + CSV
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("\U0001f50d Raw Data Preview (filtered)", expanded=False):
    st.dataframe(df.head(500), use_container_width=True, hide_index=True)

csv_bytes = df.to_csv(index=False).encode("utf-8")
st.download_button("\u2b07\ufe0f Download Filtered Data (CSV)", csv_bytes, "ENTOD_SPO_TEAM_Filtered.csv", "text/csv")
st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
st.caption("ENTOD SPO-Wise + TEAM Analytics · Apr–May 2026 · Powered by Streamlit")
