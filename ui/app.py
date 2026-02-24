import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/match/"

st.set_page_config(page_title="TalentMatch AI", page_icon=":briefcase:", layout="wide")


# Title and description

st.title("TalentMatch AI")
st.markdown("### Smart Job Matching System")
st.markdown("Our AI (SBERT)-powered engine analyzes your skills and finds the most suitable job listings for you.")
st.markdown("---")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📝 CV or Skills")
    cv_text = st.text_area(
        "Paste your skills, technologies you use, or your CV text here:",
        height=300,
        placeholder="hello, i am a software developer with experience in python, machine learning, and web development..."
    )

    match_button = st.button("Find Matching Jobs",use_container_width=True)

with col2:
    st.subheader("🔍 Matching Results")

    if match_button:
        if not cv_text.split():
            st.warning("Please enter your CV or skills to find matching jobs.")
        else:
            with st.spinner("Finding the best job matches for you..."):
                try:
                    response = requests.post(API_URL, json={"cv_text": cv_text})
                    
                    if response.status_code == 200:
                        data = response.json()
                        matches = data.get("matches", data.get("detail", []))

                        if not matches:
                            st.info("No matching jobs found. Try adding more details to your CV or skills.")
                        else:
                            st.success(f"Found {len(matches)} matching jobs!")

                            for job in matches:
                                score = job["match_score"]
                                title = job["job_title"]
                                company = job["company"] if job["company"] else "Unknown Company"

                                # streamlit expander
                                with st.expander(f"{title} - {company} (harmony: %{score})"):
                                    st.markdown(f"job ID: {job['job_id']}")
                                    st.markdown(f"**Match Score:** {score}%")
                                    
                                    job_link = job.get("link", "https://weworkremotely.com")
                                    st.link_button("🔗 Go to Advertisement", url=job_link, use_container_width=True)

                    else:
                        st. error(f"API error (code: {response.status_code}): {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the API. Please make sure the backend server is running.")
