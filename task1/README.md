## Recruitment system

### Project introduction
A web-based recruitment system that connects job seekers and recruiters. Job seekers can search and apply for jobs with resume, while recruiters can post jobs and manage applicancations.

### Teatures:
For job seekers, after register and login, they can search jobs by keyword or company name, apply for jobs with resume, add personnal skills(function in task2) and view application status. For recruiters, after register and login, they can post jobs with required skills, view posted jobs, review applicants' resumes and update application status.

### Tech:
Python + Flask + SQLite

### How to Run:

Requirements: Python 3.8+
  
#### Steps:
-1. Clone or download the project 

-2.Run the application: python main.py

-3. Open browser and visit http://127.0.0.1:5000

### How to Use:
Job seeker register an account as seeker, after login they can search jobs and click "Apply", fill in resume and submit. And then they can check their application and result in "My Applications".
Recruiter register an account as recruiter, after login they can click "Post job" to create a job posting, after seeker apply, they can go to "My Posted Jobs" to view applicants with their resumes and apdate application status. 

### Match Score Algorithm:
The system uses Jaccard similarity to calculate match score:

Formula: matched_skills / required_skills

Score range: 0% (no match) to 100% (perfect match)

### Future Improvements
-Password encryption (bcrypt)

-PDF/Word resume upload

-TF-IDF matching algorithm

-Email notification system

### GitHub Repository
https://github.com/yugeaaaaaaaaa/COMP2090SEF-Group-Project/edit/main/task1

### Group member:

Peng Ziyu 14048424 (leader)(job.platform.py, job application.py, main.py)

XU Zhiheng 13961266(matching.py)

WONG Hiu Ching 14267324(task1.py)
