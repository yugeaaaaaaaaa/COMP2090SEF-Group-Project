from task1 import User, Job
from matching import match_score  
from jobapplication import JobApplication
from datetime import datetime

class JobPlatform:
    def __init__(self):
        self.users = []
        self.jobs = []
        self.applications =[]
        self.current_user = None
        self.next_user_id = 1
        self.next_job_id = 1
        self.next_application_id = 1

    def register(self, name, email, password, user_type):
        for user in self.users:
            if user.email == email:
                print ("This email is registered.")
                return False
            
        new_user = User(
            user_id = self.next_user_id,
            name = name,
            email = email,
            password=password,
            user_type=user_type,
            skills = []
        )

        new_user.resume = ""
        new_user.education = ""
        new_user.experience = ""
        new_user.email = email
        new_user.password = password
        new_user.user_type = user_type
        self.users.append(new_user)
        self.next_user_id += 1
        print(f"{name} register successfully!")

    def login(self, email, password):
        for user in self.users:
            if user.email == email and user.password == password:
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
        for app in my_apps:
            score = match_score(app.applicant, app.job)
            print(f"Match score: {score * 100:.1f}%")
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
        
        applicants_information =[]
        for application in self.applications:
            if application.job.job_id == job_id:
                applicants_information.append({
                    'application': application,
                    'applicant': application.applicant,
                    'resume': application.resume,
                    'status': application.status,
                    'application_date': application.application_date
                })
        return applicants_information
            
#---------------------------------------------------------
    def post_job(self, title, description, company):
        if not self.current_user:
            print("pleace login.")
            return None
        
        if self.current_user.user_type !="recruiter":
            print("Only recruiters can post job!")
            return None
        
        new_job = Job(
            job_id = self.next_job_id,
            title = title,
            department="", 
        )
        new_job.company = company
        new_job.description = description
        new_job.posted_by = self.current_user.user_id
        new_job.posted_date = datetime.now().strftime("%Y-%m-%d")

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
        

