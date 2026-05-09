from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv
from jsearch import fetch_jobs
from recommender import recommend
import os

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

app = FastAPI()

class Profil(BaseModel):
    competences: str
    experience: str = ""
    formation: str = ""
    location: str = "Morocco"

@app.post("/recommandations")
def get_recommandations(profil: Profil):
    
    # Combine toutes les infos en un seul texte
    profil_complet = f"{profil.competences} {profil.experience} {profil.formation}"
    
    # Récupère les offres JSearch
    jobs = fetch_jobs(
        query=profil.competences,
        location=profil.location,
        num_pages=2
    )
    
    # Passe dans recommender avec le profil complet
    top10 = recommend(
        profil=profil_complet,
        offres=jobs,
        top_n=10
    )
    
    return {"total": len(top10), "recommandations": top10}