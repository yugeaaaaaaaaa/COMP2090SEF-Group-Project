from user_job_model import User, Job
from matching import match_score  
from jobapplication import JobApplication
from datetime import datetime
from database import RecruitmentDatabase

class JobPlatform:
    def __init__(self):
        self.db = RecruitmentDatabase()
        self.users = []
        self.jobs = []
        self.applications =[]
        self.current_user = None
        self.next_user_id = 1
        self.next_job_id = 1
        self.next_application_id = 1
        self.load_data_from_db()

    def load_data_from_db(self):
        conn = self.db._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, name, email, password, user_type, skills FROM users')

        users_data = cursor.fetchall()
        for u in users_data:
            user = User(
                user_id=u[0],
                name=u[1],
                email=u[2],
                password=u[3],
                user_type=u[4]
            )
            skills_str = u[5] if len(u) > 5 and u[5] else ''
            user.skills = skills_str.split(',') if skills_str else []
            user.applied_jobs = []
            self.users.append(user)
            if u[0] >= self.next_user_id:
                self.next_user_id = u[0] + 1

        cursor.execute('SELECT job_id, title, company, description, post_time, posted_by FROM jobs')
        jobs_data = cursor.fetchall()
        for j in jobs_data:
            job = Job(
                job_id=j[0],
                title=j[1],
                company=j[2],
                description=j[3]
            )
            job.post_time = j[4]
            job.posted_by = j[5]
            cursor.execute('''
            SELECT s.name FROM job_skills js
            JOIN skills s ON js.skill_id = s.skill_id
            WHERE js.job_id = ?''', (j[0],))
            skill_rows = cursor.fetchall()
            job.skills = [row[0] for row in skill_rows]
            self.jobs.append(job)
            if j[0] >= self.next_job_id:
                self.next_job_id = j[0] + 1

        cursor.execute('SELECT application_id, job_id, applicant_id, resume, status, application_date FROM applications')
        apps_data = cursor.fetchall()
        for a in apps_data:
            job = next((j for j in self.jobs if j.job_id == a[1]), None)
            applicant = next((u for u in self.users if u.user_id == a[2]), None)
            if job and applicant:
                application = JobApplication(a[0], job, a[3], applicant)
                application.status = a[4]
                application.application_date = a[5]
                self.applications.append(application)
                if a[0] >= self.next_application_id:
                    self.next_application_id = a[0] + 1

        conn.close()
        print(f"Loaded {len(self.users)} users, {len(self.jobs)} jobs, {len(self.applications)} applications from database")

    def register(self, name, email, password, user_type):
        for user in self.users:
            if user.email == email:
                print ("This email is registered.")
                return False
            
        existing = self.db.get_user_by_email(email)
        if existing:
            print("This email is registered in database.")
            return False
            
        new_user = User(
            user_id = self.next_user_id,
            name = name,
            email = email,
            password=password,
            user_type=user_type,
        )

        new_user.skills = []
        new_user.applied_jobs = []

        db_user_id = self.db.add_user(new_user)
        if db_user_id == -1:
            print("Email already exists in database")
            return False

        self.users.append(new_user)
        self.next_user_id += 1
        print(f"{name} register successfully!")
        return True

    def login(self, email, password):
        for user in self.users:
            if user.email == email and user.password == password:
                self.current_user = user
                print(f"{user.name} login successfully!")
                return user
            
        db_user = self.db.get_user_by_email(email)
        if db_user and db_user['password'] == password:
            user = User(
                user_id=db_user['user_id'],
                name=db_user['name'],
                email=db_user['email'],
                password=db_user['password'],
                user_type=db_user['user_type']
            )
            skills_str = db_user.get('skills', '')
            user.skills = skills_str.split(',') if skills_str else []
            user.applied_jobs = []
            self.users.append(user)
            self.current_user = user
            print(f"{user.name} login successfully!")
            return user

        print("password or email is incorrect.")
        return None
        
    def logout(self):
        self.current_user = None
        print("logout successful.")
    
    def search_job(self, keyword):
        result = []
        for job in self.jobs:
            if hasattr(job, 'title') and hasattr(job, 'company'):
                if keyword.lower() in job.title.lower() or keyword.lower() in job.company.lower():
                    result.append(job)
        return result
        
    def check_job_detail(self, job_id):
        for job in self.jobs:
            if job.job_id == job_id:
                return job
        return None
        
    def apply_job(self, job_id, resume_text):
        if not self.current_user:
            print("please login.")
            return None
        
        if self.current_user.user_type != "seeker":
            print("Only job seekers can apply for jobs!")
            return None
        
        job = self.check_job_detail(job_id)
        if not job:
            print("Job not found!")
            return None
        
        for app in self.applications:
            if app.applicant.user_id == self.current_user.user_id and app.job.job_id == job_id:
                print("You have already applied for this job!")
                return None
            
        if resume_text:
            resume = resume_text
        else:
            resume = self.current_user.resume if hasattr(self.current_user, 'resume') else ""

        application = JobApplication(
            self.next_application_id,
            job,
            resume,
            self.current_user,
        )
        application.application_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.add_application(
        job_id,
        self.current_user.user_id,
        resume,
        application.status,
        application.application_date)
        self.applications.append(application)
        self.next_application_id +=1
        print(f"Submitted successfully. ID{application.application_id}")
        return application
    
    def get_my_applications(self):
        if not self.current_user:
            print("Please login first.")
            return []
    
        my_apps = []
        for app in self.applications:
            if app.applicant.user_id == self.current_user.user_id:
                my_apps.append(app)

        all_jobs = self.jobs
        for app in my_apps:
            try:
                score = match_score(app.applicant, app.job, all_jobs)
                app.match_score = score
                print(f"Match score for {app.job.title}: {score * 100:.1f}%")
            except Exception as e:
                print(f"Error calculating match score: {e}")
                app.match_score = 0.0
        return my_apps
    
    def update_resume(self, resume_text, education="", experience=""):
        if not self.current_user:
            print("Please login first.")
            return False
        
        self.current_user.resume = resume_text
        self.current_user.education = education
        self.current_user.experience = experience
        print("Resume updated successfully!")
        return True
    
    def get_resume(self, user_id):
        if not self.current_user:
            print("Please login first.")
            return None
        
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None
    
    def view_applicants(self,job_id):
        if not self.current_user:
            print("Please login first.")
            return []
        
        all_jobs = self.jobs
        applicants_information =[]
        for application in self.applications:
            if application.job.job_id == job_id:
                try:
                    score = match_score(application.applicant, application.job, all_jobs)
                    match_percent = int(score * 100)
                except Exception as e:
                    print (f"Error calculating match score: {e}")
                    match_percent = 0

                applicants_information.append({
                    'application': application,
                    'applicant': application.applicant,
                    'resume': application.resume,
                    'status': application.status,
                    'application_date': application.application_date,
                    'match_percent': match_percent 
                })
        return applicants_information
            
