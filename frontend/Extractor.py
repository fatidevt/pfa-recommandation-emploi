import re
from pypdf import PdfReader


# ─────────────────────────────────────────────
# 1. EXTRACT RAW TEXT FROM PDF
# ─────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract raw text from a PDF file (CV).

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        str: Raw extracted text from all pages
    """
    reader = PdfReader(pdf_path)
    raw_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            raw_text += text + "\n"

    return raw_text


# ─────────────────────────────────────────────
# 2. CLEAN EXTRACTED TEXT
# ─────────────────────────────────────────────

def clean_text(text: str) -> str:
    """
    Clean extracted CV text for TF-IDF processing.

    Args:
        text (str): Raw text from PDF

    Returns:
        str: Cleaned text
    """
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)

    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)

    # Remove phone numbers
    text = re.sub(r'[\+\(]?[1-9][0-9\s\.\-\(\)]{8,}[0-9]', '', text)

    # Remove special characters but keep letters, numbers, spaces
    text = re.sub(r'[^\w\s]', ' ', text)

    # Remove numbers alone (like dates: 2020, 2021)
    text = re.sub(r'\b\d{1,4}\b', '', text)

    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text).strip()

    # Lowercase
    text = text.lower()

    return text


# ─────────────────────────────────────────────
# 3. MAIN FUNCTION — EXTRACT + CLEAN
# ─────────────────────────────────────────────

def extract_profile_from_cv(pdf_path: str) -> dict:
    """
    Full pipeline: extract text from CV PDF and clean it
    for use as TF-IDF user profile.

    Args:
        pdf_path (str): Path to the PDF CV file

    Returns:
        dict: {
            "raw_text": original extracted text (for preview),
            "clean_text": cleaned text (for TF-IDF),
            "num_pages": number of pages,
            "word_count": number of words in clean text
        }
    """
    # Step 1 - Extract
    raw_text = extract_text_from_pdf(pdf_path)

    if not raw_text.strip():
        raise ValueError("Le PDF ne contient pas de texte extractible. Essayez un CV en format texte.")

    # Step 2 - Clean
    clean = clean_text(raw_text)

    return {
        "raw_text": raw_text[:2000],   # preview first 2000 chars
        "clean_text": clean,
        "num_pages": len(PdfReader(pdf_path).pages),
        "word_count": len(clean.split())
    }


# ─────────────────────────────────────────────
# 4. TEST WITH FAKE PDF DATA
# ─────────────────────────────────────────────

def test_with_fake_text():
    """
    Test the cleaning function with fake CV text
    (no real PDF needed).
    """
    print("\n" + "="*55)
    print("🧪 TEST — Fake CV Text Cleaning")
    print("="*55)

    fake_cv_text = """
    John Doe
    john.doe@email.com | +212 6 12 34 56 78
    https://linkedin.com/in/johndoe

    COMPÉTENCES TECHNIQUES
    Python, Django, REST API, PostgreSQL, SQL
    Machine Learning, Scikit-learn, Pandas, NumPy
    Git, Docker, Linux

    EXPÉRIENCE
    2021 - 2023: Développeur Backend @ TechCorp Casablanca
    Développement d'APIs REST avec Python Django.
    Gestion de bases de données PostgreSQL.

    2020 - 2021: Stage Développeur @ StartupMaroc
    Développement web avec Flask et MySQL.

    FORMATION
    2018 - 2020: Master Informatique — Université Mohammed V, Rabat
    2015 - 2018: Licence Informatique — ENSA Casablanca
    """

    cleaned = clean_text(fake_cv_text)

    print(f"\n📄 Raw text (first 200 chars):\n{fake_cv_text[:200]}...")
    print(f"\n✅ Cleaned text:\n{cleaned}")
    print(f"\n📊 Word count: {len(cleaned.split())} words")

    # Checks
    assert "john.doe@email.com" not in cleaned, "❌ Email not removed!"
    assert "http" not in cleaned, "❌ URL not removed!"
    assert "+212" not in cleaned, "❌ Phone not removed!"
    assert cleaned == cleaned.lower(), "❌ Text not lowercased!"

    print("\n✅ All checks passed — cleaner works correctly!\n")
    return cleaned


if __name__ == "__main__":
    # Test 1: cleaning with fake text
    test_with_fake_text()

    # Test 2: real PDF (uncomment and provide a real CV path)
    # result = extract_profile_from_cv("cv.pdf")
    # print(f"Pages: {result['num_pages']}")
    # print(f"Words: {result['word_count']}")
    # print(f"Preview:\n{result['raw_text'][:500]}")
    # print(f"Clean:\n{result['clean_text'][:500]}")