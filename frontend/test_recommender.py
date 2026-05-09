from recommender import recommend

# Fake jobs
fake_jobs = [
    {
        "job_title": "Python Developer",
        "job_description": "We need a Python developer with Django, REST API, PostgreSQL and experience in backend development.",
        "employer_name": "TechCorp",
        "job_employment_type": "FULLTIME",
        "job_city": "Casablanca",
    },
    {
        "job_title": "Data Scientist",
        "job_description": "Looking for a data scientist with Python, pandas, scikit-learn, machine learning and TensorFlow.",
        "employer_name": "DataLab",
        "job_employment_type": "FULLTIME",
        "job_city": "Rabat",
    },
    {
        "job_title": "Graphic Designer",
        "job_description": "Create visual content using Photoshop, Illustrator and Figma for marketing campaigns.",
        "employer_name": "CreativeStudio",
        "job_employment_type": "PARTTIME",
        "job_city": "Marrakech",
    },
]

profile = "python django REST API backend developer"
results = recommend(profile, fake_jobs, top_n=3)

print(f"\n{'Rank':<5} {'Score':<10} {'Job Title':<25} {'Company'}")
print("-" * 60)
for i, job in enumerate(results, 1):
    print(f"{i:<5} {job['matching_score']:<10} {job['job_title']:<25} {job['employer_name']}")