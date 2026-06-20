import streamlit as st
import requests
from datetime import datetime
 
st.set_page_config(
    page_title="Morocco Job Finder",
    page_icon="💼",
    layout="wide"
)
 
# ─────────────────────────────────────────────
# CSS PROFESSIONNEL
# ─────────────────────────────────────────────
 
st.markdown("""
<style>
    /* Fond général */
    .stApp {
        background-color: #f4f6f9;
    }
 
    /* Header */
    .header-box {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        padding: 40px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 30px;
    }
    .header-box h1 {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    .header-box p {
        color: #a0aec0;
        font-size: 1rem;
        margin-top: 8px;
    }
 
    /* Carte offre */
    .job-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 16px;
        border-left: 5px solid #0f3460;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        transition: transform 0.2s;
    }
    .job-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    .job-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 6px;
    }
    .job-meta {
        color: #718096;
        font-size: 0.9rem;
        margin-bottom: 12px;
    }
    .score-badge-green {
        background: #c6f6d5;
        color: #276749;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .score-badge-yellow {
        background: #fefcbf;
        color: #744210;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .score-badge-red {
        background: #fed7d7;
        color: #9b2c2c;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
 
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #ffffff;
        padding: 8px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        color: #4a5568;
    }
    .stTabs [aria-selected="true"] {
        background: #0f3460 !important;
        color: white !important;
    }
 
    /* Bouton */
    .stButton > button {
        background: linear-gradient(135deg, #0f3460, #1a1a2e);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        transition: opacity 0.2s;
    }
    .stButton > button:hover {
        opacity: 0.85;
    }
 
    /* Input */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1.5px solid #e2e8f0;
        padding: 10px 14px;
        background: #ffffff;
    }
    .stTextInput > div > div > input:focus {
        border-color: #0f3460;
        box-shadow: 0 0 0 3px rgba(15,52,96,0.1);
    }
 
    /* Stats bar */
    .stats-bar {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        display: flex;
        align-items: center;
        gap: 12px;
    }
 
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 16px 0;
    }
</style>
""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
 
st.markdown("""
<div class="header-box">
    <h1>💼 Morocco Job Finder</h1>
    <p>Système intelligent de recommandation d'emploi — propulsé par IA & JSearch API</p>
</div>
""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────
 
def format_date(raw: str) -> str:
    try:
        return datetime.strptime(raw[:10], "%Y-%m-%d").strftime("%d %b %Y")
    except:
        return "N/A"
 
def afficher_offres(jobs):
    if not jobs:
        st.warning("Aucune offre trouvée. Essayez d'autres mots-clés.")
        return
 
    st.markdown(f"""
    <div class="stats-bar">
        ✅ <strong>{len(jobs)} offres</strong> trouvées et classées par score de matching
    </div>
    """, unsafe_allow_html=True)
 
    for i, job in enumerate(jobs):
        titre = job.get('job_title') or job.get('titre', 'N/A')
        entreprise = job.get('employer_name') or job.get('entreprise', 'Unknown')
        lieu = job.get('job_city') or job.get('job_location') or job.get('lieu', 'N/A')
        lien = job.get('job_apply_link') or job.get('lien', '#')
        description = job.get('job_description') or job.get('description', '')
        emploi_type = job.get('job_employment_type', 'N/A')
        score = round(job.get("matching_score", 0), 1)
 
        if score >= 60:
            badge = f'<span class="score-badge-green">🟢 {score}% match</span>'
        elif score >= 30:
            badge = f'<span class="score-badge-yellow">🟡 {score}% match</span>'
        else:
            badge = f'<span class="score-badge-red">🔴 {score}% match</span>'
 
        st.markdown(f"""
        <div class="job-card">
            <div class="job-title">#{i+1} &nbsp; {titre}</div>
            <div class="job-meta">
                🏢 {entreprise} &nbsp;|&nbsp; 📍 {lieu} &nbsp;|&nbsp; 🕒 {emploi_type}
            </div>
            {badge}
        </div>
        """, unsafe_allow_html=True)
 
        col_desc, col_btn = st.columns([4, 1])
        with col_desc:
            if description:
                with st.expander("📄 Voir la description"):
                    st.write(description[:1000] + "..." if len(description) > 1000 else description)
        with col_btn:
            st.link_button("Postuler ➜", lien, use_container_width=True)
 
# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
 
tab1, tab2 = st.tabs(["✏️  Saisie manuelle", "📄  Upload CV"])
 
# ─────────────────────────────────────────────
# ONGLET 1 — Saisie manuelle
# ─────────────────────────────────────────────
 
with tab1:
    st.markdown("### 🔍 Décrivez votre profil")
    col1, col2 = st.columns(2)
    with col1:
        query = st.text_input("Compétences *", placeholder="ex: python django REST API")
        experience = st.text_input("Expérience", placeholder="ex: 2 ans développement backend")
    with col2:
        formation = st.text_input("Formation", placeholder="ex: Master Informatique")
        location = st.text_input("Localisation", value="Morocco")
 
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("🔎 Trouver les meilleures offres", use_container_width=True, type="primary", key="btn_manuel")
 
    st.markdown("<hr>", unsafe_allow_html=True)
 
    if search_btn and query:
        with st.spinner("🤖 Analyse de votre profil en cours..."):
            response = requests.post(
                "http://localhost:8000/recommandations",
                json={"competences": query, "experience": experience, "formation": formation, "location": location}
            )
            jobs = response.json().get("recommandations", [])
        afficher_offres(jobs)
    elif search_btn and not query:
        st.error("⚠️ Veuillez entrer vos compétences.")
    else:
        st.info("👆 Remplissez votre profil et cliquez sur Rechercher.")
 
# ─────────────────────────────────────────────
# ONGLET 2 — Upload CV
# ─────────────────────────────────────────────
 
with tab2:
    st.markdown("### 📄 Uploadez votre CV")
    st.markdown("Notre IA extrait automatiquement vos compétences et trouve les offres les plus pertinentes.")
 
    location_cv = st.text_input("Localisation", value="Morocco", key="location_cv")
    cv_file = st.file_uploader("Déposez votre CV ici (PDF uniquement)", type=["pdf"])
 
    st.markdown("<br>", unsafe_allow_html=True)
    upload_btn = st.button("🚀 Analyser mon CV", use_container_width=True, type="primary", key="btn_cv")
 
    st.markdown("<hr>", unsafe_allow_html=True)
 
    if upload_btn and cv_file:
        with st.spinner("📖 Extraction et analyse de votre CV..."):
            response = requests.post(
                f"http://localhost:8000/upload-cv?location={location_cv}",
                files={"fichier": (cv_file.name, cv_file.getvalue(), "application/pdf")}
            )
        if response.status_code == 200:
            data = response.json()
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.metric("📃 Pages extraites", data.get("num_pages", "?"))
            with col_info2:
                st.metric("📝 Mots analysés", data.get("word_count", "?"))
 
            with st.expander("👁️ Aperçu du texte extrait"):
                st.text(data.get("cv_apercu", "")[:500])
 
            afficher_offres(data.get("recommandations", []))
        else:
            st.error(f"❌ Erreur : {response.json().get('detail', 'Erreur inconnue')}")
    elif upload_btn and not cv_file:
        st.error("⚠️ Veuillez uploader un fichier PDF.")
    else:
        st.info("👆 Uploadez votre CV PDF et cliquez sur Analyser.")