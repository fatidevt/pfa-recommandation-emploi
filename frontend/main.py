from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv
from jsearch import fetch_jobs
from recommender import recommend
from Extractor import extract_profile_from_cv
import tempfile
import pandas as pd
import os

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

app = FastAPI()

# ─────────────────────────────────────────────
# MODÈLES
# ─────────────────────────────────────────────

class Profil(BaseModel):
    competences: str
    experience: str = ""
    formation: str = ""
    location: str = "Morocco"

# ─────────────────────────────────────────────
# FALLBACK CSV — si quota JSearch dépassé
# ─────────────────────────────────────────────

def fetch_jobs_safe(query: str, location: str, num_pages: int) -> list:
    try:
        jobs = fetch_jobs(query=query, location=location, num_pages=num_pages)
        if not jobs:
            raise ValueError("Aucune offre retournée par JSearch")
        return jobs
    except Exception:
        csv_path = Path(__file__).parent / "offres_backup.csv"
        if not csv_path.exists():
            raise HTTPException(503, "JSearch indisponible et aucun fichier backup trouvé")
        df = pd.read_csv(csv_path)
        return df.to_dict(orient="records")

# ─────────────────────────────────────────────
# ENDPOINT 1 — Saisie manuelle
# ─────────────────────────────────────────────

@app.post("/recommandations")
def get_recommandations(profil: Profil):
    try:
        profil_complet = f"{profil.competences} {profil.experience} {profil.formation}"
        jobs = fetch_jobs_safe(query=profil.competences, location=profil.location, num_pages=2)
        top10 = recommend(profil=profil_complet, offres=jobs, top_n=10)
        return {"total": len(top10), "recommandations": top10}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Erreur serveur : {str(e)}")

# ─────────────────────────────────────────────
# ENDPOINT 2 — Upload CV PDF
# ─────────────────────────────────────────────

@app.post("/upload-cv")
async def upload_cv(fichier: UploadFile = File(...), location: str = "Morocco"):
    if not fichier.filename.endswith(".pdf"):
        raise HTTPException(400, "Seuls les fichiers PDF sont acceptés")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await fichier.read())
        tmp_path = tmp.name

    try:
        profil_cv = extract_profile_from_cv(tmp_path)
    except ValueError as e:
        raise HTTPException(422, str(e))
    except Exception as e:
        raise HTTPException(500, f"Erreur extraction PDF : {str(e)}")
    finally:
        os.unlink(tmp_path)

    try:
        jobs = fetch_jobs_safe(query=profil_cv["clean_text"][:200], location=location, num_pages=2)
        top10 = recommend(profil=profil_cv["clean_text"], offres=jobs, top_n=10)
        return {
            "cv_apercu": profil_cv["raw_text"],
            "num_pages": profil_cv["num_pages"],
            "word_count": profil_cv["word_count"],
            "total": len(top10),
            "recommandations": top10
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Erreur recommandation : {str(e)}")