#---------------------------------------------------------
    def post_job(self, title,description,company,skills_text=""):
        if not self.current_user:
            print("pleace login.")
            return None
        
        new_job = Job(
            job_id = self.next_job_id,
            title = title,
            company=company,
            description=description, 
        )
        if skills_text:
            skills_list = [s.strip() for s in skills_text.split(',') if s.strip()]
            new_job.skills = skills_list

        new_job.posted_by = self.current_user.user_id
        new_job.posted_date = datetime.now().strftime("%Y-%m-%d")

        _ = self.db.add_job(new_job, self.current_user.user_id)

        self.jobs.append(new_job)
        self.next_job_id +=1
        print("Post job successfully.")
        return True
    
    def get_my_posted_jobs(self):
        if not self.current_user:
            return []
        if self.current_user.user_type != "recruiter":
            return []    
        return [job for job in self.jobs if hasattr(job, 'posted_by') and job.posted_by == self.current_user.user_id]
    
    def update_application_status(self, application_id, new_status):
        for app in self.applications:
            if app.application_id == application_id:
                app.update_status(new_status)
                self.db.update_application_status(application_id, new_status)
                return True
        return False   
    
    def update_user_skills(self, skills_list):
        if not self.current_user:
            return False
        self.current_user.skills = skills_list
        skills_str = ','.join(skills_list)
        conn = self.db._get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET skills = ? WHERE user_id = ?', (skills_str, self.current_user.user_id))
        conn.commit()
        conn.close()
        return True
