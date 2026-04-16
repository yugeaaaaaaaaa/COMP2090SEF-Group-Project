import math

def computeTF(words):
    if not words:
        return {}
    total = len(words)
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    for word in freq:
        freq[word] = freq[word] / total
    return freq

def computeIDF(jobList):
    if not jobList:
        return {}
    
    totalJobs = len(jobList)
    docCount = {}
    
    for job in jobList:
        if hasattr(job, 'skills') and job.skills:
            unique_skills = set(job.skills)
            for skill in unique_skills:
                docCount[skill] = docCount.get(skill, 0) + 1
    
    # 计算IDF
    idf = {}
    for skill, count in docCount.items():
        idf[skill] = math.log(totalJobs / (count + 1)) + 1
    
    return idf

def match_score_tfidf(seeker, job, all_jobs):
    if not hasattr(job, 'skills') or not job.skills:
        return 0.0
    
    if not hasattr(seeker, 'skills') or not seeker.skills:
        return 0.0
    
    if not all_jobs:
        all_jobs = [job]
    
    idf_all = computeIDF(all_jobs)
    
    tf = computeTF(job.skills)
    
    total_score = 0.0
    max_possible_score = 0.0
    
    for skill in job.skills:
        tf_value = tf.get(skill, 0)
        idf_value = idf_all.get(skill, 0)
        
        max_possible_score += tf_value * idf_value
        
        if skill in seeker.skills:
            total_score += tf_value * idf_value
    
    if max_possible_score > 0:
        return min(total_score / max_possible_score, 1.0)
    
    return 0.0