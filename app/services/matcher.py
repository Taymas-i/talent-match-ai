from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from app.models import Job

class NLPJobMatcher:
    def __init__(self, db: Session):
        #upload the huggingface model for sentence
        self.db = db
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    def calculate_match_scores(self, cv_text: str):
        
        jobs = self.db.query(Job).filter(Job.is_active == True).all()

        if not jobs:
            return []
        
        job_documents = [f"{job.title} {job.description}" for job in jobs]
        job_ids = [job.id for job in jobs]

        #transform the CV and job documents into embeddings
        cv_embedding = self.model.encode([cv_text])
        job_embeddings = self.model.encode(job_documents)

        #calculate cosine similarity scores between the CV and each job
        cosine_similarities = cosine_similarity(cv_embedding, job_embeddings).flatten()

        match_results = []
        for i, score in enumerate(cosine_similarities):
            percentage_score = round(float(score) * 100, 2)
            
            match_results.append({
                "job_id": job_ids[i],
                "job_title": jobs[i].title,
                "company": jobs[i].company,
                "link": jobs[i].link,
                "match_score": percentage_score
            })
        match_results = sorted(match_results, key=lambda x: x['match_score'], reverse=True)

        return match_results
    
    def calculate_manual_match_score(self, cv_text: str, job_text: str):
        cv_embedding = self.model.encode([cv_text])
        job_embedding = self.model.encode([job_text])

        
        similarity = cosine_similarity(cv_embedding, job_embedding)[0][0]
        percentage_score = round(float(similarity) * 100, 2)

        return percentage_score
    


