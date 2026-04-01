"""
Resume Parser - NLP Entity Extraction
"""
import pandas as pd
import numpy as np
import re
from typing import Dict, List

class SkillTaxonomy:
    """Comprehensive skill taxonomy"""
    SKILLS = {
        'Python': ['python', 'py', 'pandas', 'numpy', 'django', 'flask'],
        'Java': ['java', 'spring', 'maven', 'junit'],
        'JavaScript': ['javascript', 'js', 'node.js', 'react', 'vue', 'angular'],
        'SQL': ['sql', 'mysql', 'postgresql', 'oracle', 'sqlserver'],
        'AWS': ['aws', 'ec2', 's3', 'lambda', 'rds'],
        'Azure': ['azure', 'cosmos', 'blob storage'],
        'Docker': ['docker', 'containers'],
        'Kubernetes': ['kubernetes', 'k8s'],
        'Machine Learning': ['ml', 'machine learning', 'sklearn', 'tensorflow', 'keras', 'pytorch'],
        'Data Science': ['data science', 'analytics', 'visualization'],
        'Git': ['git', 'github', 'gitlab', 'bitbucket'],
        'DevOps': ['devops', 'ci/cd', 'jenkins', 'gitlab ci'],
        'Linux': ['linux', 'unix', 'bash'],
        'Excel': ['excel', 'vba'],
        'Tableau': ['tableau', 'powerbi', 'looker']
    }
    
    @staticmethod
    def extract_skills(text: str) -> List[str]:
        """Extract skills from text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill, keywords in SkillTaxonomy.SKILLS.items():
            for keyword in keywords:
                if re.search(r'\b' + keyword + r'\b', text_lower):
                    if skill not in found_skills:
                        found_skills.append(skill)
                    break
        
        return found_skills

class ResumeParser:
    """Parse resume text and extract information"""
    
    @staticmethod
    def extract_contact(text: str) -> Dict:
        """Extract contact information"""
        contact = {}
        
        # Email
        email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text)
        contact['email'] = email_match.group(1) if email_match else None
        
        # Phone
        phone_match = re.search(r'(?:\+?1[-.\s]?)?(?:\(?(\d{3})\)?[-.\s]?)?(\d{3})[-.\s]?(\d{4})', text)
        contact['phone'] = phone_match.group(0) if phone_match else None
        
        # Name (usually first line)
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        contact['name'] = lines[0] if lines else None
        
        return contact
    
    @staticmethod
    def extract_experience_years(text: str) -> float:
        """Estimate years of experience"""
        # Look for year ranges
        year_patterns = re.findall(r'(20\d{2})\s*-\s*(20\d{2}|present)', text.lower())
        
        if year_patterns:
            total_years = 0
            for start, end in year_patterns:
                if 'present' in end.lower():
                    end = 2024
                else:
                    end = int(end)
                total_years += (int(end) - int(start))
            return total_years
        
        return 0.0
    
    @staticmethod
    def extract_education(text: str) -> List[str]:
        """Extract education details"""
        degrees = re.findall(r'\b(Bachelor|Master|Ph\.?D|MBA|Associate|Diploma|B\.?[A-Z]{1,2}|M\.?[A-Z]{1,2})\b', text, re.IGNORECASE)
        return list(set(degrees))

class ResumeScorer:
    """Score resumes based on multiple factors"""
    
    @staticmethod
    def score_resume(contact: Dict, skills: List[str], experience_years: float, 
                    education: List[str], job_requirements: List[str] = None) -> int:
        """Score resume 0-100"""
        score = 0
        
        # Contact info (20 points)
        if contact.get('email'):
            score += 10
        if contact.get('phone'):
            score += 10
        
        # Skills (30 points)
        score += min(30, len(skills) * 3)
        
        # Experience (20 points)
        score += min(20, experience_years * 2)
        
        # Education (20 points)
        if education:
            score += min(20, len(education) * 10)
        
        # Job match bonus (10 points)
        if job_requirements and skills:
            matches = set(skills) & set(job_requirements)
            if matches:
                score += min(10, len(matches) * 5)
        
        return min(100, score)

class ResumeDatabase:
    """Store and manage parsed resumes"""
    
    @staticmethod
    def generate_sample_resumes(n=100) -> pd.DataFrame:
        """Generate sample resumes"""
        np.random.seed(42)
        
        names = ['John Smith', 'Sarah Johnson', 'Mike Chen', 'Emma Davis', 'Alex Rodriguez']
        skills_list = list(SkillTaxonomy.SKILLS.keys())
        
        data = []
        for i in range(n):
            skills = list(np.random.choice(skills_list, size=np.random.randint(3, 10), replace=False))
            exp_years = np.random.uniform(0, 20)
            education = np.random.choice([['Bachelor'], ['Master'], ['Diploma', 'Bachelor']], p=[0.5, 0.3, 0.2])
            
            data.append({
                'candidate_id': f'CAND_{i:05d}',
                'name': f'{np.random.choice(names)}_{i}',
                'email': f'candidate{i}@email.com',
                'phone': f'+1-555-000-{i:04d}',
                'skills': ', '.join(skills),
                'experience_years': round(exp_years, 1),
                'education': ', '.join(education),
                'score': 0
            })
        
        return pd.DataFrame(data)
