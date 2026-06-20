# Morocco Job Finder — Systeme de Recommandation Emploi

## Equipe
- Fati : Algorithme TF-IDF + Extraction PDF
- Najib : API FastAPI + Endpoints  
- Nouha : Interface Streamlit

## Installation

\\ash
git clone <url-repo>
cd pfa-recommandation-emploi/frontend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
\
## Configurer .env
\JSEARCH_API_KEY=votre_cle
\
## Lancement

\\ash
# Terminal 1
uvicorn main:app --reload

# Terminal 2
streamlit run app.py
\
## Endpoints API

| Endpoint | Methode | Description |
|----------|---------|-------------|
| /recommandations | POST | Recommandations par competences |
| /upload-cv | POST | Recommandations depuis CV PDF |

## Structure
\frontend/
├── main.py          # API FastAPI
├── app.py           # Interface Streamlit
├── recommender.py   # Algorithme TF-IDF
├── Extractor.py     # Extraction PDF
├── jsearch.py       # API JSearch
├── offres_backup.csv
└── requirements.txt
\
## Etablissement
SUP MTI Rabat — Master 1 ISI — 2025-2026
