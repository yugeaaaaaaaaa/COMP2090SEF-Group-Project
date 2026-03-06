class JobApplication:
    def __init__(self, application_id, job, resume, applicant ):
        self.application_id = application_id
        self.job = job
        self.applicant = applicant
        self.resume = resume
        self.application_date = None
        self.status = "received"

    def update_status(self, new_status):
        self.status = new_status
        print(f"your application is {new_status}.")

    def get_information(self):
        information = f""" application_id:{self.application_id}
        job:{self.job}
        applicant:{self.applicant}
        status:{self.status}
        """
        return information
    
    def __str__(self):
        return f"applicant {self.application_id} is {self.status} "