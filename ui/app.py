import streamlit as st
import requests
from document_parser import parse_cv_file

API_URL_MATCH = "http://127.0.0.1:8000/match/"
API_URL_MANUAL_MATCH = "http://127.0.0.1:8000/match/manual"

st.set_page_config(page_title="TalentMatch AI", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
        /**/
        .stButton>button {
            background-color: #2C3E50;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            transition: all 0.3s ease 0s;
        }
        .stButton>button:hover {
            background-color: #1A252F;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        }
        /**/
        div.stAlert {
            border-radius: 8px;
            border: 1px solid rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135679.png", width=60) 
    st.title("Profilinizi Oluşturun")
    st.markdown("Sistemi kullanmak için özgeçmişinizi yükleyin.")
    st.divider()
    
    uploaded_file = st.file_uploader("📄 CV Yükle (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    st.markdown("<div style='text-align: center; color: gray;'>— VEYA —</div>", unsafe_allow_html=True)
    cv_text_input = st.text_area("✍️ Yeteneklerinizi manuel yazın:", height=150, placeholder="Örnek: Python, SQL, Proje Yönetimi, İletişim Becerileri...")

cv_text = ""
if uploaded_file is not None:
    with st.spinner("Belge analiz ediliyor..."):
        cv_text = parse_cv_file(uploaded_file)
        st.sidebar.success("✅ Dosya başarıyla okundu ve vektörize edilmeye hazır!")
elif cv_text_input:
    cv_text = cv_text_input

st.title("TalentMatch AI 🚀")
st.markdown("#### Akıllı İş Eşleştirme ve Analiz Motoru")
st.markdown("Aday özgeçmişleri ile iş ilanlarını anlamsal (semantic) olarak eşleştirir ve eksik yetenek analizi yapar.")
st.divider()

tab1, tab2 = st.tabs(["📊 Veritabanı Tarama", "🎯 Derinlemesine İlan Analizi"])


with tab1:
    st.markdown("### Sistemde Kayıtlı İlanlar Arasında Ara")
    st.caption("WeWorkRemotely üzerinden çekilen ilanlar SBERT modeli ile CV'nize göre skorlanır.")
    
    match_button = st.button("🔍 Veritabanında Uygun İlanları Bul", use_container_width=True, key="db_match")
    
    if match_button:
        if not cv_text or not cv_text.strip():
            st.warning("⚠️ Lütfen sol menüden bir CV yükleyin veya yeteneklerinizi yazın.")
        else:
            with st.spinner("Ağ mimarisi çalışıyor, en iyi eşleşmeler hesaplanıyor..."):
                try:
                    response = requests.post(API_URL_MATCH, json={"cv_text": cv_text})
                    if response.status_code == 200:
                        data = response.json()
                        matches = data.get("matches", [])
                        
                        if not matches:
                            st.info("Eşleşen iş ilanı bulunamadı.")
                        else:
                            st.success(f"🎉 Tam {len(matches)} eşleşen ilan bulundu! (En iyi 5 ilan gösteriliyor)")
                            st.write("") 
                            
                            for job in matches[:5]: 
                                score = job["match_score"]

                                emoji = "🟢" if score > 50 else ("🟡" if score > 30 else "🔴")
                                
                                with st.expander(f"{emoji} {job['job_title']} - {job['company']} (Uyum: %{score})"):
                                    st.markdown(f"**Anlamsal Eşleşme Skoru:** `% {score}`")
                                    st.link_button("🔗 Orijinal İlana Git", url=job.get("link", "#"))
                    else:
                        st.error(f"API Hatası: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("API'ye bağlanılamadı. Sunucusunun çalıştığından emin olun.")

with tab2:
    st.markdown("### İstediğiniz Bir İlanı CV'nizle Karşılaştırın")
    st.caption("İlan metnini yapıştırın.")
    
    job_text_input = st.text_area("İş ilanı metni (Job Description):", height=200, placeholder="İlan detaylarını buraya yapıştırın...")
    manual_match_button = st.button("🧠 Yapay Zeka ile Analiz Et", use_container_width=True, key="manual_match")
    
    if manual_match_button:
        if not cv_text or not cv_text.strip():
            st.warning("⚠️ Lütfen sol menüden bir CV yükleyin.")
        elif not job_text_input or not job_text_input.strip():
            st.warning("⚠️ Lütfen karşılaştırmak için bir iş ilanı metni girin.")
        else:
            with st.spinner("Model çalışıyor, bu işlem birkaç saniye sürebilir..."):
                try:
                    payload = {"cv_text": cv_text, "job_text": job_text_input}
                    response = requests.post(API_URL_MANUAL_MATCH, json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        score = result.get("match_score", 0)
                        analysis = result.get("analysis", {})
                        
                        st.divider()
                        
                        c1, c2 = st.columns([1, 2])
                        with c1:
                            st.metric(label="🎯 Uyum Skoru", value=f"%{score}")
                        with c2:
                            st.markdown("#### 🧑‍💼 İK Uzmanı (LLM) Değerlendirmesi")
                            st.info(analysis.get("recommendation", "Değerlendirme yapılamadı."))
                        
                        st.write("")
                        
                        colA, colB = st.columns(2)
                        with colA:
                            st.success("✅ Karşılanan Yetenekler")
                            matched = analysis.get("matched_skills", [])
                            if matched:
                                for skill in matched:
                                    st.markdown(f"- {skill}")
                            else:
                                st.write("Eşleşen belirgin bir yetenek bulunamadı.")
                                
                        with colB:
                            st.error("🚀 Geliştirilmesi Gerekenler (Skill Gap)")
                            missing = analysis.get("missing_skills", [])
                            if missing:
                                for skill in missing:
                                    st.markdown(f"- {skill}")
                            else:
                                st.write("Harika! İlanın istediği temel yeteneklerde eksiğiniz görünmüyor.")
                                
                    else:
                        st.error(f"API Hatası: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("API'ye bağlanılamadı.")
