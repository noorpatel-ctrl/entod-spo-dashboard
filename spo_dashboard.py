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
ICO_STATE    = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M9 3L3 6v15l6-3 6 3 6-3V3l-6 3-6-3Z'/><path stroke-linecap='round' d='M9 3v15m6-12v15'/>")

SICO_SPO     = _svg("<path stroke-linecap='round' stroke-linejoin='round' d='M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z'/>", w=15, sw="1.8")
SICO_PERF    = _svg("<path stroke-linecap='round' d='M6 3h12M6 3v6a6 6 0 0 0 12 0V3M6 3H4a2 2 0 0 0 0 4h2m12 0h2a2 2 0 0 0 0-4h-2m-6 12v3m0 0H9m3 0h3'/>", w=15, sw="1.8")
SICO_TREND   = _svg("<path stroke-linecap='round' d='M3 17l5-5 4 4 9-9M21 7h-4V3'/>", w=15, sw="1.8")
SICO_TABLE   = _svg("<rect x='3' y='3' width='18' height='18' rx='2'/><path stroke-linecap='round' d='M3 9h18M9 9v12'/>", w=15, sw="1.8")
SICO_DIV     = _svg("<rect x='8' y='2' width='8' height='4' rx='1'/><rect x='3' y='4' width='18' height='17' rx='2'/><path stroke-linecap='round' d='M8 11h8M8 15h5'/>", w=15, sw="1.8")
SICO_KPI     = _svg("<path stroke-linecap='round' d='M3 3v18h18'/><path stroke-linecap='round' d='M7 16l4-4 4 4 4-6'/>", w=15, sw="1.8")

# ── LOGO (base64 embedded) ─────────────────────────────────────────────────────
LOGO_SRC = "data:image/png;base64,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"

