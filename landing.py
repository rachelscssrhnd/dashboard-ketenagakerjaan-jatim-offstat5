"""
Landing Page - Dashboard Ketenagakerjaan Jawa Timur
Main entry point for the employment dashboard
"""

import streamlit as st
import os

BASE = os.path.dirname(os.path.abspath(__file__))
def p(fname): return os.path.join(BASE, fname)

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Ketenagakerjaan Jawa Timur",
    page_icon=p("Logo.png"),
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── STYLING ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

*, html, body {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

html, body, .main, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .block-container {
    background: linear-gradient(135deg, #f0f4f8 0%, #ffffff 100%) !important;
}

.block-container {
    padding: 2rem !important;
    max-width: 900px !important;
}

/* LANDING PAGE CONTAINER */
.landing-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    text-align: center;
    animation: fadeIn 0.6s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* LOGO SECTION */
.logo-section {
    margin-bottom: 40px;
    display: flex;
    justify-content: center;
}

.logo-frame {
    width: 120px;
    height: 120px;
    background: linear-gradient(135deg, #003d7a 0%, #0072bc 100%);
    border-radius: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 12px 40px rgba(0,61,122,.2);
    padding: 15px;
}

.logo-frame img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

/* TITLE & SUBTITLE */
.landing-title {
    color: #003d7a;
    font-size: 2.5rem;
    font-weight: 800;
    margin: 30px 0 15px 0;
    line-height: 1.2;
}

.landing-subtitle {
    color: #0072bc;
    font-size: 1.1rem;
    font-weight: 500;
    margin-bottom: 10px;
}

.landing-description {
    color: #555;
    font-size: 1rem;
    font-weight: 400;
    margin-bottom: 50px;
    line-height: 1.6;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

/* FEATURE CARDS */
.features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 50px;
    margin-top: 40px;
}

.feature-card {
    background: #fff;
    border-radius: 16px;
    padding: 25px;
    border: 2px solid #dde4ee;
    text-align: center;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,.05);
}

.feature-card:hover {
    border-color: #f47920;
    box-shadow: 0 8px 24px rgba(244,121,32,.15);
    transform: translateY(-4px);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 12px;
}

.feature-title {
    color: #003d7a;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.feature-text {
    color: #666;
    font-size: 0.95rem;
    line-height: 1.5;
}

/* CTA BUTTON */
.cta-button-wrapper {
    display: flex;
    gap: 15px;
    justify-content: center;
    flex-wrap: wrap;
}

.cta-button {
    display: inline-block;
    padding: 14px 40px;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 600;
    text-decoration: none !important;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
}

.btn-primary {
    background: linear-gradient(135deg, #003d7a 0%, #0072bc 100%);
    color: #fff;
    box-shadow: 0 6px 20px rgba(0,61,122,.3);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0,61,122,.4);
}

.btn-secondary {
    background: #f47920;
    color: #fff;
    box-shadow: 0 6px 20px rgba(244,121,32,.2);
}

.btn-secondary:hover {
    opacity: 0.9;
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(244,121,32,.3);
}

/* FOOTER */
.landing-footer {
    margin-top: 60px;
    padding-top: 30px;
    border-top: 2px solid #dde4ee;
    color: #999;
    font-size: 0.9rem;
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .landing-title { font-size: 2rem; }
    .landing-subtitle { font-size: 1rem; }
    .landing-description { font-size: 0.95rem; }
    .features-grid { grid-template-columns: 1fr; gap: 15px; }
    .logo-frame { width: 100px; height: 100px; }
}
</style>
""", unsafe_allow_html=True)

# ─── HIDE STREAMLIT DEFAULT UI ────────────────────────────────────────────────
st.markdown("""
<style>
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── LANDING PAGE CONTENT ─────────────────────────────────────────────────────
st.markdown("""
<div class="landing-container">
    <div class="logo-section">
        <div class="logo-frame">
            <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==" alt="Logo" style="visibility:hidden;">
        </div>
    </div>
    
    <h1 class="landing-title">Dashboard Ketenagakerjaan</h1>
    <p class="landing-subtitle">Jawa Timur</p>
    <p class="landing-description">
        Eksplorasi data ketenagakerjaan terkini di Provinsi Jawa Timur dengan visualisasi interaktif 
        dan analisis mendalam untuk mendukung pengambilan keputusan yang lebih baik.
    </p>
    
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Visualisasi Data</div>
            <div class="feature-text">Grafik dan dashboard interaktif yang mudah dipahami</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Analisis Mendalam</div>
            <div class="feature-text">Insight komprehensif tentang tren ketenagakerjaan</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📥</div>
            <div class="feature-title">Export Data</div>
            <div class="feature-text">Unduh laporan dan data dalam berbagai format</div>
        </div>
    </div>
    
    <div class="cta-button-wrapper">
        <a href="/dashboard_jatim_streamlit" class="cta-button btn-primary" style="text-decoration: none !important;">
            🚀 Buka Dashboard
        </a>
        <a href="https://github.com" target="_blank" class="cta-button btn-secondary" style="text-decoration: none !important;">
            📖 Dokumentasi
        </a>
    </div>
    
    <div class="landing-footer">
        <p>Dashboard Ketenagakerjaan Jawa Timur | Data dari BPS (Badan Pusat Statistik)</p>
        <p style="margin-top: 10px; color: #ccc;">© 2026 - Offstat</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Display logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image(p("Logo.png"), width=120)
    except:
        pass
