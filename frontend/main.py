from fastapi import FastAPI
from dotenv import load_dotenv
from jsearch import fetch_jobs

load_dotenv(dotenv_path="../.env")

app = FastAPI()

@app.get("/offres")
def get_offres(competences: str, location: str = "Morocco"):
    
    jobs = fetch_jobs(
        query=competences,
        location=location,
        num_pages=1
    )
    
    return {"total": len(jobs), "offres": jobs}