# ── CSS ────────────────────────────────────────────────────────────────────────
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
.kpi-value.sm { font-size:1.1rem; }
.kpi-sub { font-size:0.65rem; color:#555; }
.kpi-green { color:#22c55e !important; }
.kpi-red { color:#f50f12 !important; }
.sec-hdr { display:flex; align-items:center; gap:8px; margin:28px 0 12px 0; padding-bottom:8px; border-bottom:1px solid #2a2a2a; }
.sec-hdr span { font-size:0.95rem; font-weight:700; color:#e0e0e0; letter-spacing:0.01em; }
.chart-label { font-size:0.75rem; color:#666; margin-bottom:4px; font-weight:500; letter-spacing:0.02em; }
[data-testid="stSidebar"] { background:#111 !important; border-right:1px solid #1f1f1f !important; min-width:200px !important; max-width:200px !important; width:200px !important; }
[data-testid="stSidebar"] > div:first-child { width:200px !important; padding:0.75rem 0.65rem !important; }
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
[data-testid="stDataFrame"] table td:first-child,
[data-testid="stDataFrame"] table th:first-child { text-align:center; }
.stMultiSelect, .stDownloadButton { margin-bottom:2px; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
def fmt_inr(val):
    if val >= 1e7:  return f"₹{val/1e7:.2f} Cr"
    if val >= 1e5:  return f"₹{val/1e5:.1f} L"
    return f"₹{val:,.0f}"

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
BASE_LAYOUT = dict(
    paper_bgcolor=PAPER, plot_bgcolor=BG,
    font=dict(color=FONT, family="Inter", size=11),
    hoverlabel=dict(bgcolor="#1a1a1a", bordercolor="#333", font=dict(color="#eee", size=12)),
)
DEFAULT_MARGIN = dict(l=8, r=8, t=16, b=8)
CFG = {"displayModeBar":True,"displaylogo":False,
       "modeBarButtonsToRemove":["select2d","lasso2d","toggleSpikelines","hoverClosestCartesian","hoverCompareCartesian"],
       "toImageButtonOptions":{"format":"png","filename":"ENTOD_SPO","height":600,"width":1200,"scale":2}}

# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING  — reads Sales_HQ_SPO_Mapped_AprMay2026_Fixed.xlsx
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner="⏳ Loading ENTOD SPO Data…", ttl=3600)
def load_data():
    import os
    fname = "Sales_HQ_SPO_Mapped_AprMay2026_Fixed.xlsx"
    if not os.path.exists(fname):
        return None, None
    # Raw detail sheet → row-level data for full analysis
    raw = pd.read_excel(fname, sheet_name="Raw Mapped Detail", header=2, skiprows=[3])
    raw.columns = ["State","Corrected_HQ","Orig_HQ","SPO","Division","Product","Pack",
                   "Qty_Apr","Amt_Apr","Qty_May","Amt_May","Total_Qty","Total_Amt"]
    raw = raw.dropna(subset=["SPO","Division"])
    raw["SPO"] = raw["SPO"].astype(str).str.strip()
    raw["Division"] = raw["Division"].astype(str).str.strip()

    # Non-covering sheet
    nc = pd.read_excel(fname, sheet_name="Non-Covering HQs", header=2, skiprows=[3])
    nc.columns = ["Division","Orig_HQ","Qty_Apr","Amt_Apr","Qty_May","Amt_May","Total_Qty","Total_Amt"]
    nc = nc.dropna(subset=["Division"])
    nc["Division"] = nc["Division"].astype(str).str.strip()
    nc = nc[nc["Division"] != "TOTAL"]
    return raw, nc

raw_full, nc_full = load_data()
if raw_full is None:
    st.error("❌ Data file not found. Place **Sales_HQ_SPO_Mapped_AprMay2026_Fixed.xlsx** in the same folder as this app.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR FILTERS
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div class="sb-logo-wrap">
      <img src="{LOGO_SRC}" alt="ENTOD Logo"/>
      <div>
        <div class="sb-brand-name">ENTOD SPO Insight</div>
        <div class="sb-brand-sub">SPO-Wise Analytics</div>
      </div>
    </div>
    <div style='border-bottom:1px solid #222; margin-bottom:14px;'></div>
    """, unsafe_allow_html=True)
    st.markdown("**Filters**")

    all_divs  = sorted(raw_full["Division"].dropna().unique())
    sel_divs  = st.multiselect("🏢 Division", all_divs, default=[], placeholder="All divisions")

    all_states = sorted(raw_full["State"].dropna().unique())
    sel_states = st.multiselect("🗺️ State", all_states, default=[], placeholder="All states")

    all_hqs   = sorted(raw_full["Corrected_HQ"].dropna().unique())
    sel_hqs   = st.multiselect("📍 HQ", all_hqs, default=[], placeholder="All HQs")

    all_prods = sorted(raw_full["Product"].dropna().unique())
    sel_prods = st.multiselect("💊 Product", all_prods, default=[], placeholder="All products")

    st.markdown("<div style='border-bottom:1px solid #222; margin:14px 0 10px 0;'></div>", unsafe_allow_html=True)
    st.caption(f"📊 Total SPOs: **{raw_full['SPO'].nunique():,}**")
    st.caption("ℹ️ Leave blank to include all.")

# ── Apply filters ──────────────────────────────────────────────────────────────
df = raw_full.copy()
if sel_divs:   df = df[df["Division"].isin(sel_divs)]
if sel_states: df = df[df["State"].isin(sel_states)]
if sel_hqs:    df = df[df["Corrected_HQ"].isin(sel_hqs)]
if sel_prods:  df = df[df["Product"].isin(sel_prods)]

nc_df = nc_full.copy()
if sel_divs:   nc_df = nc_df[nc_df["Division"].isin(sel_divs)]

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
c_logo, c_title = st.columns([1, 10])
with c_logo:
    st.markdown(f"<img src='{LOGO_SRC}' style='width:62px;height:62px;border-radius:10px;margin-top:4px;'>",
                unsafe_allow_html=True)
with c_title:
    filter_txt = " | ".join(
        ([f"Div: {', '.join(sel_divs)}" if sel_divs else ""] +
         [f"State: {', '.join(sel_states)}" if sel_states else ""] +
         [f"HQ: {', '.join(sel_hqs)}" if sel_hqs else ""])
    ).strip(" | ") or "All Divisions · All States · All HQs"
    st.markdown(f"""
    <div style='padding-top:6px;'>
      <div style='font-size:1.55rem;font-weight:800;color:#f0f0f0;letter-spacing:-0.02em;'>
        ENTOD SPO-Wise Sales Analytics &nbsp;
        <span style='font-size:0.85rem;font-weight:500;color:#555;'>Apr–May 2026</span>
      </div>
      <div style='font-size:0.72rem;color:#555;margin-top:2px;'>{filter_txt}</div>
    </div>""", unsafe_allow_html=True)

# ── Ticker ─────────────────────────────────────────────────────────────────────
total_rev = df["Total_Amt"].sum()
total_qty = df["Total_Qty"].sum()
n_spos    = df["SPO"].nunique()
n_hqs     = df["Corrected_HQ"].nunique()
n_prods   = df["Product"].nunique()
n_states  = df["State"].nunique()
ticker_items = [
    f"💰 Total Revenue: {fmt_inr(total_rev)}",
    f"📦 Total Qty Sold: {int(total_qty):,}",
    f"👤 Active SPOs: {n_spos}",
    f"📍 HQs Covered: {n_hqs}",
    f"💊 Products: {n_prods}",
    f"🗺️ States: {n_states}",
]
ticker_str = "  ·  ".join(ticker_items * 3)
st.markdown(f"<div class='ticker-outer'><div class='ticker-inner'>{ticker_str}</div></div>",
            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_KPI, "Key Metrics")

spo_rev = df.groupby("SPO")["Total_Amt"].sum()
avg_spo_rev = spo_rev.mean() if len(spo_rev) else 0
top_spo = spo_rev.idxmax() if len(spo_rev) else "—"
top_spo_rev = spo_rev.max() if len(spo_rev) else 0
rev_apr = df["Amt_Apr"].sum()
rev_may = df["Amt_May"].sum()
mom_pct = round((rev_may - rev_apr) / rev_apr * 100, 1) if rev_apr else 0
mom_cls = "kpi-green" if mom_pct >= 0 else "kpi-red"
mom_str = f"{mom_pct:+.1f}%"

nc_total = nc_df["Total_Amt"].sum()
nc_hqs   = nc_df["Orig_HQ"].nunique()

k1, k2, k3, k4, k5, k6 = st.columns(6)
kpi(k1, ICO_REVENUE, "Total Revenue",    fmt_inr(total_rev),   "Apr + May 2026")
kpi(k2, ICO_QTY,     "Total Qty Sold",   f"{int(total_qty):,}", "All products")
kpi(k3, ICO_SPO,     "Active SPOs",      f"{n_spos}",           "Mapped & covered")
kpi(k4, ICO_HQ,      "HQs Covered",      f"{n_hqs}",            "Corrected HQs")
kpi(k5, ICO_TREND,   "Apr vs May MoM",   mom_str,               f"Apr ₹{rev_apr/1e5:.1f}L → May ₹{rev_may/1e5:.1f}L", mom_cls)
kpi(k6, ICO_DIV,     "Non-Covering Rev", fmt_inr(nc_total),     f"{nc_hqs} non-covering HQs")

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

k7, k8, k9, k10, k11, k12 = st.columns(6)
kpi(k7,  ICO_PRODUCT, "Products Sold",     f"{n_prods}",          "Unique SKUs")
kpi(k8,  ICO_STATE,   "States Covered",    f"{n_states}",         "Active states")
kpi(k9,  ICO_SPO,     "Avg Rev / SPO",     fmt_inr(avg_spo_rev),  "Per MR")
kpi(k10, ICO_REVENUE, "Top SPO Revenue",   fmt_inr(top_spo_rev),  f"{top_spo[:16]}…" if len(str(top_spo))>16 else str(top_spo))
kpi(k11, ICO_QTY,     "Apr Revenue",       fmt_inr(rev_apr),      "April 2026")
kpi(k12, ICO_TREND,   "May Revenue",       fmt_inr(rev_may),      "May 2026")

# ══════════════════════════════════════════════════════════════════════════════
# SPO SUMMARY TABLE
# ══════════════════════════════════════════════════════════════════════════════
spo_sum = (
    df.groupby("SPO", as_index=False)
      .agg(
          Corrected_HQ = ("Corrected_HQ", "first"),
          Division     = ("Division",    lambda x: ", ".join(sorted(x.unique()))),
          State        = ("State",        "first"),
          Qty_Apr      = ("Qty_Apr",      "sum"),
          Amt_Apr      = ("Amt_Apr",      "sum"),
          Qty_May      = ("Qty_May",      "sum"),
          Amt_May      = ("Amt_May",      "sum"),
          Total_Qty    = ("Total_Qty",    "sum"),
          Total_Amt    = ("Total_Amt",    "sum"),
          Products     = ("Product",      "nunique"),
      )
      .sort_values("Total_Amt", ascending=False)
      .reset_index(drop=True)
)
spo_sum["MoM_%"] = spo_sum.apply(
    lambda r: round((r["Amt_May"] - r["Amt_Apr"]) / r["Amt_Apr"] * 100, 1)
    if r["Amt_Apr"] > 0 else None, axis=1)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 1 : Top 20 SPOs bar  +  SPO Revenue Share donut
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_PERF, "SPO Performance Overview")

c1, c2 = st.columns(2)

with c1:
    clabel("Top 20 SPOs by Total Revenue")
    top20 = spo_sum.head(20).sort_values("Total_Amt")
    fig1 = go.Figure(go.Bar(
        x=top20["Total_Amt"], y=top20["SPO"], orientation="h",
        marker=dict(color=top20["Total_Amt"].astype(float), colorscale=REDS, showscale=False),
        text=[fmt_inr(v) for v in top20["Total_Amt"]],
        textposition="outside", textfont=dict(size=8, color=FONT),
        hovertemplate="<b>%{y}</b><br>%{x:,.0f}<extra></extra>",
    ))
    fig1.update_layout(**BASE_LAYOUT, height=480,
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
    reds_pie = [RED,"#cc0000","#ff4444","#990000","#ff6666",
                "#800000","#ff8080","#660000","#ffaaaa","#4d0000",
                "#ff2222","#aa0000","#ff5555","#770000","#ff9999","#333333"]
    fig2 = go.Figure(go.Pie(
        labels=top15["SPO"], values=top15["Total_Amt"].round(2),
        hole=0.52,
        marker=dict(colors=reds_pie[:len(top15)], line=dict(color="#111", width=2)),
        textinfo="label+percent", textfont=dict(size=8, color="#ddd"),
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>",
        insidetextorientation="radial",
    ))
    fig2.add_annotation(text=f"<b>{len(spo_sum)}</b><br>SPOs",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=14, color="#e0e0e0", family="Inter"))
    fig2.update_layout(**BASE_LAYOUT, height=480, showlegend=False, margin=DEFAULT_MARGIN)
    st.plotly_chart(fig2, use_container_width=True, config=CFG)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 2 : Apr vs May bar (top 15)  +  MoM % bar (top 20)
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_TREND, "Month-on-Month Analysis")

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
    fig3.update_layout(**BASE_LAYOUT, height=380, barmode="group",
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
    fig4.update_layout(**BASE_LAYOUT, height=380,
        xaxis=dict(showgrid=True, gridcolor=GRID,
                   zeroline=True, zerolinecolor="#333", zerolinewidth=1),
        yaxis=dict(showgrid=False, tickfont=dict(size=8)),
        margin=dict(l=8, r=50, t=16, b=8))
    st.plotly_chart(fig4, use_container_width=True, config=CFG)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 3 : Division-wise SPO breakdown  +  Top SPOs by Qty
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_DIV, "Division & Quantity Analysis")

c5, c6 = st.columns(2)

with c5:
    clabel("Revenue by Division")
    div_sum = (df.groupby("Division", as_index=False)["Total_Amt"].sum()
                 .sort_values("Total_Amt", ascending=False))
    fig5 = go.Figure(go.Bar(
        x=div_sum["Total_Amt"], y=div_sum["Division"], orientation="h",
        marker=dict(color=div_sum["Total_Amt"].astype(float), colorscale=REDS, showscale=False),
        text=[fmt_inr(v) for v in div_sum["Total_Amt"]],
        textposition="outside", textfont=dict(size=9, color=FONT),
        hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
    ))
    fig5.update_layout(**BASE_LAYOUT, height=300,
        xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
        yaxis=dict(showgrid=False),
        margin=dict(l=8, r=70, t=16, b=8))
    st.plotly_chart(fig5, use_container_width=True, config=CFG)

with c6:
    clabel("Top 20 SPOs by Qty Sold")
    top20q = spo_sum.sort_values("Total_Qty", ascending=False).head(20).sort_values("Total_Qty")
    fig6 = go.Figure(go.Bar(
        x=top20q["Total_Qty"], y=top20q["SPO"], orientation="h",
        marker=dict(color=top20q["Total_Qty"].astype(float), colorscale=REDS, showscale=False),
        text=top20q["Total_Qty"].apply(lambda x: f"{int(x):,}"),
        textposition="outside", textfont=dict(size=8, color=FONT),
        hovertemplate="<b>%{y}</b><br>Qty: %{x:,}<extra></extra>",
    ))
    fig6.update_layout(**BASE_LAYOUT, height=300,
        xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=","),
        yaxis=dict(showgrid=False, tickfont=dict(size=8)),
        margin=dict(l=8, r=60, t=16, b=8))
    st.plotly_chart(fig6, use_container_width=True, config=CFG)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 4 : Revenue vs Qty bubble  +  HQ-wise SPO count
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_SPO, "SPO Scatter & HQ Coverage")

c7, c8 = st.columns(2)

with c7:
    clabel("Revenue vs Qty — Bubble Chart (size = revenue)")
    max_r = spo_sum["Total_Amt"].max() or 1
    sizes = (spo_sum["Total_Amt"] / max_r * 28 + 5).astype(float)
    fig7 = go.Figure(go.Scatter(
        x=spo_sum["Total_Qty"], y=spo_sum["Total_Amt"],
        mode="markers",
        text=spo_sum["SPO"].apply(lambda x: x[:16]+"…" if len(x)>16 else x),
        marker=dict(size=sizes, color=spo_sum["Total_Amt"].astype(float),
                    colorscale=REDS, showscale=False,
                    line=dict(color="rgba(255,255,255,0.12)", width=1)),
        hovertemplate="<b>%{text}</b><br>Qty: %{x:,}<br>Revenue: ₹%{y:,.0f}<extra></extra>",
    ))
    fig7.update_layout(**BASE_LAYOUT, height=340, margin=DEFAULT_MARGIN,
        xaxis=dict(showgrid=True, gridcolor=GRID, title=dict(text="Sales Qty", font=dict(size=10))),
        yaxis=dict(showgrid=True, gridcolor=GRID, title=dict(text="Revenue (₹)", font=dict(size=10))))
    st.plotly_chart(fig7, use_container_width=True, config=CFG)

with c8:
    clabel("Top 20 HQs by Revenue (Covered SPOs)")
    hq_sum = (df.groupby("Corrected_HQ", as_index=False)["Total_Amt"].sum()
                .sort_values("Total_Amt", ascending=False).head(20).sort_values("Total_Amt"))
    fig8 = go.Figure(go.Bar(
        x=hq_sum["Total_Amt"], y=hq_sum["Corrected_HQ"], orientation="h",
        marker=dict(color=hq_sum["Total_Amt"].astype(float), colorscale=REDS, showscale=False),
        text=[fmt_inr(v) for v in hq_sum["Total_Amt"]],
        textposition="outside", textfont=dict(size=8, color=FONT),
        hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
    ))
    fig8.update_layout(**BASE_LAYOUT, height=340,
        xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
        yaxis=dict(showgrid=False, tickfont=dict(size=8)),
        margin=dict(l=8, r=70, t=16, b=8))
    st.plotly_chart(fig8, use_container_width=True, config=CFG)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 5 : Non-Covering HQs bar  +  Division donut
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_TABLE, "Non-Covering & Division View")

c9, c10 = st.columns(2)

with c9:
    clabel("Non-Covering HQs by Revenue")
    nc_plot = nc_df.groupby("Orig_HQ", as_index=False)["Total_Amt"].sum()
    nc_plot = nc_plot.sort_values("Total_Amt", ascending=False).head(20).sort_values("Total_Amt")
    if len(nc_plot):
        fig9 = go.Figure(go.Bar(
            x=nc_plot["Total_Amt"], y=nc_plot["Orig_HQ"], orientation="h",
            marker_color="#cc2200",
            text=[fmt_inr(v) for v in nc_plot["Total_Amt"]],
            textposition="outside", textfont=dict(size=8, color=FONT),
            hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
        ))
        fig9.update_layout(**BASE_LAYOUT, height=320,
            xaxis=dict(showgrid=True, gridcolor=GRID, tickformat=",.0f"),
            yaxis=dict(showgrid=False, tickfont=dict(size=8)),
            margin=dict(l=8, r=70, t=16, b=8))
        st.plotly_chart(fig9, use_container_width=True, config=CFG)
    else:
        st.info("No non-covering data for selected filters.")

with c10:
    clabel("Division Revenue Share")
    div_pie = df.groupby("Division", as_index=False)["Total_Amt"].sum().sort_values("Total_Amt", ascending=False)
    fig10 = go.Figure(go.Pie(
        labels=div_pie["Division"], values=div_pie["Total_Amt"].round(2),
        hole=0.50,
        marker=dict(colors=reds_pie[:len(div_pie)], line=dict(color="#111", width=2)),
        textinfo="label+percent", textfont=dict(size=9, color="#ddd"),
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>",
    ))
    fig10.add_annotation(text="Divisions", x=0.5, y=0.5, showarrow=False,
        font=dict(size=11, color="#e0e0e0", family="Inter"))
    fig10.update_layout(**BASE_LAYOUT, height=320, showlegend=True,
        legend=dict(font=dict(size=9), bgcolor="rgba(20,20,20,0.8)",
                    bordercolor="#333", borderwidth=1, x=1, y=1),
        margin=DEFAULT_MARGIN)
    st.plotly_chart(fig10, use_container_width=True, config=CFG)

# ══════════════════════════════════════════════════════════════════════════════
# SPO FULL RANKING TABLE
# ══════════════════════════════════════════════════════════════════════════════
sec(SICO_TABLE, "SPO Full Ranking Table")

tbl = spo_sum.copy().reset_index(drop=True)
tbl.insert(0, "#", range(1, len(tbl)+1))
tbl["Revenue"]  = tbl["Total_Amt"].apply(fmt_inr)
tbl["Qty"]      = tbl["Total_Qty"].apply(lambda x: f"{int(x):,}")
tbl["Apr Rev"]  = tbl["Amt_Apr"].apply(fmt_inr)
tbl["May Rev"]  = tbl["Amt_May"].apply(fmt_inr)
tbl["MoM %"]    = tbl["MoM_%"].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else "—")
display_tbl = tbl[["#","SPO","Corrected_HQ","Division","State","Apr Rev","May Rev","Revenue","Qty","Products","MoM %"]].copy()
display_tbl.columns = ["#","SPO / MR","HQ","Division","State","Apr Rev","May Rev","Total Rev","Qty Sold","SKUs","MoM %"]
st.dataframe(
    display_tbl, use_container_width=True, height=400, hide_index=True,
    column_config={
        "#":        st.column_config.NumberColumn("#", width="small"),
        "SPO / MR": st.column_config.TextColumn("SPO / MR"),
        "HQ":       st.column_config.TextColumn("HQ", width="small"),
        "Division": st.column_config.TextColumn("Division", width="small"),
        "State":    st.column_config.TextColumn("State", width="small"),
        "Apr Rev":  st.column_config.TextColumn("Apr Rev", width="small"),
        "May Rev":  st.column_config.TextColumn("May Rev", width="small"),
        "Total Rev":st.column_config.TextColumn("Total Rev", width="small"),
        "Qty Sold": st.column_config.TextColumn("Qty Sold", width="small"),
        "SKUs":     st.column_config.NumberColumn("SKUs", width="small"),
        "MoM %":    st.column_config.TextColumn("MoM %", width="small"),
    },
)

# ══════════════════════════════════════════════════════════════════════════════
# RAW DATA  +  CSV DOWNLOAD
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("🔍 Raw Data Preview (filtered)", expanded=False):
    st.dataframe(df.head(500), use_container_width=True, hide_index=True)

csv_bytes = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Filtered Data (CSV)", csv_bytes, "ENTOD_SPO_Filtered.csv", "text/csv")

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
st.caption("ENTOD SPO-Wise Analytics · Apr–May 2026 · Powered by Streamlit")
