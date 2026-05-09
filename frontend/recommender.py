from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend(profil: str, offres: list, top_n: int = 10):
    """
    Compare le profil utilisateur avec les offres
    et retourne le Top-10 trié par score.
    
    Args:
        profil: texte complet du profil utilisateur
        offres: liste d'offres de JSearch
        top_n: nombre d'offres à retourner
    
    Returns:
        liste d'offres triées par score décroissant
    """

    # Étape 1 - Extraire le texte de chaque offre
    textes_offres = []
    for offre in offres:
        # Boost job title (most relevant part) + limit description length
        titre = f"{offre.get('job_title', '')} " * 5
        description = offre.get('job_description', '')[:500]
        employeur = offre.get('employer_name', '')
        texte = f"{titre} {description} {employeur}".lower()
        textes_offres.append(texte)

    # Étape 2 - Si pas d'offres retourner liste vide
    if not textes_offres:
        return []

    # Étape 3 - Booster le profil pour équilibrer avec les longues descriptions
    profil_boosted = (profil + " ") * 10

    # Étape 4 - Préparer tous les textes ensemble
    tous_textes = [profil_boosted] + textes_offres

    # Étape 5 - Appliquer TF-IDF avec paramètres optimisés
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),   # capture "machine learning", "data science", etc.
        max_features=5000,
        sublinear_tf=True,    # atténue l'effet des textes très longs
        min_df=1
    )
    tfidf_matrix = vectorizer.fit_transform(tous_textes)

    # Étape 6 - Calculer similarité cosinus
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Étape 7 - Ajouter le score à chaque offre (mis à l'échelle pour affichage)
    for i, offre in enumerate(offres):
        raw = float(scores[i])
        # Scale: cosine range (0.0–0.33) → percentage (0–100%)
        scaled = round(min(raw * 300, 100), 2)
        offre["matching_score"] = scaled

    # Étape 8 - Trier par score décroissant et retourner Top-N
    offres_triees = sorted(offres, key=lambda x: x["matching_score"], reverse=True)

    return offres_triees[:top_n]