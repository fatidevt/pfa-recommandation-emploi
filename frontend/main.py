from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv
from jsearch import fetch_jobs
from recommender import recommend
import os

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Debug - vérifie la clé
print("CLE API:", os.getenv("JSEARCH_API_KEY"))

app = FastAPI()

class Profil(BaseModel):
    competences: str
    location: str = "Morocco"

@app.post("/recommandations")
def get_recommandations(profil: Profil):
    
    jobs = fetch_jobs(
        query=profil.competences,
        location=profil.location,
        num_pages=2
    )
    
    print("Nombre offres récupérées:", len(jobs))
    
    top10 = recommend(
        profil=profil.competences,
        offres=jobs,
        top_n=10
    )
    
    return {"total": len(top10), "recommandations": top10}