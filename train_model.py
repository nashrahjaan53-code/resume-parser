"""
Resume Parser Training & Job Matching
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.parser import ResumeParser, SkillTaxonomy, ResumeScorer, ResumeDatabase

def main():
    print("📄 Advanced Resume Parser Training")
    
    # Generate sample resumes
    print("\n📊 Generating sample resumes...")
    resume_db = ResumeDatabase.generate_sample_resumes(n=500)
    
    # Score resumes
    print("🎯 Scoring resumes...")
    scores = []
    for _, row in resume_db.iterrows():
        contact = {
            'name': row['name'],
            'email': row['email'],
            'phone': row['phone']
        }
        skills = row['skills'].split(', ')
        score = ResumeScorer.score_resume(contact, skills, row['experience_years'], row['education'].split(', '))
        scores.append(score)
    
    resume_db['resume_score'] = scores
    
    # Save
    resume_db.to_csv('data/resumes.csv', index=False)
    
    print(f"\n📊 Resume Database:")
    print(f"✓ Total Resumes: {len(resume_db)}")
    print(f"✓ Avg Score: {resume_db['resume_score'].mean():.1f}")
    print(f"✓ Top Score: {resume_db['resume_score'].max()}")
    print(f"✓ Min Score: {resume_db['resume_score'].min()}")
    
    print(f"\n👥 Top 5 Candidates:")
    top_5 = resume_db.nlargest(5, 'resume_score')[['name', 'experience_years', 'skills', 'resume_score']]
    print(top_5.to_string(index=False))
    
    print(f"\n✅ Resume parsing complete!")
    print("🚀 Start dashboard with: streamlit run dashboard/app.py")

if __name__ == '__main__':
    main()
