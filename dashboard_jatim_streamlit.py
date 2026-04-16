"""
Dashboard Ketenagakerjaan Jawa Timur — v4
BPS Color Palette | Per-Chart Filter | Download Button | Clean Narasi
Run: streamlit run dashboard_jatim_v4.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import os, warnings, io, base64
warnings.filterwarnings("ignore")

BASE = os.path.dirname(os.path.abspath(__file__))
def p(fname): return os.path.join(BASE, fname)

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Ketenagakerjaan Jawa Timur",
    page_icon=p("Logo.png"), layout="wide",
    initial_sidebar_state="collapsed"
)

# BPS Color Palette: biru tua #003d7a, oranye #f47920, biru muda #0072bc, abu #f0f4f8
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

*, html, body {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    box-sizing: border-box;
}
html, body, .main, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .block-container {
    background: #f0f4f8 !important;
}
.block-container { padding: 1.5rem 2rem !important; max-width: 100% !important; }

/* HEADER */
.dash-header {
    background: linear-gradient(135deg, #003d7a 0%, #0072bc 100%);
    border-radius: 14px;
    padding: 20px 28px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 18px;
    box-shadow: 0 4px 20px rgba(0,61,122,.25);
    position: sticky !important;
    top: 0 !important;
    z-index: 9999 !important;
}
.dash-header-logo {
    width: 52px; height: 52px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    background: transparent;
    overflow: hidden;
}
.dash-header-logo img {
    width: 100%; height: 100%;
    object-fit: contain;
    border-radius: 8px;
}
.dash-header-title { color: #fff; font-size: 1.35rem; font-weight: 800; margin: 0; }
.dash-header-sub { color: rgba(255,255,255,.75); font-size: .8rem; margin-top: 3px; }
.dash-header-badge {
    margin-left: auto;
    background: rgba(255,255,255,.15);
    color: #fff;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: .75rem;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,.25);
}

/* METRIC CARDS */
.kpi-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; margin-bottom: 20px; }
.kpi-card {
    background: #fff;
    border-radius: 12px;
    padding: 16px 20px;
    border: 1px solid #dde4ee;
    box-shadow: 0 1px 6px rgba(0,0,0,.05);
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0;
    width: 4px; height: 100%;
    background: #f47920;
}
.kpi-label { font-size: .7rem; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: .6px; margin-bottom: 8px; }
.kpi-value { font-size: 1.65rem; font-weight: 800; color: #003d7a; }
.kpi-delta { font-size: .75rem; margin-top: 4px; color: #6b7280; }
.kpi-delta.up { color: #16a34a; }
.kpi-delta.down { color: #dc2626; }

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: #fff !important;
    border-radius: 12px !important;
    border: 1px solid #dde4ee !important;
    padding: 6px 8px !important;
    gap: 6px !important;
    box-shadow: 0 1px 6px rgba(0,0,0,.04) !important;
    margin-bottom: 20px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: .83rem !important;
    color: #6b7280 !important;
    background: transparent !important;
    padding: 10px 26px !important;
    min-width: 200px !important;
    transition: all .2s ease !important;
}
.stTabs [aria-selected="true"] {
    background: #003d7a !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(0,61,122,.3) !important;
}

/* CHART CARD */
.chart-card {
    background: #ffffff;
    border-radius: 14px;
    border: 1px solid #dde4ee;
    box-shadow: 0 1px 8px rgba(0,0,0,.05);
    overflow: hidden;
    margin-bottom: 18px;
}
.chart-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 18px 10px;
    border-bottom: 1px solid #f0f4f8;
}
.chart-card-title {
    font-size: .85rem;
    font-weight: 700;
    color: #003d7a;
    display: flex;
    align-items: center;
    gap: 8px;
}
.chart-card-title::before {
    content: '';
    display: inline-block;
    width: 4px; height: 16px;
    background: #f47920;
    border-radius: 3px;
    flex-shrink: 0;
}
.chart-card-body { padding: 12px 16px 8px; }
.chart-card-filter {
    padding: 10px 16px;
    background: #f8fafc;
    border-bottom: 1px solid #f0f4f8;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: .78rem;
    color: #6b7280;
}

/* ANALISIS BOX */
.analisis-card {
    background: #f8fafc;
    border: 1px solid #dde4ee;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 18px;
    font-size: .8rem;
    color: #374151;
    line-height: 1.75;
}
.analisis-card h5 {
    font-size: .7rem;
    font-weight: 800;
    color: #003d7a;
    text-transform: uppercase;
    letter-spacing: .7px;
    margin: 0 0 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid #dde4ee;
    display: flex;
    align-items: center;
    gap: 6px;
}
.analisis-card h5::before { content: ''; }
.analisis-card ul { margin: 0; padding-left: 18px; }
.analisis-card li { margin-bottom: 6px; }
.hi { font-weight: 700; color: #003d7a; }
.warn { font-weight: 700; color: #dc2626; }
.ok { font-weight: 700; color: #16a34a; }

/* SECTION HEADING */
.sec-head {
    font-size: 1rem;
    font-weight: 800;
    color: #003d7a;
    padding: 10px 16px;
    background: #eff6ff;
    border-left: 4px solid #0072bc;
    border-radius: 0 8px 8px 0;
    margin: 22px 0 14px;
    letter-spacing: .2px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* DOWNLOAD BTN */
.dl-btn {
    display: inline-flex; align-items: center; gap: 5px;
    font-size: .72rem; font-weight: 600;
    color: #003d7a; background: #eff6ff;
    border: 1px solid #c7d9f8; border-radius: 6px;
    padding: 5px 10px; cursor: pointer;
    text-decoration: none;
    transition: all .15s;
}
.dl-btn:hover { background: #003d7a; color: #fff; border-color: #003d7a; }
.dl-btns { display: flex; gap: 6px; flex-wrap: wrap; }

hr { border-color: #e4e9f0 !important; margin: 16px 0 !important; }

/* Streamlit overrides */
[data-testid="stMetric"] { display: none; }
div[data-testid="column"] > div { height: 100%; }
.stSelectbox label, .stSlider label, .stMultiSelect label {
    font-size: .75rem !important;
    font-weight: 700 !important;
    color: #003d7a !important;
    text-transform: uppercase !important;
    letter-spacing: .4px !important;
}
/* Streamlit main container - allow overflow for sticky */
[data-testid="stAppViewContainer"] {
    overflow-y: auto !important;
}
/* Sticky Tab Bar */
[role="tablist"] {
    position: sticky !important;
    top: 0 !important;
    z-index: 9998 !important;
    background: white !important;
    padding: 10px 0 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,.1) !important;
    margin: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── BPS COLORS ───────────────────────────────────────────────────────────────
C = dict(
    biru="#003d7a",   # BPS biru tua
    biru2="#0072bc",  # BPS biru muda
    oranj="#f47920",  # BPS oranye
    red="#dc2626",
    green="#16a34a",
    yellow="#ca8a04",
    gray="#6b7280",
    sky="#0ea5e9",
    purple="#7c3aed",
)
BPS_SEQ = ["#003d7a","#0072bc","#00a0e3","#f47920","#faa555","#fdd099"]

def bps_layout(extra=None):
    d = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#374151", size=11),
        xaxis=dict(gridcolor="#f0f4f8", zerolinecolor="#e4e9f0", linecolor="#e4e9f0"),
        yaxis=dict(gridcolor="#f0f4f8", zerolinecolor="#e4e9f0", linecolor="#e4e9f0"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10), orientation="h", y=-0.22),
        margin=dict(t=20, r=20, b=50, l=60),
        hoverlabel=dict(bgcolor="#ffffff", font_size=12, bordercolor="#dde4ee"),
    )
    if extra: d.update(extra)
    return d

# ─── DOWNLOAD BUTTON HTML ─────────────────────────────────────────────────────
def dl_buttons(fig, key):
    """Render PNG/JPEG/SVG download buttons for a plotly figure."""
    import json
    fig_json = fig.to_json()
    html = f"""
    <div class="dl-btns" id="dlbtns_{key}">
        <a class="dl-btn" onclick="dlChart('{key}','png')">⬇ PNG</a>
        <a class="dl-btn" onclick="dlChart('{key}','jpeg')">⬇ JPEG</a>
        <a class="dl-btn" onclick="dlChart('{key}','svg')">⬇ SVG</a>
    </div>
    <div id="plotdata_{key}" style="display:none">{fig_json}</div>
    <script>
    function dlChart(key, fmt) {{
        try {{
            var data = JSON.parse(document.getElementById('plotdata_' + key).textContent);
            Plotly.downloadImage({{data: data.data, layout: data.layout}}, {{
                format: fmt, filename: 'chart_' + key, width: 1200, height: 500
            }});
        }} catch(e) {{
            // fallback: open in new tab as PNG via canvas
            alert('Download via toolbar icon on chart (right-click > Save)');
        }}
    }}
    </script>
    """
    return html

# ─── DATA LOADERS (same as v3) ────────────────────────────────────────────────
@st.cache_data
def load_tpt():
    raw = pd.read_excel(p("TPT_2001-2025.xlsx"), header=1)
    raw = raw.rename(columns={raw.columns[0]: "wilayah"})
    raw = raw.dropna(subset=["wilayah"])
    # Ambil semua kolom tahun 2001-2025
    year_cols = [c for c in raw.columns if str(c).strip().isdigit()
                 and 2001 <= int(str(c).strip()) <= 2025]
    out = raw[["wilayah"] + year_cols].copy()
    out.columns = ["wilayah"] + [str(int(str(c).strip())) for c in year_cols]
    out = out[out["wilayah"] != "wilayah"]
    for c in out.columns[1:]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    return out.reset_index(drop=True)

@st.cache_data
def load_tpak():
    raw = pd.read_excel(p("TPAK_2021-2025.xlsx"), header=1)
    raw = raw.rename(columns={raw.columns[0]: "wilayah"})
    raw = raw.dropna(subset=["wilayah"])
    yc = [c for c in raw.columns if str(c).strip() in ["2021","2022","2023","2024","2025"]]
    out = raw[["wilayah"] + yc].copy()
    out.columns = ["wilayah","2021","2022","2023","2024","2025"]
    out = out[out["wilayah"] != "wilayah"]
    for c in ["2021","2022","2023","2024","2025"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    return out.reset_index(drop=True)

@st.cache_data
def load_ak():
    df = pd.read_excel(p("PEKERJA_BERDASARKAN_TINGKAT_PENDIDIKAN_TAHUN_2023.xlsx"), header=None)
    tr = df.iloc[5]
    return {2021: float(str(tr.iloc[2]).replace("-","").strip() or 0)/1e6,
            2022: float(str(tr.iloc[4]).replace("-","").strip() or 0)/1e6,
            2023: float(str(tr.iloc[6]).replace("-","").strip() or 0)/1e6,
            2024: float(str(tr.iloc[7]).replace("-","").strip() or 0)/1e6,
            2025: float(str(tr.iloc[9]).replace("-","").strip() or 0)/1e6}

@st.cache_data
def load_upah_informal():
    df = pd.read_excel(p("UPAH_PEKERJA_INFORMAL_2021-2025.xlsx"), header=None)
    jt = df[df.iloc[:,0]=="Jawa Timur"].iloc[0]
    return {2021:int(jt.iloc[4]),2022:int(jt.iloc[9]),2023:int(jt.iloc[14]),2025:int(jt.iloc[19])}

@st.cache_data
def load_upah_formal():
    df = pd.read_excel(p("RATA2_UPAH_PEKERJA_FORMAL_2025.xlsx"), header=2)
    df = df.rename(columns={df.columns[0]:"wilayah", df.columns[4]:"upah_total"})
    df = df.dropna(subset=["wilayah","upah_total"])
    df["upah_total"] = pd.to_numeric(df["upah_total"], errors="coerce")
    df["wilayah"] = df["wilayah"].astype(str).str.replace("Kabupaten ","Kab. ")
    return df[["wilayah","upah_total"]].dropna().reset_index(drop=True)

@st.cache_data
def load_jam_umur():
    df = pd.read_excel(p("JAM_KERJA_BERDASARKAN_KELOMPOK_UMUR_2021-2025.xlsx"), header=None)
    recs, cur = {}, None
    for _, row in df.iterrows():
        v = str(row.iloc[0])
        if v in ["2021","2022","2023","2025"]:
            cur = int(v); recs[cur] = []
        elif v == "Jumlah/Total" and cur:
            recs[cur] = {"0jam":int(row.iloc[1]),"1_14":int(row.iloc[2]),
                         "15_34":int(row.iloc[3]),"35plus":int(row.iloc[4]),"total":int(row.iloc[5])}
    return recs

@st.cache_data
def load_jam_umur_detail():
    df = pd.read_excel(p("JAM_KERJA_BERDASARKAN_KELOMPOK_UMUR_2021-2025.xlsx"), header=None)
    rows, cur = [], None
    for _, row in df.iterrows():
        v = str(row.iloc[0])
        if v in ["2021","2022","2023","2025"]:
            cur = int(v)
        elif cur and v != "Jumlah/Total" and not v.startswith("nan"):
            try:
                rows.append({"tahun":cur,"umur":v,
                    "0jam":int(float(str(row.iloc[1]).replace("-","0") or 0)),
                    "1_14":int(float(str(row.iloc[2]).replace("-","0") or 0)),
                    "15_34":int(float(str(row.iloc[3]).replace("-","0") or 0)),
                    "35plus":int(float(str(row.iloc[4]).replace("-","0") or 0)),
                    "total":int(float(str(row.iloc[5]).replace("-","0") or 0))})
            except: pass
    return pd.DataFrame(rows)

@st.cache_data
def load_lk():
    df = pd.read_excel(p("DATA_KETERSEDIAAN_LAPANGAN_KERJA_2021-2025.xlsx"), header=None)
    data = df.iloc[2:].copy()
    data.columns = range(len(data.columns))
    data = data.rename(columns={0:"wilayah"})
    data = data.dropna(subset=["wilayah"])
    data = data[data["wilayah"].astype(str).str.strip()!=""]
    def si(x):
        try: return int(float(str(x).replace("-","").strip() or 0))
        except: return 0
    out = pd.DataFrame({"wilayah": data["wilayah"].values})
    for col, idx in [("pencari_2021",3),("lowongan_2021",6),("penempatan_2021",9),
                     ("pencari_2022",12),("lowongan_2022",15),("penempatan_2022",18),
                     ("pencari_2023",21),("lowongan_2023",24),("penempatan_2023",27),
                     ("pencari_2024",40),("lowongan_2024",43),("penempatan_2024",46),
                     ("pencari_2025",49),("lowongan_2025",52)]:
        out[col] = data[idx].apply(si).values
    return out.reset_index(drop=True)

@st.cache_data
def load_status():
    df = pd.read_excel(p("JUMLAH_ANGKATAN_KERJA_2021-2025.xlsx"), header=None)
    sr = df.iloc[3:9].copy()
    labels = sr.iloc[:,0].tolist()
    totals = sr.iloc[:,18].tolist()
    out = pd.DataFrame({"status":labels,"jumlah":[int(float(str(x).replace("-","0"))) for x in totals]})
    return out[out["jumlah"]>0]

# ─── LOAD DATA ────────────────────────────────────────────────────────────────
with st.spinner("Memuat data..."):
    df_tpt = load_tpt(); df_tpak = load_tpak()
    ak_d = load_ak(); upah_inf = load_upah_informal()
    df_uf = load_upah_formal(); jam_d = load_jam_umur()
    df_ju = load_jam_umur_detail(); df_lk = load_lk(); df_stat = load_status()

prov_tpt  = df_tpt[df_tpt["wilayah"].str.strip()=="Jawa Timur"].iloc[0]
prov_tpak = df_tpak[df_tpak["wilayah"].str.strip()=="Jawa Timur"].iloc[0]
prov_lk   = df_lk[df_lk["wilayah"].astype(str).str.strip()=="Jawa Timur"].iloc[0]
kab_lk    = df_lk[df_lk["wilayah"].astype(str).str.strip()!="Jawa Timur"].copy()

YEARS = [2021,2022,2023,2024,2025]
TPT_Y  = [float(prov_tpt[str(y)]) for y in YEARS]
TPAK_Y = [float(prov_tpak[str(y)]) for y in YEARS]
AK_Y   = [ak_d.get(y) for y in YEARS]
PEN_Y  = [int(prov_lk.get(f"pencari_{y}",0)) for y in YEARS]
LOW_Y  = [int(prov_lk.get(f"lowongan_{y}",0)) for y in YEARS]

# ─── HEADER ───────────────────────────────────────────────────────────────────
# Read and encode logo as base64
import base64
try:
    with open(p("Logo.png"), "rb") as img:
        logo_base64 = base64.b64encode(img.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="Logo" style="width:100%; height:100%; object-fit:contain;"/>'  
except:
    logo_html = ''

st.markdown(f"""
<div class="dash-header">
    <div class="dash-header-logo">{logo_html}</div>
    <div>
        <div class="dash-header-title">Dashboard Ketenagakerjaan Jawa Timur</div>
        <div class="dash-header-sub">Analisis Pasar Kerja Berbasis Data BPS · Sakernas 2021–2025</div>
    </div>
    <div class="dash-header-badge">Sumber: BPS Jawa Timur dan Sakernas 2021–2025</div>
