class Job:
    def __init__(self, job_id, title, department):
        self.job_id = job_id
        self.title = title
        self.department = department
        self.company = ""
        self.description = ""

    def show_info(self):
        print(f"Title: {self.title} | Department: {self.department}")
        print(f"Required skills: {','.join(self.requirement_skills)}\n")

class User:
    def __init__(self, user_id, name, skills,email,password,user_type):
        self.user_id = user_id
        self.name = name
        self.skills = skills
        self.email = email
        self.password = password
        self.user_type = user_type
        self.applied_jobs = []

    def show_info(self):
        print(f"Name: {self.name} | ID: {self.user_id}")
        print(f"Skills: {','.join(self.skills)}\n")

    def apply_job(self, Job):
        self.applied_jobs.append(Job)
        print(f"{self.name} applied: {Job.title}")

if __name__ == "__main__":
    job1 = Job(101, "engineer", "technology department", ["Python","MySQL"])
    job2 = Job(102, "Product manager", "Marketing Department", ["Marketing strategy", "Communication skill"])

    user1 = User(1, "John", ["Python","MySQL"])
    user2 = User(2, "Amy", ["Marketing strategy", "Communication skill"])

    job1.show_info()
    job2.show_info()
    user1.show_info()
    user2.show_info()

    user1.apply_job(job1)
    user2.apply_job(job2)


