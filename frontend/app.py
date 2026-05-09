import streamlit as st
import requests

st.set_page_config(
    page_title="Morocco Job Finder",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Morocco Job Finder")
st.markdown("Find the latest job offers in Morocco powered by JSearch API")
st.divider()

# --- Formulaire enrichi ---
col1, col2 = st.columns(2)

with col1:
    query = st.text_input("🔍 Compétences", placeholder="e.g. python django sql")
    experience = st.text_input("💼 Expérience", placeholder="e.g. 2 ans backend")

with col2:
    formation = st.text_input("🎓 Formation", placeholder="e.g. master informatique")
    location = st.text_input("📍 Location", value="Morocco")

st.markdown("<br>", unsafe_allow_html=True)
search_btn = st.button("🔎 Rechercher", use_container_width=True, type="primary")

st.divider()

# --- Fetch & Display ---
if search_btn and query:
    with st.spinner("Analyse de votre profil en cours..."):

        response = requests.post(
            "http://localhost:8000/recommandations",
            json={
                "competences": query,
                "experience": experience,
                "formation": formation,
                "location": location
            }
        )

        data = response.json()
        jobs = data.get("recommandations", [])

    if not jobs:
        st.warning("Aucune offre trouvée. Essayez d'autres mots-clés.")
    else:
        st.success(f"✅ **{len(jobs)}** offres trouvées et classées par score")
        st.divider()

        for i, job in enumerate(jobs):
            with st.container():
                col_a, col_b = st.columns([4, 1])

                with col_a:
                    st.subheader(f"#{i+1} {job.get('job_title', 'N/A')}")
                    st.markdown(f"🏢 **{job.get('employer_name', 'Unknown')}**")
                    st.markdown(f"📍 {job.get('job_location', 'N/A')}")
                    st.markdown(f"🕒 {job.get('job_employment_type', 'N/A')}  |  📅 {job.get('job_posted_at', 'N/A')}")

                    # Score de matching
                    score = job.get("matching_score", 0)

                    if score >= 10:
                        color = "🟢"
                    elif score >= 5:
                        color = "🟡"
                    else:
                        color = "🔴"

                    st.markdown(f"### {color} Matching Score: **{score}%**")
                    st.progress(min(score / 100, 1.0))

                    description = job.get("job_description", "")
                    if description:
                        with st.expander("📄 Voir la description"):
                            st.write(description[:1000] + "..." if len(description) > 1000 else description)

                with col_b:
                    apply_link = job.get("job_apply_link", "#")
                    st.markdown("<br><br>", unsafe_allow_html=True)
                    st.link_button("Postuler ➜", apply_link, use_container_width=True)

                st.divider()

elif search_btn and not query:
    st.error("⚠️ Veuillez entrer vos compétences.")
else:
    st.info("👆 Remplissez votre profil et cliquez sur Rechercher.")