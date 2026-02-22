from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from app.models import Job

class NLPJobMatcher:
    def __init__(self, db: Session):
        self.db = db
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def calculate_match_scores(self, cv_text: str):
        
        jobs = self.db.query(Job).filter(Job.is_active == True).all()

        if not jobs:
            return []
        
        job_documents = [f"{job.title} {job.company} {job.description}" for job in jobs]
        job_ids = [job.id for job in jobs]

        documents = [cv_text] + job_documents

        tfidf_matrix = self.vectorizer.fit_transform(documents)
        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        match_results = []
        for i, score in enumerate(cosine_similarities):

            percentage_score = round(score * 100, 2)

            match_results.append({
                "job_id": job_ids[i],
                "job_title": jobs[i].title,
                "company": jobs[i].company,
                "match_score": percentage_score
            })

        match_results = sorted(match_results, key=lambda x: x["match_score"], reverse=True)

        return match_results