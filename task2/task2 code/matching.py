    #The purpose of this section is to calculate and distinguish the degree of matching between occupations and competencies.
from TFIDF import match_score_tfidf

def match_score(seeker,job, all_jobs = None):
    if not job.skills:
        return 0.0
    
    if all_jobs and len(all_jobs) > 0:
        return match_score_tfidf(seeker, job, all_jobs)
    
    seeker_skills = set(seeker.skills)
    job_skills = set(job.skills)
    matched = seeker_skills & job_skills
    return len(matched)/len(job_skills) if job_skills else 0.0

