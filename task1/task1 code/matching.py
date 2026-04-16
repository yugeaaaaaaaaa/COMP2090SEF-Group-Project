    #The purpose of this section is to calculate and distinguish the degree of matching between occupations and competencies.
def match_score(seeker,job):
    if not job.requirement_skills:
        return 0.0
    seeker_skills = set(seeker.skills)
    job_skills = set(job.requirement_skills)
    matched = seeker_skills & job_skills
    return len(matched)/len(job_skills)