</div>
""", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "Struktur Ketenagakerjaan",
    "Pasar & Kebutuhan Kerja",
    "Analisis Lanjutan",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: STRUKTUR KETENAGAKERJAAN
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    # ── KPI CARDS (global year picker for KPI only) ────────────────────────
    yr_kpi = st.selectbox("Tahun Referensi KPI", ["2025","2024","2023","2022","2021"], key="kpi_yr")
    tpt_c = float(prov_tpt[yr_kpi])
    tpak_c = float(prov_tpak[yr_kpi])
    ak_c = ak_d.get(int(yr_kpi))
    up_c = upah_inf.get(int(yr_kpi))
    prev_yr = str(int(yr_kpi)-1)
    tpt_prev = float(prov_tpt[prev_yr]) if int(yr_kpi)>2021 else None
    tpak_prev = float(prov_tpak[prev_yr]) if int(yr_kpi)>2021 else None
    ak_prev = ak_d.get(int(yr_kpi)-1)

    def delta_class(v): return "up" if v>0 else "down" if v<0 else ""
    def delta_sym(v): return f"+ {abs(v):.2f}" if v>0 else f"- {abs(v):.2f}" if v<0 else "="

    d_ak  = (ak_c - ak_prev) if ak_c and ak_prev else 0
    d_tpt = (tpt_c - tpt_prev) if tpt_prev else 0
    d_tpak= (tpak_c - tpak_prev) if tpak_prev else 0

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-label">Angkatan Kerja</div>
            <div class="kpi-value">{ak_c:.2f}jt</div>
            <div class="kpi-delta {delta_class(d_ak)}">{delta_sym(d_ak)} juta vs {prev_yr}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">TPT Jawa Timur</div>
            <div class="kpi-value">{tpt_c:.2f}%</div>
            <div class="kpi-delta {delta_class(-d_tpt)}">{delta_sym(d_tpt)}pp vs {prev_yr}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">TPAK Jawa Timur</div>
            <div class="kpi-value">{tpak_c:.2f}%</div>
            <div class="kpi-delta {delta_class(d_tpak)}">{delta_sym(d_tpak)}pp vs {prev_yr}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Upah Informal</div>
            <div class="kpi-value">{f'Rp{up_c/1e6:.2f}jt' if up_c else 'N/A'}</div>
            <div class="kpi-delta">{f'Rata-rata {yr_kpi}' if up_c else 'Data tahun 2024 tidak tersedia'}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ═══ GRAFIK A: Tren Angkatan Kerja ════════════════════════════════════
    st.markdown('<div class="sec-head">A · Tren Tingkat Partisipasi Angkatan Kerja (TPAK)</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        # Filter
        fa1, fa2 = st.columns([2,4])
        with fa1:
            show_ak_line = st.selectbox("Tampilan", ["Area + Marker","Hanya Garis"], key="fa_style")
        st.markdown(f'<div class="chart-card-title" style="padding:0 18px 6px;">Tren Jumlah Angkatan Kerja Jawa Timur (Juta Jiwa)</div>', unsafe_allow_html=True)

        ak_v = [v for v in AK_Y if v]; ak_x = [YEARS[i] for i,v in enumerate(AK_Y) if v]
        fig_a = go.Figure()
        fill_mode = "tozeroy" if show_ak_line=="Area + Marker" else "none"
        fig_a.add_trace(go.Scatter(
            x=ak_x, y=[v*1e6 for v in ak_v],
            mode="lines+markers+text",
            line=dict(color=C["biru"],width=3),
            marker=dict(size=9,color=C["oranj"],line=dict(color="#fff",width=2)),
            text=[f"{v:.2f} jt" for v in ak_v],
            textposition="top center",
            textfont=dict(size=10,color=C["biru"],family="monospace"),
            fill=fill_mode, fillcolor="rgba(0,61,122,.07)",
            name="Angkatan Kerja",
            hovertemplate="<b>%{x}</b><br>%{y:,.0f} jiwa<extra></extra>",
        ))
        fig_a.update_layout(**bps_layout({
            "yaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",tickformat=".3s"),
            "xaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",dtick=1),
            "height":320,
        }))

        col_g, col_n = st.columns([3,1])
        with col_g:
            st.plotly_chart(fig_a, use_container_width=True, config={"displaylogo":False,"toImageButtonOptions":{"format":"png","filename":"tren_ak"}})
        with col_n:
            ak_25 = ak_d.get(2025,0); ak_21 = ak_d.get(2021,0)
            delta_4y = ak_25 - ak_21
            st.markdown(f"""<div class="analisis-card"><h5>Analisis</h5>
            <ul>
            <li>Angkatan kerja naik <span class="hi">+{delta_4y:.2f} juta jiwa</span> selama 4 tahun (2021–2025).</li>
            <li>Pertumbuhan stabil menunjukkan ekspansi ekonomi yang sehat.</li>
            <li>Butuh <span class="warn">lapangan kerja baru</span> sebanding agar tidak memperparah pengangguran.</li>
            </ul></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ═══ GRAFIK B: Tren TPT & TPAK ════════════════════════════════════════
    st.markdown('<div class="sec-head">B · Tren Tingkat Pengangguran Terbuka (TPT) dan Tingkat Partisipasi Angkatan Kerja (TPAK)</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fb1, fb2 = st.columns([2,4])
        with fb1:
            show_b = st.selectbox("Overlay", ["TPT + TPAK","Hanya TPT"], key="fb_ov")
        st.markdown('<div class="chart-card-title" style="padding:0 18px 6px;">Tren TPT & TPAK Jawa Timur 2021–2025 (%)</div>', unsafe_allow_html=True)

        fig_b = go.Figure()
        fig_b.add_trace(go.Scatter(
            x=YEARS, y=TPT_Y, mode="lines+markers+text", name="TPT (%)",
            line=dict(color=C["oranj"],width=3),
            marker=dict(size=9,color=C["oranj"],line=dict(color="#fff",width=2)),
            text=[f"{v:.2f}%" for v in TPT_Y],
            textposition="top center",
            textfont=dict(size=10,color=C["oranj"],family="monospace"),
            fill="tozeroy", fillcolor="rgba(244,121,32,.08)",
            hovertemplate="TPT <b>%{x}</b>: %{y:.2f}%<extra></extra>",
        ))
        layout_extra_b = {
            "yaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",range=[0,8],title="TPT (%)"),
            "xaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",dtick=1),
            "height":320,
        }
        if show_b == "TPT + TPAK":
            fig_b.add_trace(go.Scatter(
                x=YEARS, y=TPAK_Y, mode="lines+markers+text", name="TPAK (%)",
                line=dict(color=C["biru2"],width=3,dash="dot"),
                marker=dict(size=9,color=C["biru2"],line=dict(color="#fff",width=2)),
                text=[f"{v:.1f}%" for v in TPAK_Y],
                textposition="bottom center",
                textfont=dict(size=9,color=C["biru2"]),
                yaxis="y2",
                hovertemplate="TPAK <b>%{x}</b>: %{y:.2f}%<extra></extra>",
            ))
            layout_extra_b["yaxis2"] = dict(overlaying="y",side="right",range=[65,82],title="TPAK (%)",gridcolor="rgba(0,0,0,0)")
        fig_b.update_layout(**bps_layout(layout_extra_b))

        col_g, col_n = st.columns([3,1])
        with col_g:
            st.plotly_chart(fig_b, use_container_width=True, config={"displaylogo":False,"toImageButtonOptions":{"format":"png","filename":"tren_tpt_tpak"}})
        with col_n:
            st.markdown(f"""<div class="analisis-card"><h5>Analisis</h5>
            <ul>
            <li>TPT turun <span class="ok">{TPT_Y[0]-TPT_Y[-1]:.2f} poin</span> dari 2021 ke 2025 — tren positif.</li>
            <li>TPAK naik <span class="hi">{TPAK_Y[-1]-TPAK_Y[0]:.2f} poin</span> — lebih banyak warga aktif bekerja.</li>
            <li>TPT ↓ + TPAK ↑ = <span class="ok">perbaikan nyata</span>, bukan sekadar orang keluar dari pasar kerja.</li>
            </ul></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ═══ GRAFIK C: TPT per Kab/Kota ═══════════════════════════════════════
    st.markdown('<div class="sec-head">C · Persebaran TPT per Kabupaten/Kota</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fc1, fc2, fc3 = st.columns([1,1,2])
        with fc1: yr_c = st.selectbox("Tahun", ["2025","2024","2023","2022","2021"], key="fc_yr")
        with fc2: wil_c = st.selectbox("Wilayah", ["Semua","Hanya Kabupaten","Hanya Kota"], key="fc_wil")
        with fc3: topn_c = st.slider("Top N Wilayah", 10, 38, 20, key="fc_top")
        st.markdown(f'<div class="chart-card-title" style="padding:0 18px 6px;">TPT per Kab/Kota — {yr_c} (Top {topn_c})</div>', unsafe_allow_html=True)

        kab_c = df_tpt[df_tpt["wilayah"].str.strip()!="Jawa Timur"].copy()
        if wil_c=="Hanya Kabupaten": kab_c = kab_c[~kab_c["wilayah"].str.startswith("Kota")]
        elif wil_c=="Hanya Kota": kab_c = kab_c[kab_c["wilayah"].str.startswith("Kota")]
        kab_c = kab_c.sort_values(yr_c, ascending=False).head(topn_c)
        bar_colors = [C["red"] if v>=7 else C["oranj"] if v>=5 else C["biru2"] if v>=3 else C["green"] for v in kab_c[yr_c]]

        fig_c = go.Figure(go.Bar(
            x=kab_c[yr_c], y=kab_c["wilayah"], orientation="h",
            marker_color=bar_colors,
            text=[f"{v:.2f}%" for v in kab_c[yr_c]],
            textposition="outside", textfont=dict(size=9),
            hovertemplate="<b>%{y}</b><br>TPT: %{x:.2f}%<extra></extra>",
        ))
        fig_c.update_layout(**bps_layout({
            "height":max(380,topn_c*20),
            "margin":dict(t=10,r=65,b=20,l=170),
            "xaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",range=[0,14]),
            "yaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",automargin=True,tickfont=dict(size=9)),
        }))

        col_g, col_n = st.columns([3,1])
        with col_g:
            st.plotly_chart(fig_c, use_container_width=True, config={"displaylogo":False,"toImageButtonOptions":{"format":"png","filename":"tpt_kabkota"}})
        with col_n:
            top1 = kab_c.iloc[0]["wilayah"] if len(kab_c)>0 else "-"
            top1v = float(kab_c.iloc[0][yr_c]) if len(kab_c)>0 else 0
            bot1 = kab_c.iloc[-1]["wilayah"] if len(kab_c)>0 else "-"
            bot1v = float(kab_c.iloc[-1][yr_c]) if len(kab_c)>0 else 0
            st.markdown(f"""<div class="analisis-card"><h5>Analisis</h5>
            <ul>
            <li><span class="warn">Tertinggi:</span> {top1} ({top1v:.2f}%) — perlu intervensi segera.</li>
            <li><span class="ok">Terendah:</span> {bot1} ({bot1v:.2f}%) — bisa jadi model best practice.</li>
            <li>Warna merah = TPT ≥7%, oranye = 5–7%, biru = 3–5%, hijau = &lt;3%.</li>
            <li>Kota besar cenderung TPT lebih tinggi karena menarik <span class="warn">migrasi pencari kerja</span>.</li>
            </ul></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ═══ GRAFIK D: Jam Kerja ══════════════════════════════════════════════
    st.markdown('<div class="sec-head">D · Komposisi Jam Kerja Penduduk Bekerja</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fd1, _ = st.columns([2,4])
        with fd1:
            mode_d = st.selectbox("Tampilan", ["Stacked Bar","Grouped Bar"], key="fd_mode")
        st.markdown('<div class="chart-card-title" style="padding:0 18px 6px;">Komposisi Jam Kerja Penduduk Bekerja (%, per Tahun)</div>', unsafe_allow_html=True)

        ay = [y for y in [2021,2022,2023,2025] if y in jam_d and isinstance(jam_d[y],dict)]
        jdf = pd.DataFrame([{"tahun":y,
            "Pekerja Penuh (35+)": jam_d[y]["35plus"]/jam_d[y]["total"]*100,
            "Setengah Pengangguran (<35)": (jam_d[y]["0jam"]+jam_d[y]["1_14"]+jam_d[y]["15_34"])/jam_d[y]["total"]*100}
            for y in ay])

        fig_d = go.Figure()
        bmode = "stack" if mode_d=="Stacked Bar" else "group"
        fig_d.add_trace(go.Bar(x=jdf["tahun"], y=jdf["Pekerja Penuh (35+)"],
            name="Pekerja Penuh (35+ jam)", marker_color=C["biru"],
            text=[f"{v:.1f}%" for v in jdf["Pekerja Penuh (35+)"]],
            textposition="inside", textfont=dict(size=11,color="white")))
        fig_d.add_trace(go.Bar(x=jdf["tahun"], y=jdf["Setengah Pengangguran (<35)"],
            name="Setengah Pengangguran (<35 jam)", marker_color=C["oranj"],
            text=[f"{v:.1f}%" for v in jdf["Setengah Pengangguran (<35)"]],
            textposition="inside", textfont=dict(size=11,color="white")))
        fig_d.update_layout(**bps_layout({
            "barmode":bmode,
            "yaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",range=[0,105],title="%"),
            "xaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",dtick=1),
            "height":300,
        }))

        col_g, col_n = st.columns([3,1])
        with col_g:
            st.plotly_chart(fig_d, use_container_width=True, config={"displaylogo":False,"toImageButtonOptions":{"format":"png","filename":"jam_kerja"}})
        with col_n:
            pct_p = jdf[jdf["tahun"]==max(ay)]["Pekerja Penuh (35+)"].values[0]
            pct_s = 100 - pct_p
            st.markdown(f"""<div class="analisis-card"><h5>Analisis</h5>
            <ul>
            <li>Data tahun 2024 tidak tersedia di BPS.</li>
            <li>Tahun {max(ay)}: <span class="hi">{pct_p:.1f}%</span> pekerja penuh waktu.</li>
            <li><span class="warn">{pct_s:.1f}% setengah pengangguran</span> — bekerja &lt;35 jam/minggu, berdampak pada pendapatan rendah.</li>
            <li>Butuh kebijakan <span class="hi">penciptaan kerja formal</span> dengan jam kerja penuh.</li>
            </ul></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ═══ GRAFIK E: Upah Informal + Status ═════════════════════════════════
    st.markdown('<div class="sec-head">E · Upah Informal & Status Pekerjaan</div>', unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)

    with col_e1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fe1, _ = st.columns([2,2])
        with fe1:
            show_e_ann = st.selectbox("Anotasi", ["Tampilkan Nilai","Sembunyikan"], key="fe_ann")
        st.markdown('<div class="chart-card-title" style="padding:0 18px 6px;">Tren Upah Pekerja Informal (Rp)</div>', unsafe_allow_html=True)
        uyr = sorted(upah_inf.keys()); uv = [upah_inf[y] for y in uyr]
        fig_e1 = go.Figure(go.Scatter(
            x=uyr, y=uv, mode="lines+markers" + ("+text" if show_e_ann=="Tampilkan Nilai" else ""),
            line=dict(color=C["biru"],width=3),
            marker=dict(size=10,color=C["oranj"],line=dict(color="#fff",width=2)),
            text=[f"Rp{v/1e6:.2f}jt" for v in uv],
            textposition="top center",
            textfont=dict(size=10,color=C["biru"],family="monospace"),
            fill="tozeroy", fillcolor="rgba(0,61,122,.07)",
            hovertemplate="<b>%{x}</b><br>Rp%{y:,.0f}<extra></extra>",
        ))
        fig_e1.update_layout(**bps_layout({
            "yaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",tickformat=",.0f",title="Rp"),
            "xaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0"),
            "height":290,"margin":dict(t=10,r=20,b=40,l=80),
        }))
        st.plotly_chart(fig_e1, use_container_width=True, config={"displaylogo":False,"toImageButtonOptions":{"format":"png","filename":"upah_informal"}})

        u_first = uv[0]; u_last = uv[-1]
        st.markdown(f"""<div class="analisis-card" style="margin-top:8px"><h5>Analisis</h5>
        <ul>
        <li>Upah informal naik <span class="hi">{(u_last-u_first)/u_first*100:.1f}%</span> dalam periode 2021–{max(uyr)}.</li>
        <li>Namun tetap jauh di bawah upah formal — <span class="warn">sektor informal masih rentan</span>.</li>
        </ul></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_e2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fe2a, _ = st.columns([2,2])
        with fe2a:
            hole_e2 = st.selectbox("Tipe Chart", ["Donut Chart","Pie Chart"], key="fe2_type")
        st.markdown('<div class="chart-card-title" style="padding:0 18px 6px;">Komposisi Status Pekerjaan 2024</div>', unsafe_allow_html=True)
        hole_val = 0.42 if hole_e2=="Donut" else 0
        fig_e2 = go.Figure(go.Pie(
            labels=df_stat["status"], values=df_stat["jumlah"],
            hole=hole_val,
            marker_colors=[C["biru"],C["biru2"],C["oranj"],"#faa555","#fdd099",C["gray"]],
            textinfo="label+percent", textfont=dict(size=9),
            pull=[0.05 if i==0 else 0 for i in range(len(df_stat))],
            hovertemplate="<b>%{label}</b><br>%{value:,} orang<br>%{percent}<extra></extra>",
        ))
        fig_e2.update_layout(**bps_layout({
            "margin":dict(t=10,r=10,b=50,l=10),
            "showlegend":True,
            "legend":dict(bgcolor="rgba(0,0,0,0)",font=dict(size=8.5),orientation="h",y=-0.12,x=0),
            "height":290,
        }))
        st.plotly_chart(fig_e2, use_container_width=True, config={"displaylogo":False,"toImageButtonOptions":{"format":"png","filename":"status_pekerjaan"}})

        top_stat = df_stat.sort_values("jumlah",ascending=False).iloc[0]
        st.markdown(f"""<div class="analisis-card" style="margin-top:8px"><h5>Analisis</h5>
        <ul>
        <li>Status terbesar: <span class="hi">{top_stat['status']}</span> — menunjukkan dominasi sektor ini.</li>
        <li>Diversifikasi status kerja penting untuk ketahanan tenaga kerja jangka panjang.</li>
        </ul></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    #  PATCH: Section F — Heatmap Pemetaan Spasial Jawa Timur
    #  Sisipkan di dalam `with tab1:`, setelah penutup Section E
    #  (tepat sebelum komentar  # ══ TAB 2: PASAR & KEBUTUHAN KERJA ══)
    #
    #  TIDAK MEMERLUKAN dependensi tambahan — semua sudah ada di requirements
    #  (plotly, pandas, numpy, requests sudah include di Streamlit default).
    #
    #  Strategi peta:
    #   • Jika GeoJSON berhasil dimuat → px.choropleth (peta isi penuh)
    #   • Jika tidak ada koneksi → px.scatter_geo bubble map (tetap informatif)
    #
    #  GeoJSON dicoba dari dua sumber alternatif yang ringan (file <500 KB).
    #  Centroid 38 kab/kota Jawa Timur di-embed langsung (fallback 0 dependency).
    # ═══════════════════════════════════════════════════════════════════════════

    import requests as _req, json as _json, re as _re

    # ── Centroid lookup (fallback bubble map & label matching) ──────────────────
    _JATIM_CENTROIDS = {
        "Kab. Pacitan":     (-8.175, 111.110), "Kab. Ponorogo":    (-7.870, 111.463),
        "Kab. Trenggalek":  (-8.054, 111.712), "Kab. Tulungagung": (-8.067, 111.903),
        "Kab. Blitar":      (-8.100, 112.168), "Kab. Kediri":      (-7.820, 112.018),
        "Kab. Malang":      (-8.160, 112.630), "Kab. Lumajang":    (-8.130, 113.222),
        "Kab. Jember":      (-8.172, 113.703), "Kab. Banyuwangi":  (-8.220, 114.370),
        "Kab. Bondowoso":   (-7.910, 113.820), "Kab. Situbondo":   (-7.710, 114.010),
        "Kab. Probolinggo": (-7.750, 113.220), "Kab. Pasuruan":    (-7.645, 112.910),
        "Kab. Sidoarjo":    (-7.450, 112.718), "Kab. Mojokerto":   (-7.472, 112.433),
        "Kab. Jombang":     (-7.550, 112.232), "Kab. Nganjuk":     (-7.605, 111.905),
        "Kab. Madiun":      (-7.630, 111.542), "Kab. Magetan":     (-7.652, 111.329),
        "Kab. Ngawi":       (-7.404, 111.443), "Kab. Bojonegoro":  (-7.152, 111.881),
        "Kab. Tuban":       (-6.902, 111.894), "Kab. Lamongan":    (-7.118, 112.413),
        "Kab. Gresik":      (-7.156, 112.654), "Kab. Bangkalan":   (-7.038, 112.733),
        "Kab. Sampang":     (-7.187, 113.248), "Kab. Pamekasan":   (-7.157, 113.474),
        "Kab. Sumenep":     (-6.988, 113.869), "Kota Kediri":      (-7.817, 112.011),
        "Kota Blitar":      (-8.095, 112.161), "Kota Malang":      (-7.983, 112.621),
        "Kota Probolinggo": (-7.752, 113.215), "Kota Pasuruan":    (-7.643, 112.899),
        "Kota Mojokerto":   (-7.469, 112.436), "Kota Madiun":      (-7.629, 111.527),
        "Kota Surabaya":    (-7.250, 112.750), "Kota Batu":        (-7.870, 112.524),
    }

    def _norm(x):
        if pd.isna(x):
            return ""
        x = str(x).lower().strip()

        # hapus prefix
        x = x.replace("kabupaten ", "")
        x = x.replace("kab. ", "")
        x = x.replace("kota ", "")

        # bersihin spasi
        x = " ".join(x.split())

        return x

    def _fuzzy_match(query: str, choices) -> str | None:
        q = _norm(query).lower()
        for c in choices:
            if _norm(c).lower() == q: return c
        for c in choices:
            cn = _norm(c).lower()
            if q in cn or cn in q: return c
        q_tok = set(q.split())
        best = max(choices, key=lambda c: len(q_tok & set(_norm(c).lower().split())), default=None)
        if best and q_tok & set(_norm(best).lower().split()):
            return best
        return None

    # ── GeoJSON loader (tries two CDN routes, falls back gracefully) ────────────
    _GJ_URLS = [
        "https://raw.githubusercontent.com/ans-4175/peta-indonesia-geojson/master/jawa-timur.geojson",
        "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/jawa-timur.geojson",
    ]
    _GJ_CACHE_PATH = os.path.join(BASE, "_jatim_geo_cache.json")

    @st.cache_data(ttl=86400, show_spinner=False)
    def _load_geojson():
        if os.path.exists(_GJ_CACHE_PATH):
            try:
                with open(_GJ_CACHE_PATH) as f: return _json.load(f)
            except Exception: pass
        for url in _GJ_URLS:
            try:
                r = _req.get(url, timeout=12,
                            headers={"User-Agent": "Mozilla/5.0 (compatible; dashboard/1.0)"})
                r.raise_for_status()
                gj = r.json()
                if gj.get("features"):
                    with open(_GJ_CACHE_PATH, "w") as f: _json.dump(gj, f)
                    return gj
            except Exception:
                continue
        return None

    # ═══════════════════════════════════════════════════════════════════════════
    #  SECTION F — Heatmap Pemetaan Spasial Jawa Timur
    # ═══════════════════════════════════════════════════════════════════════════

    st.markdown(
        '<div class="sec-head">F · Pemetaan Spasial Angka TPT Jawa Timur</div>',
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)

        # ── Filter row ──────────────────────────────────────────────────────────
        ff1, ff2, ff3 = st.columns([1, 1, 2])
        with ff1:
            yr_map = st.selectbox(
                "Tahun", ["2025", "2024", "2023", "2022", "2021"], key="f_map_yr"
            )
        with ff2:
            ind_map = st.selectbox(
                "Indikator",
                ["TPT (%)"],
                key="f_map_ind",
            )
        with ff3:
            cs_opt = st.selectbox(
                "Skema Warna",
                ["RdYlGn_r — Merah=Kritis", "Blues", "YlOrRd", "Viridis"],
                key="f_map_cs",
            )

        st.markdown(
            f'<div class="chart-card-title" style="padding:0 18px 8px;">'
            f'Peta Sebaran <b>{ind_map}</b> per Kab/Kota — {yr_map}</div>',
            unsafe_allow_html=True,
        )

        # ── Build nilai per kab/kota ────────────────────────────────────────────
        kab_m = df_tpt[df_tpt["wilayah"].str.strip() != "Jawa Timur"].copy()
        kab_m["wilayah_norm"] = kab_m["wilayah"].apply(_norm)

        if ind_map == "TPT (%)":
            kab_m["nilai"] = pd.to_numeric(kab_m[yr_map], errors="coerce")
            unit, fmt = "%", ".2f"

        elif ind_map in ("Pencari Kerja (Orang)", "Lowongan Kerja (Orang)"):
            field = "pencari" if "Pencari" in ind_map else "lowongan"
            col_lk = f"{field}_{yr_map}"
            tmp = kab_lk[["wilayah", col_lk]].copy()
            tmp["wilayah_norm"] = tmp["wilayah"].apply(_norm)
            kab_m = kab_m.merge(
                tmp[["wilayah_norm", col_lk]], on="wilayah_norm", how="left"
            )
            kab_m["nilai"] = pd.to_numeric(kab_m[col_lk], errors="coerce")
            unit, fmt = "orang", ",.0f"

        else:  # Rasio Lowongan/Pencari
            tmp2 = kab_lk[["wilayah", f"pencari_{yr_map}", f"lowongan_{yr_map}"]].copy()
            tmp2["wilayah_norm"] = tmp2["wilayah"].apply(_norm)
            kab_m = kab_m.merge(tmp2[["wilayah_norm", f"pencari_{yr_map}", f"lowongan_{yr_map}"]],
                                on="wilayah_norm", how="left")
            pen  = kab_m[f"pencari_{yr_map}"].replace(0, np.nan)
            kab_m["nilai"] = (kab_m[f"lowongan_{yr_map}"] / pen).round(2)
            unit, fmt = "x", ".2f"

        kab_m["nilai"] = pd.to_numeric(kab_m["nilai"], errors="coerce")
        v_clean = kab_m["nilai"].dropna()

        # ── Koordinat ──────────────────────────────────────────────────────────
        def _coord(wil):
            k = _fuzzy_match(wil, list(_JATIM_CENTROIDS.keys()))
            return _JATIM_CENTROIDS.get(k, (None, None))

        kab_m["lat"] = kab_m["wilayah"].apply(lambda w: _coord(w)[0])
        kab_m["lon"] = kab_m["wilayah"].apply(lambda w: _coord(w)[1])

        # ── Color scale mapping ─────────────────────────────────────────────────
        _CS = {
            "RdYlGn_r — Merah=Kritis": "RdYlGn_r",
            "Blues":  "Blues",
            "YlOrRd": "YlOrRd",
            "Viridis": "Viridis",
        }
        chosen_cs = _CS.get(cs_opt, "RdYlGn_r")

        # ── Attempt choropleth, fallback to bubble map ──────────────────────────
        gj = _load_geojson()
        col_map, col_ana = st.columns([3, 1])

        with col_map:
            if gj and gj.get("features"):
                # ── Choropleth (full polygon fill) ─────────────────────────────
                props0 = gj["features"][0]["properties"]
                name_key = next(
                    (k for k in ["name", "NAME", "KABKOT", "WADMKK", "kabupaten", "kota"]
                    if k in props0),
                    list(props0.keys())[0],
                )
                geo_names = [f["properties"].get(name_key, "") for f in gj["features"]]
                kab_m["geo_name"] = kab_m["wilayah"].apply(
                    lambda w: _fuzzy_match(w, geo_names) or w
                )
                hover_lbl = ind_map.replace(" (%)", "").replace(" (Orang)", "").replace("/", " per ")
                fig_map = px.choropleth(
                    kab_m.dropna(subset=["nilai", "geo_name"]),
                    geojson=gj,
                    locations="geo_name",
                    featureidkey=f"properties.{name_key}",
                    color="nilai",
                    color_continuous_scale=chosen_cs,
                    hover_name="wilayah",
                    hover_data={"nilai": f":{fmt}", "geo_name": False},
                    labels={"nilai": hover_lbl},
                )
                fig_map.update_geos(fitbounds="locations", visible=False)
                fig_map.update_coloraxes(colorbar=dict(
                    title=dict(text=hover_lbl, font=dict(size=10)),
                    tickfont=dict(size=9), len=0.75, thickness=14,
                ))
                fig_map.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", geo_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10, r=10, b=10, l=10), height=440,
                    font=dict(family="Plus Jakarta Sans, sans-serif"),
                    hoverlabel=dict(bgcolor="#fff", font_size=12, bordercolor="#dde4ee"),
                )
                map_mode = "choropleth"
            else:
                # ── Bubble map (scatter_geo) — offline-safe ─────────────────────
                kab_plot = kab_m.dropna(subset=["nilai", "lat", "lon"]).copy()

                # Normalise bubble size (min 6, max 40)
                v_range = kab_plot["nilai"].max() - kab_plot["nilai"].min()
                if v_range > 0:
                    kab_plot["bsize"] = 6 + 34 * (kab_plot["nilai"] - kab_plot["nilai"].min()) / v_range
                else:
                    kab_plot["bsize"] = 20

                # Color by quantile
                q25 = kab_plot["nilai"].quantile(0.25)
                q75 = kab_plot["nilai"].quantile(0.75)
                def _bcolor(v):
                    if v >= q75:   return C["red"]
                    if v >= kab_plot["nilai"].median(): return C["oranj"]
                    if v >= q25:   return C["biru2"]
                    return C["green"]
                kab_plot["bcolor"] = kab_plot["nilai"].apply(_bcolor)
                kab_plot["label_txt"] = kab_plot["nilai"].apply(
                    lambda v: f"{v:{fmt}}{unit if unit in ('%','x') else ''}"
                )

                fig_map = go.Figure()

                # Background boundary rectangle (very rough Jawa Timur bbox)
                fig_map.add_trace(go.Scattergeo(
                    lon=[110.5, 115.0, 115.0, 110.5, 110.5],
                    lat=[-5.8, -5.8, -9.0, -9.0, -5.8],
                    mode="lines",
                    line=dict(color="#dde4ee", width=1),
                    showlegend=False,
                    hoverinfo="skip",
                ))

                # Bubbles
                fig_map.add_trace(go.Scattergeo(
                    lon=kab_plot["lon"],
                    lat=kab_plot["lat"],
                    mode="markers+text",
                    marker=dict(
                        size=kab_plot["bsize"],
                        color=kab_plot["nilai"],
                        colorscale=chosen_cs,
                        cmin=kab_plot["nilai"].min(),
                        cmax=kab_plot["nilai"].max(),
                        opacity=0.88,
                        line=dict(color="#ffffff", width=0.8),
                        colorbar=dict(
                            title=dict(text=ind_map, font=dict(size=10)),
                            tickfont=dict(size=9), len=0.7, thickness=14, x=1.0,
                        ),
                        showscale=True,
                    ),
                    text=kab_plot["wilayah"].apply(
                        lambda w: w.replace("Kabupaten ", "Kab. ").replace("Kota ", "Kota ")
                    ),
                    textfont=dict(size=7, color="#374151"),
                    textposition="top center",
                    customdata=kab_plot[["wilayah", "label_txt"]].values,
                    hovertemplate=(
                        "<b>%{customdata[0]}</b><br>"
                        + ind_map + ": %{customdata[1]}<extra></extra>"
                    ),
                    showlegend=False,
                ))

                # Madura highlight line (cosmetic)
                fig_map.add_trace(go.Scattergeo(
                    lon=[112.6, 112.7], lat=[-7.1, -7.05],
                    mode="lines", line=dict(color="#94a3b8", width=0.5, dash="dot"),
                    showlegend=False, hoverinfo="skip",
                ))

                fig_map.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    geo=dict(
                        scope="asia",
                        resolution=50,
                        center=dict(lon=112.7, lat=-7.6),
                        projection_scale=22,
                        showland=True, landcolor="#f8fafc",
                        showcoastlines=True, coastlinecolor="#cbd5e1", coastlinewidth=0.7,
                        showocean=True, oceancolor="#e0f2fe",
                        showlakes=False,
                        bgcolor="rgba(0,0,0,0)",
                    ),
                    margin=dict(t=0, r=0, b=0, l=0),
                    height=440,
                    font=dict(family="Plus Jakarta Sans, sans-serif"),
                    hoverlabel=dict(bgcolor="#fff", font_size=12, bordercolor="#dde4ee"),
                )
                map_mode = "bubble"

            st.plotly_chart(
                fig_map, use_container_width=True, key="map_tab1",
                config={"displaylogo": False,
                        "toImageButtonOptions": {"format": "png", "filename": f"peta_jatim_{yr_map}"}},
            )

            if map_mode == "bubble":
                st.markdown(
                    '<div style="font-size:.72rem;color:#6b7280;padding:0 4px 8px;">'
                    '🔵 Ukuran & warna lingkaran proporsional terhadap nilai indikator. '
                    'Untuk peta poligon penuh, pastikan koneksi internet tersedia agar GeoJSON dapat dimuat.</div>',
                    unsafe_allow_html=True,
                )

        with col_ana:
            if len(v_clean) > 0:
                vmax  = v_clean.max(); vmin  = v_clean.min()
                vmean = v_clean.mean(); vmed  = v_clean.median()
                vstd  = v_clean.std()
                n_hi  = (v_clean > vmed).sum()
                n_lo  = len(v_clean) - n_hi

                wil_max = kab_m.loc[kab_m["nilai"].idxmax(), "wilayah"]
                wil_min = kab_m.loc[kab_m["nilai"].idxmin(), "wilayah"]

                def _fmtv(x):
                    if unit == "%": return f"{x:.2f}%"
                    if unit == "x": return f"{x:.2f}x"
                    return f"{x:,.0f}"

                # Interpretasi khusus per indikator
                interp_hi = "kondisi kritis" if "TPT" in ind_map or "Pencari" in ind_map else "potensi besar"
                interp_lo = "kondisi terbaik" if "TPT" in ind_map or "Pencari" in ind_map else "perlu perhatian"

                st.markdown(
                    f"""<div class="analisis-card"><h5>Analisis Spasial</h5>
                    <ul>
                    <li><span class="warn">Tertinggi:</span> {wil_max}
                        <br><b>{_fmtv(vmax)}</b> — {interp_hi}</li>
                    <li><span class="ok">Terendah:</span> {wil_min}
                        <br><b>{_fmtv(vmin)}</b> — {interp_lo}</li>
                    <li>Rata-rata: <span class="hi">{_fmtv(vmean)}</span></li>
                    <li>Median: <span class="hi">{_fmtv(vmed)}</span></li>
                    <li>Std. Dev: <span class="hi">{_fmtv(vstd)}</span>
                        {"— <span class='warn'>dispersi tinggi</span>" if vstd > vmean * 0.3 else "— dispersi rendah"}</li>
                    <li><span class="warn">{n_hi} wilayah</span> di atas median</li>
                    <li><span class="ok">{n_lo} wilayah</span> di bawah/sama median</li>
                    </ul></div>""",
                    unsafe_allow_html=True,
                )

                # Top-5 kritis
                top5 = kab_m[["wilayah", "nilai"]].dropna().nlargest(5, "nilai")
                bot3 = kab_m[["wilayah", "nilai"]].dropna().nsmallest(3, "nilai")

                st.markdown(
                    "<div class='analisis-card'><h5>5 Wilayah Kritis (Tertinggi)</h5>"
                    + "".join([
                        f"<div style='display:flex;justify-content:space-between;"
                        f"padding:4px 0;border-bottom:1px solid #e5e7eb;font-size:.77rem;'>"
                        f"<span>{row['wilayah']}</span>"
                        f"<span class='warn' style='font-weight:700;font-family:monospace'>{_fmtv(row['nilai'])}</span>"
                        f"</div>"
                        for _, row in top5.iterrows()
                    ])
                    + "</div>",
                    unsafe_allow_html=True,
                )

                st.markdown(
                    "<div class='analisis-card'><h5>3 Wilayah Terbaik (Terendah)</h5>"
                    + "".join([
                        f"<div style='display:flex;justify-content:space-between;"
                        f"padding:4px 0;border-bottom:1px solid #e5e7eb;font-size:.77rem;'>"
                        f"<span>{row['wilayah']}</span>"
                        f"<span class='ok' style='font-weight:700;font-family:monospace'>{_fmtv(row['nilai'])}</span>"
                        f"</div>"
                        for _, row in bot3.iterrows()
                    ])
                    + "</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.warning("Data tidak tersedia untuk tahun & indikator yang dipilih.")

        st.markdown('</div>', unsafe_allow_html=True)  # penutup chart-card Section F

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: PASAR & KEBUTUHAN KERJA
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    # ═══ KPI Tab 2 ════════════════════════════════════════════════════════
    yr2_kpi = st.selectbox("Tahun Referensi KPI", ["2025","2024","2023","2022","2021"], key="t2_kpi")
    pc2 = int(prov_lk.get(f"pencari_{yr2_kpi}",0))
    lc2 = int(prov_lk.get(f"lowongan_{yr2_kpi}",0))
    gap2 = lc2 - pc2
    rpc2 = round(lc2/pc2,2) if pc2>0 else 0

    g_class = "ok" if gap2>=0 else "warn"
    r_class = "ok" if rpc2>=1 else "warn"
    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-label">Pencari Kerja</div>
            <div class="kpi-value">{pc2:,}</div>
            <div class="kpi-delta">Tahun {yr2_kpi}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Lowongan Kerja</div>
            <div class="kpi-value">{lc2:,}</div>
            <div class="kpi-delta">Tahun {yr2_kpi}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Gap (Lowongan–Pencari)</div>
            <div class="kpi-value {'text-green-600' if gap2>=0 else 'text-red-600'}">{'+' if gap2>=0 else ''}{gap2:,}</div>
            <div class="kpi-delta {g_class}">{'Surplus ✓' if gap2>=0 else 'Kekurangan !'}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Rasio Lowongan/Pencari</div>
            <div class="kpi-value">{rpc2:.2f}x</div>
            <div class="kpi-delta {r_class}">{'Memadai ✓' if rpc2>=1 else 'Di bawah 1 — Perlu Diperhatikan'}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ═══ GRAFIK A: Tren Pencari vs Lowongan ═══════════════════════════════
    st.markdown('<div class="sec-head">A · Tren Pencari Kerja vs Lowongan 2021–2025</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fta1, _ = st.columns([2,4])
        with fta1:
            fill_t2a = st.selectbox("Area Fill", ["Tampilkan Area","Garis Saja"], key="t2a_fill")
        st.markdown('<div class="chart-card-title" style="padding:0 18px 6px;">Perbandingan Pencari Kerja vs Lowongan Tersedia (Orang)</div>', unsafe_allow_html=True)

        fig_2a = go.Figure()
        fm = "tozeroy" if fill_t2a=="Tampilkan Area" else "none"
        fig_2a.add_trace(go.Scatter(
            x=YEARS, y=PEN_Y, mode="lines+markers+text", name="Pencari Kerja",
            line=dict(color=C["biru"],width=3),
            marker=dict(size=9,color=C["biru"],line=dict(color="#fff",width=2)),
            text=[f"{v//1000}K" for v in PEN_Y], textposition="top center",
            textfont=dict(size=9,color=C["biru"]),
            fill=fm, fillcolor="rgba(0,61,122,.07)",
            hovertemplate="Pencari <b>%{x}</b>: %{y:,}<extra></extra>",
        ))
        fig_2a.add_trace(go.Scatter(
            x=YEARS, y=LOW_Y, mode="lines+markers+text", name="Lowongan Kerja",
            line=dict(color=C["oranj"],width=3,dash="dot"),
            marker=dict(size=9,color=C["oranj"],line=dict(color="#fff",width=2)),
            text=[f"{v//1000}K" for v in LOW_Y], textposition="bottom center",
            textfont=dict(size=9,color=C["oranj"]),
            fill=fm, fillcolor="rgba(244,121,32,.06)",
            hovertemplate="Lowongan <b>%{x}</b>: %{y:,}<extra></extra>",
        ))
        fig_2a.update_layout(**bps_layout({
            "xaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",dtick=1),
            "yaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",title="Orang"),
            "height":320,
        }))

        col_g, col_n = st.columns([3,1])
        with col_g:
            st.plotly_chart(fig_2a, use_container_width=True, config={"displaylogo":False,"toImageButtonOptions":{"format":"png","filename":"pencari_vs_lowongan"}})
        with col_n:
            gap_25 = PEN_Y[-1] - LOW_Y[-1]
            st.markdown(f"""<div class="analisis-card"><h5>Analisis</h5>
            <ul>
            <li>2021–2024: lowongan selalu lebih banyak dari pencari — <span class="ok">pasar kerja sehat</span>.</li>
            <li>2025: <span class="warn">pembalikan tren!</span> Pencari ({PEN_Y[-1]:,}) melampaui lowongan ({LOW_Y[-1]:,}).</li>
            <li>Gap negatif <span class="warn">{gap_25:,} orang</span> — sinyal tekanan pasar kerja meningkat.</li>
            <li>Perlu percepatan investasi dan pembukaan lapangan kerja baru.</li>
            </ul></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ═══ GRAFIK B: Gap per Wilayah ════════════════════════════════════════
    st.markdown('<div class="sec-head">B · Analisis Gap Lapangan Kerja per Wilayah</div>', unsafe_allow_html=True)
    col_b1, col_b2 = st.columns(2)

    with col_b1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fb2_yr, fb2_top = st.columns(2)
        with fb2_yr: yr_b2 = st.selectbox("Tahun", ["2025","2024","2023","2022","2021"], key="b2yr")
        with fb2_top: top_b2 = st.slider("Top N Gap", 5,20,10, key="b2top")
        st.markdown(f'<div class="chart-card-title" style="padding:0 18px 6px;">Gap Lowongan–Pencari per Wilayah ({yr_b2})</div>', unsafe_allow_html=True)

        kb2 = kab_lk.copy()
        kb2["pencari"] = kb2[f"pencari_{yr_b2}"].fillna(0).astype(int)
        kb2["lowongan"] = kb2[f"lowongan_{yr_b2}"].fillna(0).astype(int)
        kb2["gap"] = kb2["lowongan"] - kb2["pencari"]
        kb2 = kb2[kb2["pencari"]>0]
        half = top_b2//2
        gshow = pd.concat([kb2.nsmallest(half,"gap"), kb2.nlargest(half,"gap")]).sort_values("gap")
        fig_b2 = go.Figure(go.Bar(
            x=gshow["gap"], y=gshow["wilayah"], orientation="h",
            marker_color=[C["green"] if g>=0 else C["red"] for g in gshow["gap"]],
            text=gshow["gap"].apply(lambda x: f"+{x:,}" if x>=0 else f"{x:,}"),
            textposition="outside", textfont=dict(size=9),
            hovertemplate="<b>%{y}</b><br>Gap: %{x:,}<extra></extra>",
        ))
        fig_b2.update_layout(**bps_layout({
            "margin":dict(t=10,r=75,b=20,l=160),
            "xaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",title="Gap"),
            "yaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",automargin=True,tickfont=dict(size=9)),
            "height":max(320,top_b2*26),
        }))
        st.plotly_chart(fig_b2, use_container_width=True, config={"displaylogo":False,"toImageButtonOptions":{"format":"png","filename":"gap_wilayah"}})
        n_neg = (kb2["gap"]<0).sum()
        st.markdown(f"""<div class="analisis-card" style="margin-top:8px"><h5>Analisis</h5>
        <ul>
        <li><span class="warn">{n_neg} wilayah</span> mengalami kekurangan lowongan kerja tahun {yr_b2}.</li>
        <li>Hijau = surplus lowongan, merah = kekurangan — wilayah merah butuh perhatian khusus.</li>
        </ul></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fb3_yr, fb3_top = st.columns(2)
        with fb3_yr: yr_b3 = st.selectbox("Tahun", ["2025","2024","2023","2022","2021"], key="b3yr")
        with fb3_top: top_b3 = st.slider("Top N Rasio", 5,20,12, key="b3rasio")
        st.markdown(f'<div class="chart-card-title" style="padding:0 18px 6px;">Rasio Peluang Kerja Tertinggi ({yr_b3})</div>', unsafe_allow_html=True)

        kb3 = kab_lk.copy()
        kb3["pencari"] = kb3[f"pencari_{yr_b3}"].fillna(0).astype(int)
        kb3["lowongan"] = kb3[f"lowongan_{yr_b3}"].fillna(0).astype(int)
        kb3 = kb3[kb3["pencari"]>0]
        kb3["rasio"] = kb3.apply(lambda r: round(r["lowongan"]/r["pencari"],2) if r["pencari"]>0 else 0, axis=1)
        tr3 = kb3[kb3["lowongan"]>0].nlargest(top_b3,"rasio")

        fig_b3 = go.Figure(go.Bar(
            x=tr3["wilayah"], y=tr3["rasio"],
            marker_color=[C["green"] if r>=2 else C["biru"] if r>=1 else C["red"] for r in tr3["rasio"]],
            text=[f"{r:.2f}x" for r in tr3["rasio"]], textposition="outside", textfont=dict(size=9),
            hovertemplate="<b>%{x}</b><br>Rasio: %{y:.2f}x<extra></extra>",
        ))
        fig_b3.add_hline(y=1.0, line_dash="dash", line_color=C["red"],
            annotation_text="Batas seimbang (1x)", annotation_font_color=C["red"])
        fig_b3.update_layout(**bps_layout({
            "yaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",title="Rasio",
                range=[0,tr3["rasio"].max()*1.25 if len(tr3)>0 else 5]),
            "xaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",tickangle=-35,tickfont=dict(size=8)),
            "height":max(320,top_b3*22),
        }))
        st.plotly_chart(fig_b3, use_container_width=True, config={"displaylogo":False,"toImageButtonOptions":{"format":"png","filename":"rasio_peluang"}})
        best_rasio = tr3.iloc[0] if len(tr3)>0 else None
        if best_rasio is not None:
            st.markdown(f"""<div class="analisis-card" style="margin-top:8px"><h5>Analisis</h5>
            <ul>
            <li>Rasio &gt;1 = lowongan melebihi pencari — <span class="ok">kondisi ideal</span>.</li>
            <li>Terbaik: <span class="hi">{best_rasio['wilayah']} ({best_rasio['rasio']:.2f}x)</span> — peluang kerja sangat terbuka.</li>
            </ul></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ═══ GRAFIK C: Jam Kerja per Umur ════════════════════════════════════
    st.markdown('<div class="sec-head">C · Profil Pekerja Penuh per Kelompok Umur</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fc_umur, _ = st.columns([2,4])
        with fc_umur:
            yr_umur = st.selectbox("Tahun", [y for y in [2025,2023,2022,2021] if y in df_ju["tahun"].values], key="c_umur")
        st.markdown(f'<div class="chart-card-title" style="padding:0 18px 6px;">Proporsi Pekerja Penuh (35+ jam) per Kelompok Umur ({yr_umur})</div>', unsafe_allow_html=True)

        d_umur = df_ju[df_ju["tahun"]==yr_umur].copy()
        d_umur["pct"] = d_umur.apply(lambda r: r["35plus"]/r["total"]*100 if r["total"]>0 else 0, axis=1)
        bar_c_umur = [C["green"] if v>=60 else C["biru2"] if v>=40 else C["oranj"] for v in d_umur["pct"]]
        fig_c_umur = go.Figure(go.Bar(
            x=d_umur["umur"], y=d_umur["pct"],
            marker_color=bar_c_umur,
            text=[f"{v:.1f}%" for v in d_umur["pct"]], textposition="outside", textfont=dict(size=9),
            hovertemplate="<b>%{x}</b><br>Pekerja penuh: %{y:.1f}%<extra></extra>",
        ))
        fig_c_umur.add_hline(y=60, line_dash="dash", line_color=C["oranj"],
            annotation_text="Threshold 60%", annotation_font_color=C["oranj"])
        fig_c_umur.update_layout(**bps_layout({
            "yaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",range=[0,115],title="%"),
            "xaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0"),
            "height":320,
        }))
        col_g, col_n = st.columns([3,1])
        with col_g:
            st.plotly_chart(fig_c_umur, use_container_width=True, config={"displaylogo":False,"toImageButtonOptions":{"format":"png","filename":"jam_umur"}})
        with col_n:
            st.markdown("""<div class="analisis-card"><h5>Analisis</h5>
            <ul>
            <li>Usia <span class="hi">25–49 tahun</span> — usia produktif inti — memiliki proporsi pekerja penuh tertinggi.</li>
            <li>Usia <span class="warn">15–19 tahun</span> terendah: masih sekolah atau baru masuk pasar kerja.</li>
            <li>Usia <span class="warn">60+ tahun</span> rendah karena cenderung paruh waktu / sektor informal.</li>
            <li>Perlu program magang & vokasi untuk percepat kesiapan kerja anak muda.</li>
            </ul></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ═══ SECTION D: Pemetaan Spasial Pasar Kerja ═════════════════════════
    st.markdown(
        '<div class="sec-head">D · Pemetaan Spasial Pasar Kerja Jawa Timur</div>',
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)

        # ── Filter row ──────────────────────────────────────────────────────────
        fd1, fd2, fd3 = st.columns([1, 1, 2])
        with fd1:
            yr_map_d = st.selectbox(
                "Tahun", ["2025", "2024", "2023", "2022", "2021"], key="d_map_yr"
            )
        with fd2:
            ind_map_d = st.selectbox(
                "Indikator",
                ["Pencari Kerja (Orang)", "Lowongan Kerja (Orang)", "Rasio Lowongan/Pencari"],
                key="d_map_ind",
            )
        with fd3:
            cs_opt_d = st.selectbox(
                "Skema Warna",
                ["RdYlGn_r — Merah=Kritis", "Blues", "YlOrRd", "Viridis"],
                key="d_map_cs",
            )

        st.markdown(
            f'<div class="chart-card-title" style="padding:0 18px 8px;">'
            f'Peta Sebaran <b>{ind_map_d}</b> per Kab/Kota — {yr_map_d}</div>',
            unsafe_allow_html=True,
        )

        # ── Build nilai per kab/kota ────────────────────────────────────────────
        kab_d = df_tpt[df_tpt["wilayah"].str.strip() != "Jawa Timur"].copy() if 'TPT' in ind_map_d or 'TPT (%)' == ind_map_d else kab_lk.copy()
        if 'TPT' in ind_map_d or 'TPT (%)' == ind_map_d:
            kab_d["wilayah_norm"] = kab_d["wilayah"].apply(_norm)
            if ind_map_d == "TPT (%)":
                kab_d["nilai"] = pd.to_numeric(kab_d[yr_map_d], errors="coerce")
                unit, fmt = "%", ".2f"
            else:
                # For Pencari/Lowongan in tab 2 context, still use kab_lk
                kab_d = kab_lk.copy()
                kab_d["wilayah_norm"] = kab_d["wilayah"].apply(_norm)
                field = "pencari" if "Pencari" in ind_map_d else "lowongan"
                col_lk = f"{field}_{yr_map_d}"
                kab_d["nilai"] = pd.to_numeric(kab_lk[col_lk], errors="coerce")
                unit, fmt = "orang", ",.0f"
        else:
            kab_d = kab_lk.copy()
            kab_d["wilayah_norm"] = kab_d["wilayah"].apply(_norm)
            if ind_map_d in ("Pencari Kerja (Orang)", "Lowongan Kerja (Orang)"):
                field = "pencari" if "Pencari" in ind_map_d else "lowongan"
                col_lk = f"{field}_{yr_map_d}"
                kab_d["nilai"] = pd.to_numeric(kab_lk[col_lk], errors="coerce")
                unit, fmt = "orang", ",.0f"
            else:  # Rasio
                pen = kab_lk[f"pencari_{yr_map_d}"].replace(0, np.nan)
                kab_d["nilai"] = (kab_lk[f"lowongan_{yr_map_d}"] / pen).round(2)
                unit, fmt = "x", ".2f"

        kab_d["nilai"] = pd.to_numeric(kab_d["nilai"], errors="coerce")
        v_clean = kab_d["nilai"].dropna()

        # ── Koordinat ──────────────────────────────────────────────────────────
        def _coord_d(wil):
            k = _fuzzy_match(wil, list(_JATIM_CENTROIDS.keys()))
            return _JATIM_CENTROIDS.get(k, (None, None))

        kab_d["lat"] = kab_d["wilayah"].apply(lambda w: _coord_d(w)[0])
        kab_d["lon"] = kab_d["wilayah"].apply(lambda w: _coord_d(w)[1])

        # ── Color scale mapping ─────────────────────────────────────────────────
        _CS_d = {
            "RdYlGn_r — Merah=Kritis": "RdYlGn_r",
            "Blues":  "Blues",
            "YlOrRd": "YlOrRd",
            "Viridis": "Viridis",
        }
        chosen_cs_d = _CS_d.get(cs_opt_d, "RdYlGn_r")

        # ── Attempt choropleth, fallback to bubble map ──────────────────────────
        gj_d = _load_geojson()
        col_map_d, col_ana_d = st.columns([3, 1])

        with col_map_d:
            if gj_d and gj_d.get("features"):
                # ── Choropleth (full polygon fill) ─────────────────────────────
                props0_d = gj_d["features"][0]["properties"]
                name_key_d = next(
                    (k for k in ["name", "NAME", "KABKOT", "WADMKK", "kabupaten", "kota"]
                    if k in props0_d),
                    list(props0_d.keys())[0],
                )
                geo_names_d = [f["properties"].get(name_key_d, "") for f in gj_d["features"]]
                kab_d["geo_name"] = kab_d["wilayah"].apply(
                    lambda w: _fuzzy_match(w, geo_names_d) or w
                )
                hover_lbl_d = ind_map_d.replace(" (%)", "").replace(" (Orang)", "").replace("/", " per ")
                fig_map_d = px.choropleth(
                    kab_d.dropna(subset=["nilai", "geo_name"]),
                    geojson=gj_d,
                    locations="geo_name",
                    featureidkey=f"properties.{name_key_d}",
                    color="nilai",
                    color_continuous_scale=chosen_cs_d,
                    hover_name="wilayah",
                    hover_data={"nilai": f":{fmt}", "geo_name": False},
                    labels={"nilai": hover_lbl_d},
                )
                fig_map_d.update_geos(fitbounds="locations", visible=False)
                fig_map_d.update_coloraxes(colorbar=dict(
                    title=dict(text=hover_lbl_d, font=dict(size=10)),
                    tickfont=dict(size=9), len=0.75, thickness=14,
                ))
                fig_map_d.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", geo_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10, r=10, b=10, l=10), height=440,
                    font=dict(family="Plus Jakarta Sans, sans-serif"),
                    hoverlabel=dict(bgcolor="#fff", font_size=12, bordercolor="#dde4ee"),
                )
                map_mode_d = "choropleth"
            else:
                # ── Bubble map (scatter_geo) — offline-safe ─────────────────────
                kab_plot_d = kab_d.dropna(subset=["nilai", "lat", "lon"]).copy()

                # Normalise bubble size (min 6, max 40)
                v_range_d = kab_plot_d["nilai"].max() - kab_plot_d["nilai"].min()
                if v_range_d > 0:
                    kab_plot_d["bsize"] = 6 + 34 * (kab_plot_d["nilai"] - kab_plot_d["nilai"].min()) / v_range_d
                else:
                    kab_plot_d["bsize"] = 20

                # Color by quantile
                q25_d = kab_plot_d["nilai"].quantile(0.25)
                q75_d = kab_plot_d["nilai"].quantile(0.75)
                def _bcolor_d(v):
                    if v >= q75_d:   return C["red"]
                    if v >= kab_plot_d["nilai"].median(): return C["oranj"]
                    if v >= q25_d:   return C["biru2"]
                    return C["green"]
                kab_plot_d["bcolor"] = kab_plot_d["nilai"].apply(_bcolor_d)
                kab_plot_d["label_txt"] = kab_plot_d["nilai"].apply(
                    lambda v: f"{v:{fmt}}{unit if unit in ('%','x') else ''}"
                )

                fig_map_d = go.Figure()

                # Background boundary rectangle (very rough Jawa Timur bbox)
                fig_map_d.add_trace(go.Scattergeo(
                    lon=[110.5, 115.0, 115.0, 110.5, 110.5],
                    lat=[-5.8, -5.8, -9.0, -9.0, -5.8],
                    mode="lines",
                    line=dict(color="#dde4ee", width=1),
                    showlegend=False,
                    hoverinfo="skip",
                ))

                # Bubbles
                fig_map_d.add_trace(go.Scattergeo(
                    lon=kab_plot_d["lon"],
                    lat=kab_plot_d["lat"],
                    mode="markers+text",
                    marker=dict(
                        size=kab_plot_d["bsize"],
                        color=kab_plot_d["nilai"],
                        colorscale=chosen_cs_d,
                        cmin=kab_plot_d["nilai"].min(),
                        cmax=kab_plot_d["nilai"].max(),
                        opacity=0.88,
                        line=dict(color="#ffffff", width=0.8),
                        colorbar=dict(
                            title=dict(text=ind_map_d, font=dict(size=10)),
                            tickfont=dict(size=9), len=0.7, thickness=14, x=1.0,
                        ),
                        showscale=True,
                    ),
                    text=kab_plot_d["wilayah"].apply(
                        lambda w: w.replace("Kabupaten ", "Kab. ").replace("Kota ", "Kota ")
                    ),
                    textfont=dict(size=7, color="#374151"),
                    textposition="top center",
                    customdata=kab_plot_d[["wilayah", "label_txt"]].values,
                    hovertemplate=(
                        "<b>%{customdata[0]}</b><br>"
                        + ind_map_d + ": %{customdata[1]}<extra></extra>"
                    ),
                    showlegend=False,
                ))

                # Madura highlight line (cosmetic)
                fig_map_d.add_trace(go.Scattergeo(
                    lon=[112.6, 112.7], lat=[-7.1, -7.05],
                    mode="lines", line=dict(color="#94a3b8", width=0.5, dash="dot"),
                    showlegend=False, hoverinfo="skip",
                ))

                fig_map_d.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    geo=dict(
                        scope="asia",
                        resolution=50,
                        center=dict(lon=112.7, lat=-7.6),
                        projection_scale=22,
                        showland=True, landcolor="#f8fafc",
                        showcoastlines=True, coastlinecolor="#cbd5e1", coastlinewidth=0.7,
                        showocean=True, oceancolor="#e0f2fe",
                        showlakes=False,
                        bgcolor="rgba(0,0,0,0)",
                    ),
                    margin=dict(t=0, r=0, b=0, l=0),
                    height=440,
                    font=dict(family="Plus Jakarta Sans, sans-serif"),
                    hoverlabel=dict(bgcolor="#fff", font_size=12, bordercolor="#dde4ee"),
                )
                map_mode_d = "bubble"

            st.plotly_chart(
                fig_map_d, use_container_width=True, key="map_tab2",
                config={"displaylogo": False,
                        "toImageButtonOptions": {"format": "png", "filename": f"peta_jatim_{yr_map_d}"}},
            )

            if map_mode_d == "bubble":
                st.markdown(
                    '<div style="font-size:.72rem;color:#6b7280;padding:0 4px 8px;">'
                    '🔵 Ukuran & warna lingkaran proporsional terhadap nilai indikator. '
                    'Untuk peta poligon penuh, pastikan koneksi internet tersedia agar GeoJSON dapat dimuat.</div>',
                    unsafe_allow_html=True,
                )

        with col_ana_d:
            if len(v_clean) > 0:
                vmax_d  = v_clean.max(); vmin_d  = v_clean.min()
                vmean_d = v_clean.mean(); vmed_d  = v_clean.median()
                vstd_d  = v_clean.std()
                n_hi_d  = (v_clean > vmed_d).sum()
                n_lo_d  = len(v_clean) - n_hi_d

                wil_max_d = kab_d.loc[kab_d["nilai"].idxmax(), "wilayah"]
                wil_min_d = kab_d.loc[kab_d["nilai"].idxmin(), "wilayah"]

                def _fmtv_d(x):
                    if unit == "%": return f"{x:.2f}%"
                    if unit == "x": return f"{x:.2f}x"
                    return f"{x:,.0f}"

                # Interpretasi khusus per indikator
                interp_hi_d = "kondisi kritis" if "TPT" in ind_map_d or "Pencari" in ind_map_d else "potensi besar"
                interp_lo_d = "kondisi terbaik" if "TPT" in ind_map_d or "Pencari" in ind_map_d else "perlu perhatian"

                st.markdown(
                    f"""<div class="analisis-card"><h5>Analisis Spasial</h5>
                    <ul>
                    <li><span class="warn">Tertinggi:</span> {wil_max_d}
                        <br><b>{_fmtv_d(vmax_d)}</b> — {interp_hi_d}</li>
                    <li><span class="ok">Terendah:</span> {wil_min_d}
                        <br><b>{_fmtv_d(vmin_d)}</b> — {interp_lo_d}</li>
                    <li>Rata-rata: <span class="hi">{_fmtv_d(vmean_d)}</span></li>
                    <li>Median: <span class="hi">{_fmtv_d(vmed_d)}</span></li>
                    <li>Std. Dev: <span class="hi">{_fmtv_d(vstd_d)}</span>
                        {"— <span class='warn'>dispersi tinggi</span>" if vstd_d > vmean_d * 0.3 else "— dispersi rendah"}</li>
                    <li><span class="warn">{n_hi_d} wilayah</span> di atas median</li>
                    <li><span class="ok">{n_lo_d} wilayah</span> di bawah/sama median</li>
                    </ul></div>""",
                    unsafe_allow_html=True,
                )

                # Top-5 kritis
                top5_d = kab_d[["wilayah", "nilai"]].dropna().nlargest(5, "nilai")
                bot3_d = kab_d[["wilayah", "nilai"]].dropna().nsmallest(3, "nilai")

                st.markdown(
                    "<div class='analisis-card'><h5>5 Wilayah Kritis (Tertinggi)</h5>"
                    + "".join([
                        f"<div style='display:flex;justify-content:space-between;"
                        f"padding:4px 0;border-bottom:1px solid #e5e7eb;font-size:.77rem;'>"
                        f"<span>{row['wilayah']}</span>"
                        f"<span class='warn' style='font-weight:700;font-family:monospace'>{_fmtv_d(row['nilai'])}</span>"
                        f"</div>"
                        for _, row in top5_d.iterrows()
                    ])
                    + "</div>",
                    unsafe_allow_html=True,
                )

                st.markdown(
                    "<div class='analisis-card'><h5>3 Wilayah Terbaik (Terendah)</h5>"
                    + "".join([
                        f"<div style='display:flex;justify-content:space-between;"
                        f"padding:4px 0;border-bottom:1px solid #e5e7eb;font-size:.77rem;'>"
                        f"<span>{row['wilayah']}</span>"
                        f"<span class='ok' style='font-weight:700;font-family:monospace'>{_fmtv_d(row['nilai'])}</span>"
                        f"</div>"
                        for _, row in bot3_d.iterrows()
                    ])
                    + "</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.warning("Data tidak tersedia untuk tahun & indikator yang dipilih.")

        st.markdown('</div>', unsafe_allow_html=True)  # penutup chart-card Section D

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: ANALISIS MENDALAM
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    # ═══ GRAFIK A: Clustering ════════════════════════════════════════════
    st.markdown('<div class="sec-head">A · Pemetaan Zona Ketenagakerjaan (K-Means Clustering)</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        cl_c1, cl_c2 = st.columns(2)
        with cl_c1: yr3 = st.selectbox("Tahun Clustering", ["2025","2024","2023","2022","2021"], key="t3yr")
        with cl_c2: n_cl = st.slider("Jumlah Cluster", 2, 5, 3, key="t3ncl")
        st.markdown(f'<div class="chart-card-title" style="padding:0 18px 6px;">Scatter: TPT vs Pencari Kerja — Segmentasi K-Means ({yr3}, {n_cl} Cluster)</div>', unsafe_allow_html=True)

        # Build clustering
        df_cl = df_tpt[df_tpt["wilayah"].str.strip()!="Jawa Timur"][["wilayah",yr3]].copy()
        df_cl = df_cl.rename(columns={yr3:"tpt"})
        df_cl["tpt"] = pd.to_numeric(df_cl["tpt"], errors="coerce")
        def nn(s): return str(s).strip().replace("Kabupaten ","Kab. ").replace("  "," ")
        df_cl["wn"] = df_cl["wilayah"].apply(nn)
        duf = df_uf.copy(); duf["wn"] = duf["wilayah"].apply(nn)
        df_cl = df_cl.merge(duf[["wn","upah_total"]], on="wn", how="left")
        dlk = kab_lk[["wilayah",f"pencari_{yr3}"]].copy(); dlk["wn"]=dlk["wilayah"].apply(nn)
        df_cl = df_cl.merge(dlk[["wn",f"pencari_{yr3}"]], on="wn", how="left")
        df_cl = df_cl.rename(columns={f"pencari_{yr3}":"pencari"})
        df_cl["pencari"] = df_cl["pencari"].fillna(df_cl["pencari"].median())
        df_cl["upah_total"] = df_cl["upah_total"].fillna(df_cl["upah_total"].median())
        df_cl = df_cl.dropna(subset=["tpt","upah_total","pencari"])

        X = StandardScaler().fit_transform(df_cl[["tpt","upah_total","pencari"]])
        km = KMeans(n_clusters=n_cl, random_state=42, n_init=10)
        df_cl["cluster_raw"] = km.fit_predict(X)
        means = df_cl.groupby("cluster_raw")["tpt"].mean().sort_values(ascending=False)
        rmap = {means.index[i]: i+1 for i in range(n_cl)}
        df_cl["cluster"] = df_cl["cluster_raw"].map(rmap)
        cl_names = {1:"Prioritas Tinggi",2:"Potensial",3:"Mandiri",4:"Stabil",5:"Khusus"}
        df_cl["cluster_label"] = df_cl["cluster"].map({i:f"C{i} — {cl_names.get(i,str(i))}" for i in range(1,n_cl+1)})
        pal = [C["red"],C["oranj"],C["green"],C["biru2"],C["purple"]]
        CLC = {f"C{i} — {cl_names.get(i,str(i))}": pal[i-1] for i in range(1,n_cl+1)}

        # KPI mini
        k_cols = st.columns(4)
        k_cols[0].metric("Cluster 1 — Prioritas", f"{(df_cl.cluster==1).sum()} Kab/Kota")
        k_cols[1].metric("Cluster 2 — Potensial", f"{(df_cl.cluster==2).sum()} Kab/Kota")
        k_cols[2].metric("Cluster 3 — Mandiri", f"{(df_cl.cluster==3).sum()} Kab/Kota")
        k_cols[3].metric("Total Dianalisis", f"{len(df_cl)} Kab/Kota")

        fig_cl = px.scatter(df_cl, x="pencari", y="tpt", color="cluster_label",
            size="upah_total", hover_name="wilayah", text="wn",
            color_discrete_map=CLC,
            labels={"pencari":f"Pencari Kerja","tpt":f"TPT (%)","cluster_label":"Cluster"},
        )
        fig_cl.update_traces(textposition="top center", textfont_size=7)
        fig_cl.update_layout(**bps_layout({
            "height":400,
            "legend":dict(bgcolor="rgba(0,0,0,0)",font=dict(size=10),orientation="h",y=-0.18),
        }))
        col_g, col_n = st.columns([3,1])
        with col_g:
            st.plotly_chart(fig_cl, use_container_width=True, config={"displaylogo":False,"toImageButtonOptions":{"format":"png","filename":"clustering"}})
        with col_n:
            c1_names = ", ".join(df_cl[df_cl.cluster==1]["wn"].head(3).tolist())
            c3_names = ", ".join(df_cl[df_cl.cluster==3]["wn"].head(3).tolist())
            st.markdown(f"""<div class="analisis-card"><h5>Analisis</h5>
            <ul>
            <li><span class="warn">Cluster 1 (Prioritas):</span> TPT tinggi, upah rendah. Contoh: {c1_names}. Butuh intervensi segera.</li>
            <li><span style="color:{C['oranj']};font-weight:700">Cluster 2 (Potensial):</span> Skala pencari kerja besar, cocok untuk penyerapan investasi industri.</li>
            <li><span class="ok">Cluster 3 (Mandiri):</span> Kondisi paling sehat. Contoh: {c3_names}.</li>
            <li>K-Means menggunakan 3 variabel: TPT, Upah Formal, Pencari Kerja.</li>
            </ul></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Treemap + Bar rata-rata TPT per Cluster
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-card-title" style="padding:10px 18px 6px;">Hierarki Zona Kerentanan (Treemap)</div>', unsafe_allow_html=True)
        fig_tree = px.treemap(df_cl, path=[px.Constant("Jawa Timur"),"cluster_label","wn"],
            values="tpt", color="cluster_label", color_discrete_map=CLC)
        fig_tree.update_layout(**bps_layout({"margin":dict(t=10,r=10,b=10,l=10),"height":320,"legend":{"visible":False}}))
        st.plotly_chart(fig_tree, use_container_width=True, config={"displaylogo":False,"toImageButtonOptions":{"format":"png","filename":"treemap_cluster"}})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_t2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-card-title" style="padding:10px 18px 6px;">Rata-rata TPT per Cluster</div>', unsafe_allow_html=True)
        clsm = df_cl.groupby(["cluster","cluster_label"]).agg(tpt_mean=("tpt","mean")).reset_index()
        fig_clbar = go.Figure(go.Bar(
            x=clsm["cluster_label"], y=clsm["tpt_mean"],
            marker_color=[pal[i-1] for i in clsm["cluster"]],
            text=[f"{v:.2f}%" for v in clsm["tpt_mean"]],
            textposition="outside", textfont=dict(size=11,family="monospace"),
            hovertemplate="<b>%{x}</b><br>TPT rata-rata: %{y:.2f}%<extra></extra>",
        ))
        fig_clbar.update_layout(**bps_layout({
            "yaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",title="TPT (%)"),
            "xaxis":dict(gridcolor="#f0f4f8",zerolinecolor="#e4e9f0",tickangle=-10,tickfont=dict(size=9)),
            "legend":dict(visible=False),"height":320,"margin":dict(t=10,r=20,b=80,l=60),
        }))
        st.plotly_chart(fig_clbar, use_container_width=True, config={"displaylogo":False,"toImageButtonOptions":{"format":"png","filename":"tpt_cluster"}})
        st.markdown('</div>', unsafe_allow_html=True)

    # ═══ GRAFIK B: Korelasi ════════════════════════════════════════════════
    st.markdown('<div class="sec-head">B · Korelasi Upah Formal vs Tingkat Pengangguran</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-card-title" style="padding:10px 18px 6px;">Heatmap Korelasi & Regression Plot: Upah Formal vs TPT</div>', unsafe_allow_html=True)

        fig_cor = make_subplots(rows=1, cols=2,
            subplot_titles=["Heatmap Korelasi (Pearson)","Regression: Upah Formal vs TPT"],
            column_widths=[0.38, 0.62])
        corr = df_cl[["tpt","upah_total","pencari"]].rename(
            columns={"tpt":"TPT","upah_total":"Upah","pencari":"Pencari"}).corr()
        fig_cor.add_trace(go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.index,
            colorscale=[[0,C["red"]],[0.5,"#f8fafc"],[1,C["biru"]]],
            zmid=0, zmin=-1, zmax=1,
            text=[[f"{v:.2f}" for v in row] for row in corr.values],
            texttemplate="%{text}", textfont=dict(size=13,color="#111827",family="monospace"),
            showscale=False,
        ), row=1, col=1)
        umk_a = df_cl["upah_total"].values; tpt_a = df_cl["tpt"].values
        rv = np.corrcoef(umk_a, tpt_a)[0,1]
        reg = LinearRegression().fit(umk_a.reshape(-1,1), tpt_a)
        xl = np.linspace(umk_a.min(), umk_a.max(), 100)
        yl = reg.predict(xl.reshape(-1,1))
        fig_cor.add_trace(go.Scatter(
            x=umk_a/1e6, y=tpt_a, mode="markers",
            marker=dict(size=9, color=[CLC[c] for c in df_cl["cluster_label"]], opacity=0.85),
            name="Kab/Kota", showlegend=False,
        ), row=1, col=2)
        fig_cor.add_trace(go.Scatter(
            x=xl/1e6, y=yl, mode="lines", name="Trendline",
            line=dict(color=C["red"],width=2,dash="dash"), showlegend=False,
        ), row=1, col=2)
        fig_cor.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans",color="#374151",size=11), height=380,
            annotations=list(fig_cor.layout.annotations) + [
                dict(x=xl.max()/1e6*0.85, y=tpt_a.max()*0.92,
                    text=f"r = {rv:.2f}", showarrow=False, xref="x2", yref="y2",
                    font=dict(size=14,color=C["red"],family="monospace"),
                    bgcolor="#fee2e2", bordercolor=C["red"], borderwidth=1, borderpad=5)],
            margin=dict(t=40,r=20,b=40,l=60),
        )
        fig_cor.update_xaxes(gridcolor="#f0f4f8", zerolinecolor="#e4e9f0")
        fig_cor.update_yaxes(gridcolor="#f0f4f8", zerolinecolor="#e4e9f0")
        col_g, col_n = st.columns([3,1])
        with col_g:
            st.plotly_chart(fig_cor, use_container_width=True, config={"displaylogo":False,"toImageButtonOptions":{"format":"png","filename":"korelasi"}})
        with col_n:
            dir_kata = "negatif kuat" if rv < -0.5 else "negatif sedang" if rv < 0 else "positif"
            st.markdown(f"""<div class="analisis-card"><h5>Analisis</h5>
            <ul>
            <li>Korelasi Upah vs TPT = <span class="hi">r = {rv:.2f}</span> ({dir_kata}).</li>
            <li>Daerah dengan upah formal lebih tinggi cenderung memiliki <span class="ok">TPT lebih rendah</span>.</li>
            <li>Artinya: menaikkan UMK tidak otomatis menambah pengangguran — justru mencerminkan ekonomi daerah yang lebih produktif.</li>
            <li>Data dari <span class="hi">{len(df_cl)} kabupaten/kota</span> Jawa Timur.</li>
            </ul></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ═══ GRAFIK C: Forecasting ARIMA ══════════════════════════════════════════
    st.markdown('<div class="sec-head">C · Forecasting TPT Jawa Timur</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        ff1, ff2 = st.columns([2, 2])
        with ff1:
            arima_order = st.selectbox(
                "Order ARIMA (p,d,q)",
                ["Auto (AIC terbaik)", "(1,1,1)", "(2,1,1)", "(1,1,2)", "(2,1,2)", "(0,1,1)"],
                key="t3fc"
            )
        with ff2:
            tahun_pred_end = st.selectbox("Prediksi hingga tahun", [2026, 2027, 2028, 2029, 2030], index=4, key="t3fc_end")

        st.markdown('<div class="chart-card-title" style="padding:0 18px 6px;">Proyeksi TPT Jawa Timur — ARIMA</div>', unsafe_allow_html=True)

        # Ambil data Jawa Timur dari semua tahun 2001-2025
        df_tpt = load_tpt()
        jatim_row = df_tpt[df_tpt["wilayah"].str.contains("Jawa Timur", case=False, na=False)]
        all_years = sorted([int(c) for c in df_tpt.columns if c != "wilayah"])
        if not jatim_row.empty:
            tpt_series = [float(jatim_row[str(y)].values[0]) for y in all_years]
        else:
            # fallback ke konstanta YEARS/TPT_Y jika ada
            all_years = YEARS
            tpt_series = TPT_Y

        # Filter NaN
        valid = [(y, v) for y, v in zip(all_years, tpt_series) if not np.isnan(v)]
        hist_years = [x[0] for x in valid]
        hist_vals  = [x[1] for x in valid]

        # Fit ARIMA
        from statsmodels.tsa.arima.model import ARIMA
        from statsmodels.tsa.stattools import adfuller
        import warnings, itertools

        ts = pd.Series(hist_vals, index=pd.date_range(start=str(hist_years[0]), periods=len(hist_years), freq="YE"))

        @st.cache_data
        def fit_arima(vals, order_str, end_year):
            s = pd.Series(vals, index=pd.date_range(start=str(hist_years[0]), periods=len(vals), freq="YE"))
            n_steps = end_year - hist_years[-1]

            if order_str == "Auto (AIC terbaik)":
                best_aic, best_order, best_model = np.inf, (1,1,1), None
                for p, d, q in itertools.product(range(3), range(2), range(3)):
                    try:
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            m = ARIMA(s, order=(p,d,q)).fit()
                            if m.aic < best_aic:
                                best_aic, best_order, best_model = m.aic, (p,d,q), m
                    except Exception:
                        continue
                model = best_model
                used_order = best_order
            else:
                p, d, q = map(int, order_str.strip("()").split(","))
                used_order = (p, d, q)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    model = ARIMA(s, order=(p,d,q)).fit()

            forecast = model.get_forecast(steps=n_steps)
            pred_mean = forecast.predicted_mean
            ci = forecast.conf_int(alpha=0.20)   # 80% CI
            pred_years = list(range(hist_years[-1]+1, end_year+1))
            return (
                float(model.aic),
                used_order,
                pred_years,
                pred_mean.values.tolist(),
                ci.iloc[:, 0].values.tolist(),
                ci.iloc[:, 1].values.tolist(),
            )

        try:
            aic_val, used_order, pred_years, pred_vals, ci_lo, ci_hi = fit_arima(
                tuple(hist_vals), arima_order, tahun_pred_end
            )
            arima_ok = True
        except Exception as e:
            arima_ok = False
            st.warning(f"ARIMA gagal difit: {e}. Coba order lain.")

        if arima_ok:
            fig_fc = go.Figure()

            # Data historis
            fig_fc.add_trace(go.Scatter(
                x=hist_years, y=hist_vals,
                mode="lines+markers", name="Data Historis (2001–2025)",
                line=dict(color=C["biru"], width=2.5),
                marker=dict(size=6, color=C["biru"], line=dict(color="#fff", width=1.5)),
            ))

            # Confidence interval (area)
            fig_fc.add_trace(go.Scatter(
                x=pred_years + pred_years[::-1],
                y=ci_hi + ci_lo[::-1],
                fill="toself", fillcolor="rgba(244,121,32,.15)",
                line=dict(color="rgba(0,0,0,0)"),
                showlegend=True, name="Interval Kepercayaan 80%",
            ))

            # Connector dari titik terakhir historis ke prediksi pertama
            fig_fc.add_trace(go.Scatter(
                x=[hist_years[-1]] + pred_years,
                y=[hist_vals[-1]] + pred_vals,
                mode="lines+markers+text", name=f"Prediksi ARIMA{used_order}",
                line=dict(color=C["oranj"], width=3, dash="dash"),
                marker=dict(size=9, symbol="diamond", color=C["oranj"], line=dict(color="#fff", width=2)),
                text=[""] + [f"~{v:.2f}%" for v in pred_vals],
                textposition="top center",
                textfont=dict(size=10, color=C["oranj"], family="monospace"),
            ))

            fig_fc.update_layout(**bps_layout({
                "xaxis": dict(gridcolor="#f0f4f8", zerolinecolor="#e4e9f0", dtick=2,
                            range=[2000.5, tahun_pred_end + 0.8]),
                "yaxis": dict(gridcolor="#f0f4f8", zerolinecolor="#e4e9f0", title="TPT (%)"),
                "shapes": [dict(type="line", x0=2025.5, x1=2025.5,
                                y0=0, y1=12,
                                line=dict(color="#cbd5e1", width=1.5, dash="dot"))],
                "annotations": [dict(x=2025.5, y=0.5,
                                    text="Historis | Prediksi",
                                    showarrow=False,
                                    font=dict(size=9, color="#94a3b8"),
                                    xanchor="center")],
                "height": 380,
            }))

            col_g, col_n = st.columns([3, 1])
            with col_g:
                st.plotly_chart(fig_fc, use_container_width=True,
                                config={"displaylogo": False,
                                        "toImageButtonOptions": {"format": "png", "filename": "forecasting_tpt_arima"}})
            with col_n:
                pred_str = " · ".join([f"{y}: ~{v:.2f}%" for y, v in zip(pred_years, pred_vals)])
                st.markdown(f"""<div class="analisis-card"><h5>Analisis</h5>
                <ul>
                <li>Model: <span class="hi">ARIMA{used_order}</span></li>
                <li>AIC = <span class="hi">{aic_val:.2f}</span> — semakin kecil semakin baik.</li>
                <li>Proyeksi: <span class="hi">{pred_str}</span>.</li>
                <li>Area bayangan = interval kepercayaan <span class="hi">80%</span>.</li>
                <li>Model belajar dari data <span class="hi">2001–2025</span> (25 titik).</li>
                <li>Prediksi tidak memperhitungkan <span class="warn">guncangan struktural</span> mendadak.</li>
                </ul></div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)