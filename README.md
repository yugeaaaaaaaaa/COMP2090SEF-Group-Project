# Recruitment System - COMP 2090SEF group project
**A Flask-based recruitment system with TF-IDF job matching**

### Group members: 
Peng Ziyu 14048424 (leader)

XU Zhiheng 13961266

WONG Hiu Ching 14267324

### Contents of this project:
task1: OOP-based application development(recruitment-system)

task2: Study report on TF-IDF algorithm for job matching

### Project Overview
This project is a web-based recruitment system developed for COMP 2090SEF. It connects job seekers and recruiters, allowing:

- **Job seekers** to search and apply for jobs
- **Recruiters** to post jobs and manage applications

The system uses **TF-IDF (Term Frequency-Inverse Document Frequency)** to calculate match scores between job seekers and job postings.

### Features:
For job seekers, after register and login, they can search jobs by keyword or company name, apply for jobs with resume, add personal skills (function in task2) and view application status. For recruiters, after register and login, they can post jobs with required skills, view posted jobs, review applicants' resumes and update application status.

### How to Run:
Requirements: Python 3.8+

#### Steps:
-1. Clone or download the project

-2.Run the application: python main.py

-3. Open browser and visit http://127.0.0.1:5000

### TF-IDF Algorithm：
TF-IDF (Term Frequency-Inverse Document Frequency) calculates match scores between job seekers and job postings.

#### Term	Formula
- TF = count(skill) / total_skills
- IDF =	log(total_jobs / jobs_with_skill) + 1
- Score =	Σ(TF × IDF)
  
Rare skills get higher weight than common skills.

### Future Improvements
- Password encryption (bcrypt)
- PDF/Word resume upload
- Email notification system
- Job recommendation based on match score
- Pagination for job lists
- Admin dashboard

### GitHub Repository：
https://github.com/yugeaaaaaaaaa/COMP2090SEF-Group-Project

### Introduction video:
