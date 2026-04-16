from datetime import datetime

class Job:
    def __init__(self, job_id: int, title: str, company: str, description: str):
        self.job_id = job_id
        self.title = title
        self.company = company
        self.description = description  
        self.skills = []  # 
        self.post_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_required_skill(self, skill):
        #add the job required skill
        self.skills.append(skill)

    def get_full_text(self) -> str:
        #get full text of the job name + description + requried skill
        skill_text = " ".join([s.name for s in self.skills])
        return f"{self.title} {self.description} {skill_text}"

    def __repr__(self):
        return f"Job(id={self.job_id}, title={self.title})"

class User:
    def __init__(self, user_id: int, name: str, email: str, password:str, user_type: str = "seeker"):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.user_type = user_type  # seeker/recruiter
        self.resume = None  # link with the resume
        self.applied_jobs = []

    def set_resume(self, resume):
        self.resume = resume

    def __repr__(self):
        return f"User(id={self.user_id}, name={self.name}, type={self.user_type})"


class Skill:
    def __init__(self, skill_id: int, name: str, category: str = None):
        self.skill_id = skill_id
        self.name = name  
        self.category = category  

    def __repr__(self):
        return f"Skill(id={self.skill_id}, name={self.name})"

class Resume:
    def __init__(self, resume_id: int, user_id: int, content: str):
        self.resume_id = resume_id
        self.user_id = user_id  # link with user
        self.content = content  
        self.skills = []  
        self.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_skill(self, skill):
        self.skills.append(skill)

    def get_full_text(self) -> str:
        skill_text = " ".join([s.name for s in self.skills])
        return f"{self.content} {skill_text}"

    def __repr__(self):
        return f"Resume(id={self.resume_id}, user_id={self.user_id})"

