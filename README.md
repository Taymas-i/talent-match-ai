# 🎯 TalentMatch AI: Semantic ATS & Skill Gap Analyzer

TalentMatch AI is an intelligent Applicant Tracking System (ATS) and job matching engine built with modern AI architectures. It goes beyond simple keyword matching by leveraging **SBERT (Sentence-BERT)** for deep semantic similarity and **Meta's Llama 3.1 (via Groq LPU)** for rigorous skill gap analysis.

## 🚀 Features

* **Semantic Resume Matching:** Uses `paraphrase-multilingual-MiniLM-L12-v2` to calculate cosine similarity between candidate CVs and job descriptions, understanding the actual context rather than just keyword hits.
* **LLM-Powered Skill Gap Analysis:** Integrates with Groq's high-speed API (Llama 3.1) to act as an AI Recruiter, extracting matched skills, missing technical requirements, and providing a professional readiness recommendation.
* **Automated Web Scraping:** Features a built-in background scheduler (APScheduler) that autonomously scrapes platforms like WeWorkRemotely, keeping the PostgreSQL database updated with fresh job postings.
* **Multi-Format Document Parsing:** Automatically extracts and structures text from PDF and DOCX resumes using robust parsers (`pdfplumber`, `python-docx`).
* **Modern UI/UX:** A clean, responsive dashboard built with Streamlit, separating database batch-matching from on-demand manual job analysis.

## 🛠️ Tech Stack

* **Backend:** FastAPI, Python
* **Database & ORM:** PostgreSQL, SQLAlchemy, Pydantic
* **AI & NLP:** HuggingFace (SBERT), Scikit-learn (Cosine Similarity)
* **LLM Provider:** Groq API (Llama-3.1-8b)
* **Frontend UI:** Streamlit
* **Task Scheduling:** APScheduler

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/talent-match-ai.git](https://github.com/yourusername/talent-match-ai.git)
   cd talent-match-ai