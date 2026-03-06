# services/llm_analyzer.py
import os
import json
from groq import Groq
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# API Key'i bul
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY bulunamadı! Lütfen .env dosyanıza GROQ_API_KEY=anahtariniz şeklinde ekleme yapın.")

# Groq İstemcisini Başlat
client = Groq(api_key=api_key)

def analyze_skill_gap(cv_text: str, job_text: str):
    """
    CV ve İş İlanını Groq (Llama 3.1) kullanarak analiz eder ve kesin JSON döner.
    """
    prompt = f"""
    Sen kıdemli bir İnsan Kaynakları (ATS) ve Teknik İşe Alım uzmanısın.
    Aşağıda bir adayın CV'si ve başvurduğu İş İlanı metni verilmiştir.
    Bu iki metni karşılaştırarak adayın güçlü yönlerini ve eksik yeteneklerini analiz et.
    
    ÇIKTI FORMATI: Sadece ve sadece geçerli bir JSON objesi döndür.
    {{
        "matched_skills": ["eşleşen yetenek 1", "eşleşen yetenek 2"],
        "missing_skills": ["ilanın istediği ama CV'de eksik olan yetenek 1", "eksik yetenek 2"],
        "recommendation": "Adayın bu pozisyon için uygunluğu hakkında profesyonel, net 2 cümlelik değerlendirme."
    }}

    ---
    CV METNİ:
    {cv_text}
    
    ---
    İŞ İLANI METNİ:
    {job_text}
    """

    try:
        # Groq API ile JSON Modunda istek atıyoruz
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict API that ONLY outputs valid JSON objects. Never output conversational text."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.0, # Yaratıcılığı sıfırlıyoruz, matematiksel kesinlik istiyoruz
            response_format={"type": "json_object"} # İŞTE BİZİ KURTARACAK OLAN SİHİRLİ ŞALTER
        )
        
        # Yanıtı doğrudan json.loads içine alabiliriz çünkü JSON Mode bunu garanti ediyor
        raw_text = chat_completion.choices[0].message.content
        return json.loads(raw_text)
        
    except Exception as e:
        print(f"Groq LLM Analiz Hatası: {e}")
        return {
            "matched_skills": [],
            "missing_skills": [],
            "recommendation": f"Sistem hatası: {str(e)}"
        }
