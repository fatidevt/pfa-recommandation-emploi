from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv
from jsearch import fetch_jobs
from recommender import calculer_scores
from Extractor import extract_profile_from_cv
import tempfile
import os

load_dotenv(dotenv_path="../.env")

app = FastAPI(
    title="PFA Recommandation Emploi",
    description="Systeme de recommandation avec JSearch + TF-IDF",
    version="3.0"
)

# Semaine 1
@app.get("/offres")
def get_offres(competences: str, location: str = "Morocco"):
    jobs = fetch_jobs(query=competences, location=location, num_pages=1)
    return {"total": len(jobs), "offres": jobs}

# Semaine 2
class Profil(BaseModel):
    competences: str
    experience: str = ""
    formation: str = ""
    location: str = "Morocco"

@app.post("/recommandations")
def get_recommandations(profil: Profil):
    print(f"Profil recu: {profil}")
    offres = fetch_jobs(
        query=profil.competences,
        location=profil.location,
        num_pages=1
    )
    print(f"Offres recues: {len(offres)}")
    resultats = calculer_scores(profil.dict(), offres)
    print(f"Resultats: {len(resultats)}")
    return {
        "total": len(resultats),
        "profil": profil.dict(),
        "recommandations": resultats
    }

# Semaine 3
@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...), location: str = "Morocco"):
    print(f"CV recu: {file.filename}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        texte_extrait = extract_profile_from_cv(tmp_path)
        print(f"Texte extrait ({len(texte_extrait)} caracteres)")

        if not texte_extrait or len(texte_extrait) < 10:
            query = "data scientist python machine learning"
            texte_extrait = query
        else:
            query = texte_extrait[:200]

        offres = fetch_jobs(query=query, location=location, num_pages=1)
        print(f"Offres recues: {len(offres)}")

        profil = {"competences": texte_extrait, "experience": "", "formation": ""}
        resultats = calculer_scores(profil, offres)

        return {
            "total": len(resultats),
            "texte_extrait": texte_extrait[:500],
            "recommandations": resultats
        }

    finally:
        os.unlink(tmp_path)