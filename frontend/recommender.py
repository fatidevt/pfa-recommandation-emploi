from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend(profil: str, offres: list, top_n: int = 10):
    """
    Compare le profil utilisateur avec les offres
    et retourne le Top-10 trié par score.
    
    Args:
        profil: compétences de l'utilisateur ex: "python django fastapi"
        offres: liste d'offres de JSearch
        top_n: nombre d'offres à retourner
    
    Returns:
        liste d'offres triées par score décroissant
    """
    
    # Étape 1 - Extraire le texte de chaque offre
    textes_offres = []
    for offre in offres:
        texte = f"{offre.get('job_title', '')} {offre.get('job_description', '')}"
        textes_offres.append(texte)
    
    # Étape 2 - Si pas d'offres retourner liste vide
    if not textes_offres:
        return []
    
    # Étape 3 - Préparer tous les textes ensemble
    tous_textes = [profil] + textes_offres
    
    # Étape 4 - Appliquer TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(tous_textes)
    
    # Étape 5 - Calculer similarité cosinus
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # Étape 6 - Ajouter le score à chaque offre
    for i, offre in enumerate(offres):
        offre["matching_score"] = round(float(scores[i]) * 100, 2)
    
    # Étape 7 - Trier par score décroissant et retourner Top-10
    offres_triees = sorted(offres, key=lambda x: x["matching_score"], reverse=True)
    
    return offres_triees[:top_n]