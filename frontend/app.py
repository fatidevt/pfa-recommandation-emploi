import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(
    page_title="Morocco Job Recommender",
    page_icon="💼",
    layout="wide"
)

# --- Custom CSS corrige ---
st.markdown("""
    <style>
        .job-card {
            background-color: #EAF3FB;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            border-left: 5px solid #2E75B6;
        }
        .score-high { color: #1A5C33; font-weight: bold; font-size: 18px; }
        .score-mid  { color: #B8860B; font-weight: bold; font-size: 18px; }
        .score-low  { color: #C0392B; font-weight: bold; font-size: 18px; }
        .cv-preview {
            background-color: #EAF3FB;
            border-radius: 8px;
            padding: 15px;
            border-left: 4px solid #2E75B6;
            font-size: 13px;
            color: #1F4E79;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("# 💼 Morocco Job Recommender")
st.markdown("**Système intelligent de recommandation d'offres d'emploi — JSearch API + TF-IDF**")
st.divider()

# Fonction affichage offres
def afficher_offres(jobs):
    if not jobs:
        st.warning("⚠️ Aucune offre trouvée. Essayez d'autres mots-clés.")
        return

    st.success(f"✅ **{len(jobs)} offres recommandées** — triées par score de matching")
    st.markdown("---")

    for i, job in enumerate(jobs, 1):
        score = job.get("score_matching", 0)

        if score >= 20:
            score_class = "score-high"
            score_icon  = "🟢"
        elif score >= 10:
            score_class = "score-mid"
            score_icon  = "🟡"
        else:
            score_class = "score-low"
            score_icon  = "🔴"

        with st.container():
            col_a, col_b = st.columns([4, 1])

            with col_a:
                st.markdown(f"### {i}. {job.get('job_title', 'N/A')}")
                st.markdown(f"🏢 **{job.get('employer_name', 'Unknown')}**")
                st.markdown(f"📍 {job.get('job_city', '')} {job.get('job_country', '')}")
                posted = (job.get('job_posted_at_datetime_utc') or 'N/A')[:10]
                st.markdown(f"🕒 {job.get('job_employment_type', 'N/A')}  |  📅 Publié : {posted}")

                st.markdown(f"{score_icon} **Score de matching :**")
                st.progress(min(score / 100, 1.0))
                st.markdown(
                    f'<span class="{score_class}">{score}% de compatibilité</span>',
                    unsafe_allow_html=True
                )

                description = job.get("job_description", "")
                if description:
                    with st.expander("📄 Voir la description"):
                        st.write(
                            description[:1000] + "..."
                            if len(description) > 1000
                            else description
                        )

            with col_b:
                apply_link = job.get("job_apply_link", "#")
                st.markdown("<br><br><br>", unsafe_allow_html=True)
                st.link_button("Postuler ➜", apply_link, use_container_width=True)

            st.divider()


# Deux onglets
tab1, tab2 = st.tabs(["✍️ Saisie manuelle", "📄 Upload CV PDF"])


# ONGLET 1
with tab1:
    st.markdown("### ✍️ Entrez votre profil manuellement")
    st.markdown("")

    col1, col2 = st.columns(2)

    with col1:
        competences = st.text_input(
            "🛠️ Compétences *",
            placeholder="ex: python django sql react"
        )
        experience = st.text_input(
            "💼 Expérience",
            placeholder="ex: 2 ans backend developer"
        )

    with col2:
        formation = st.text_input(
            "🎓 Formation",
            placeholder="ex: master informatique"
        )
        location = st.text_input(
            "📍 Localisation",
            value="Morocco"
        )

    st.markdown("")
    search_btn = st.button(
        "🔍 Rechercher les offres",
        use_container_width=True,
        type="primary"
    )

    if search_btn and competences:
        with st.spinner("⏳ Recherche des offres en cours..."):
            try:
                response = requests.post(
                    "http://localhost:8000/recommandations",
                    json={
                        "competences": competences,
                        "experience":  experience,
                        "formation":   formation,
                        "location":    location
                    }
                )
                data = response.json()
                jobs = data.get("recommandations", [])
                afficher_offres(jobs)

            except Exception as e:
                st.error(f"❌ Impossible de contacter FastAPI : {e}")
                st.info("👉 Lancez FastAPI : uvicorn main:app --reload")

    elif search_btn and not competences:
        st.error("⚠️ Veuillez entrer au moins une compétence.")

    else:
        st.info("👆 Renseignez vos compétences et cliquez sur Rechercher.")


# ONGLET 2
with tab2:
    st.markdown("### 📄 Uploadez votre CV en PDF")
    st.markdown("Notre système extrait automatiquement vos compétences.")
    st.markdown("")

    uploaded_file = st.file_uploader(
        "Choisissez votre CV (PDF uniquement)",
        type=["pdf"]
    )

    location_cv = st.text_input(
        "📍 Localisation souhaitée",
        value="Morocco",
        key="location_cv"
    )

    st.markdown("")
    upload_btn = st.button(
        "🚀 Analyser mon CV et trouver des offres",
        use_container_width=True,
        type="primary",
        disabled=uploaded_file is None
    )

    if uploaded_file is not None and not upload_btn:
        st.info(f"📎 Fichier sélectionné : **{uploaded_file.name}** — Cliquez sur le bouton pour analyser.")

    if upload_btn and uploaded_file is not None:
        with st.spinner("📖 Extraction du texte de votre CV..."):
            try:
                files    = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                params   = {"location": location_cv}
                response = requests.post(
                    "http://localhost:8000/upload-cv",
                    files=files,
                    params=params
                )
                data = response.json()

                texte_extrait = data.get("texte_extrait", "")
                if texte_extrait:
                    st.markdown("#### 📝 Aperçu du texte extrait de votre CV :")
                    st.markdown(
                        f'<div class="cv-preview">{texte_extrait[:500]}...</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown("")

                jobs = data.get("recommandations", [])
                afficher_offres(jobs)

            except Exception as e:
                st.error(f"❌ Erreur : {e}")
                st.info("👉 Lancez FastAPI : uvicorn main:app --reload")

    elif not uploaded_file:
        st.info("👆 Uploadez votre CV PDF pour obtenir des recommandations.")