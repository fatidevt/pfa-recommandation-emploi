from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv
from jsearch import fetch_jobs
from recommender import calculer_scores
from Extractor import extract_profile_from_cv
import tempfile
import pandas as pd
import os

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

app = FastAPI()

class Profil(BaseModel):
    competences: str
    experience: str = ""
    formation: str = ""
    location: str = "Morocco"

def extraire_mots_cles(texte: str) -> str:
    texte_lower = texte.lower()
    if any(mot in texte_lower for mot in ["cisco", "vlan", "routeur", "switch", "dhcp", "dns"]):
        return "technicien reseaux Maroc"
    elif any(mot in texte_lower for mot in ["windows server", "active directory", "vmware"]):
        return "administrateur systemes Maroc"
    elif any(mot in texte_lower for mot in ["python", "django", "react", "javascript"]):
        return "developpeur python Maroc"
    elif any(mot in texte_lower for mot in ["linux", "infrastructure", "devops"]):
        return "ingenieur infrastructure Maroc"
    else:
        return "technicien informatique Maroc"

def fetch_jobs_safe(query: str, location: str, num_pages: int) -> list:
    try:
        jobs = fetch_jobs(query=query, location=location, num_pages=num_pages)
        if not jobs:
            raise ValueError("Aucune offre retournée")
        return jobs
    except Exception:
        csv_path = Path(__file__).parent / "offres_backup.csv"
        if not csv_path.exists():
            raise HTTPException(503, "JSearch indisponible et aucun fichier backup trouvé")
        df = pd.read_csv(csv_path, encoding="utf-8")
        offres = []
        for _, row in df.iterrows():
            offres.append({
                "job_title": row.get("titre", ""),
                "job_description": row.get("description", ""),
                "employer_name": row.get("entreprise", ""),
                "job_apply_link": row.get("lien", "#"),
                "job_location": row.get("lieu", ""),
                "job_city": row.get("lieu", ""),
                "job_employment_type": "N/A"
            })
        return offres

@app.post("/recommandations")
def get_recommandations(profil: Profil):
    try:
        profil_complet = f"{profil.competences} {profil.experience} {profil.formation}"
        jobs = fetch_jobs_safe(query=profil.competences, location=profil.location, num_pages=2)
        profil_dict = {"competences": profil_complet, "experience": "", "formation": ""}
        top10 = calculer_scores(profil=profil_dict, offres=jobs)
        return {"total": len(top10), "recommandations": top10}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Erreur serveur : {str(e)}")

@app.post("/upload-cv")
async def upload_cv(fichier: UploadFile = File(...), location: str = "Morocco"):
    if not fichier.filename.endswith(".pdf"):
        raise HTTPException(400, "Seuls les fichiers PDF sont acceptés")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await fichier.read())
        tmp_path = tmp.name
    try:
        texte = extract_profile_from_cv(tmp_path)
        if not texte or len(texte.strip()) < 50:
            raise HTTPException(422, "Impossible d'extraire le texte du PDF")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Erreur extraction PDF : {str(e)}")
    finally:
        os.unlink(tmp_path)
    try:
        query = extraire_mots_cles(texte)
        print(f"Query extraite: {query}")
        jobs = fetch_jobs_safe(query=query, location=location, num_pages=2)
        profil_dict = {"competences": texte, "experience": "", "formation": ""}
        top10 = calculer_scores(profil=profil_dict, offres=jobs)
        return {
            "cv_apercu": texte[:2000],
            "num_pages": 1,
            "word_count": len(texte.split()),
            "total": len(top10),
            "recommandations": top10
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Erreur recommandation : {str(e)}")