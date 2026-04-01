"""
Resume Parser Dashboard
"""
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parser import SkillTaxonomy, ResumeScorer

st.set_page_config(page_title="Resume Parser", page_icon="📄", layout="wide")

@st.cache_resource
def load_resumes():
    return pd.read_csv('data/resumes.csv')

resumes = load_resumes()

st.title("📄 Advanced Resume Parser & Ranking")

tab1, tab2, tab3 = st.tabs(["👥 Candidates", "🎯 Job Matching", "📊 Analytics"])

with tab1:
    st.header("Candidate Database")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Candidates", len(resumes))
    with col2:
        st.metric("Avg Score", f"{resumes['resume_score'].mean():.1f}")
    with col3:
        st.metric("High Quality (>70)", len(resumes[resumes['resume_score'] > 70]))
    
    st.markdown("---")
    st.subheader("🏆 Top Candidates")
    
    top_n = st.slider("Show top N candidates:", 5, 50, 10)
    top_candidates = resumes.nlargest(top_n, 'resume_score')
    
    st.dataframe(top_candidates[['name', 'experience_years', 'skills', 'resume_score']], use_container_width=True)

with tab2:
    st.header("Job Matching")
    
    # Job requirements input
    st.subheader("📋 Job Requirements")
    job_title = st.text_input("Job Title:", "Senior Python Developer")
    required_skills = st.multiselect(
        "Required Skills:",
        list(SkillTaxonomy.SKILLS.keys()),
        default=['Python', 'AWS', 'Docker']
    )
    years_required = st.slider("Min Years Experience:", 0, 20, 3)
    
    # Match candidates
    resumes['required_match'] = resumes.apply(
        lambda row: len(set(row['skills'].split(', ')) & set(required_skills)), axis=1
    )
    
    matched = resumes[
        (resumes['experience_years'] >= years_required) & 
        (resumes['required_match'] > 0)
    ].sort_values('resume_score', ascending=False)
    
    st.markdown("---")
    st.subheader(f"✨ Matching Candidates ({len(matched)})")
    
    if len(matched) > 0:
        st.dataframe(matched[['name', 'experience_years', 'required_match', 'resume_score']], use_container_width=True)
    else:
        st.warning("No matching candidates found")

with tab3:
    st.header("Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Score distribution
        fig = px.histogram(resumes, x='resume_score', nbins=20,
                          title='Resume Score Distribution',
                          color_discrete_sequence=['#1f77b4'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Experience vs Score
        fig = px.scatter(resumes, x='experience_years', y='resume_score',
                        title='Experience vs Resume Score',
                        color='resume_score',
                        color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
