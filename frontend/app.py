import streamlit as st
import json
from jsearch import fetch_jobs

# --- Page Config ---
st.set_page_config(
    page_title="Morocco Job Finder",
    page_icon="💼",
    layout="wide"
)

# --- Header ---
st.title("💼 Morocco Job Finder")
st.markdown("Find the latest job offers in Morocco powered by JSearch API")
st.divider()

# --- Search Bar ---
col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    query = st.text_input("🔍 Job title or keywords", placeholder="e.g. Software Developer")

with col2:
    location = st.text_input("📍 Location", value="Morocco")

with col3:
    st.markdown("<br>", unsafe_allow_html=True)  # spacing
    search_btn = st.button("Search", use_container_width=True, type="primary")

# --- Fetch & Display Jobs ---
if search_btn and query:
    with st.spinner("Fetching jobs..."):
        jobs = fetch_jobs(query=query, location=location, num_pages=2)

    if not jobs:
        st.warning("No jobs found. Try different keywords.")
    else:
        st.success(f"Found **{len(jobs)}** job offers")
        st.divider()

        for job in jobs:
            with st.container():
                col_a, col_b = st.columns([4, 1])

                with col_a:
                    st.subheader(job.get("job_title", "N/A"))
                    st.markdown(f"🏢 **{job.get('employer_name', 'Unknown')}**")
                    st.markdown(f"📍 {job.get('job_city', '')} {job.get('job_country', '')}")
                    posted_date = (job.get('job_posted_at_datetime_utc') or 'N/A')[:10]
                    st.markdown(f"🕒 {job.get('job_employment_type', 'N/A')}  |  📅 Posted: {posted_date}")


                    # Description preview
                    description = job.get("job_description", "")
                    if description:
                        with st.expander("📄 View Description"):
                            st.write(description[:1000] + "..." if len(description) > 1000 else description)

                with col_b:
                    apply_link = job.get("job_apply_link", "#")
                    st.markdown(f"<br><br>", unsafe_allow_html=True)
                    st.link_button("Apply Now ➜", apply_link, use_container_width=True)

                st.divider()

elif search_btn and not query:
    st.error("Please enter a job title or keyword.")

else:
    st.info("👆 Enter a job title above and click **Search** to find jobs.")