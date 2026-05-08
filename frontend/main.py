from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from jsearch import fetch_jobs
from recommender import calculer_scores

load_dotenv(dotenv_path="../.env")

app = FastAPI(
    title="PFA Recommandation Emploi",
    description="Système de recommandation avec JSearch + TF-IDF",
    version="2.0"
)

# ── Semaine 1 ──────────────────────────────────
@app.get("/offres")
def get_offres(competences: str, location: str = "Morocco"):
    jobs = fetch_jobs(query=competences, location=location, num_pages=1)
    return {"total": len(jobs), "offres": jobs}

# ── Semaine 2 ──────────────────────────────────
class Profil(BaseModel):
    competences: str
    experience: str = ""
    formation: str = ""
    location: str = "Morocco"

@app.post("/recommandations")
def get_recommandations(profil: Profil):
    print(f"🔍 Profil recu: {profil}")
    
    offres = fetch_jobs(
        query=profil.competences,
        location=profil.location,
        num_pages=1
    )
    print(f"📦 Nombre offres recues de JSearch: {len(offres)}")
    
    resultats = calculer_scores(profil.dict(), offres)
    print(f"✅ Nombre resultats apres scoring: {len(resultats)}")
    
    return {
        "total": len(resultats),
        "profil": profil.dict(),
        "recommandations": resultats
    }