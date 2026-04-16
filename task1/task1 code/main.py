from flask import Flask,render_template_string, request, redirect, url_for, session
from jobplatform import JobPlatform
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
platform = JobPlatform()

@app.route('/')
def index():
    if 'user_id' in session:
        menu = f'''
        <h1>Recruitment system</h1>
        <p> welcome, {session['user_name']}({session['user_type']})</p>
        <a href = "/search"> Search job</a><br>
        '''

        if session['user_type'] == 'recruiter':
            menu += '<a href="/post">Post job</a><br>'
            menu += '<a href="/my_posted_jobs">My Posted Jobs</a><br>'
        else:
            menu +='<a href="/my_applications">My application</a><br>'

        menu += '<a href="/logout">Logout</a>'
        return menu
    
    else:
        return'''
        <h1>Recruitment system</h1>
        <a href = "/register">Register</a><br>
        <a href = "/login">Login</a>
        '''
    
@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        platform.register(name, email, password, user_type)
        return redirect(url_for('index'))
    
    return'''
    <form method = "post">
       name: <input name = "name" required><br>
       email:<input name = "email" required><br>
       password:<input name = "password" type = "password" required><br>
       type:<select name = "user_type">
           <option value = "seeker"> seeker</option>
           <option value = "recruiter"> recruiter</option>
        </select><br>
        <button type = "submit"> register</button>
    </form>
       '''

@app.route ('/login',methods = ['GET','POST'])
def login():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        user = platform.login(email,password)
        if user:
            session['user_id'] = user.user_id
            session['user_name'] = user.name
            session['user_type'] = user.user_type
            return redirect(url_for('index'))
        else:
            return "Email or password incorrect"
    return'''
    <form method = "post">
        email:<input name = "email" required><br>
        passwoed: <input name = "password" type = "password" required><br>
        <button type = "submit">Login</button>
    </form>
    '''

@app.route('/search')
def search():
    keyword = request.args.get('keyword','')
    jobs = platform.search_job(keyword)

    html = '<h1>search jobs</h1>'
    html += '<form method="get"><input name="keyword" placeholder="Enter keyword"><button>Search</button></form><hr>'
    if jobs:
        for job in jobs:
            html += f'''
            <div>
                <h3>{job.title}</h3>
                <p>Company:{job.company}</p>
                <a href="/apply/{job.job_id}">Apply</a>
            </div>
            <hr>
            '''
    else:
        html += '<p>No jobs found</p>'
    html += '<a href="/">Back to Home</a>'
    return html

@app.route('/post',methods = ['GET','POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        company = request.form['company']
        platform.post_job(title,description,company)
        return redirect(url_for('index'))
    
    return '''
    <form method = "post">
        Job title:<input name = "title" required><br>
        Description:<textarea name = "description" required></textarea><br>
        Company:<input name = "company" required><br>
        <button type = "submit">Post</button>
        <a href="/" style="margin-left: 20px;">Back to Home</a>
    </form>
    '''


@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    if 'user_id' not in session:
        return "Please login first. <a href='/login'>Login</a>"
    
    if session.get('user_type') != 'seeker':
        return "Only job seekers can apply for jobs. <a href='/'>Back</a>"
    
    job = platform.check_job_detail(job_id)
    if request.method == 'POST':
        resume_text = request.form.get('resume','') 
        application = platform.apply_job(job_id,resume_text)
       
        if application:
            return f"""
           <h2>Application submitted<h2>
           <p>You have successfully applied for: <strong>{job.title}</strong></p>
           <p>Application ID: {application.application_id}</p>
           <p>Status: {application.status}</p>
           <a href="/my_applications">View My Applications</a><br>
           <a href="/">Back to Home</a>"""
        else:
            return "Failed to submit application. <a href='/search'>Try again</a>"
    return f"""
    <h2>Apply for: {job.title}</h2>
    <p><strong>Company:</strong> {job.company}</p>
    <p><strong>Description:</strong> {getattr(job, 'description', 'N/A')}</p>
    
    <form method="post">
        <h3>Your Resume/Cover Letter:</h3>
        <textarea name="resume" rows="10" cols="60" placeholder="Write your resume or cover letter here...&#10;&#10;Example:&#10;Education: ...&#10;Work Experience: ...&#10;Skills: ..."></textarea><br><br>
        <button type="submit">Submit Application</button>
    </form>
    
"""

@app.route('/my_posted_jobs')
def my_posted_jobs():
    my_jobs = platform.get_my_posted_jobs()
    html = '<h1>My Posted Jobs</h1><hr>'
    if my_jobs:
        for job in my_jobs:
            applicants = platform.view_applicants(job.job_id)

            html+= f'''
            <h2>{job.title}</h2>
            <p><strong>Company:</strong> {job.company}</p>
            <p><strong>Posted on:</strong> {getattr(job, 'posted_date', 'N/A')}</p>
            <p><strong>Description:</strong> {getattr(job, 'description', 'N/A')}</p>
            <p><strong>Total Applicants:</strong> {len(applicants)}</p>
            '''
    
            if applicants:
                html += '<h3>Applicants:</h3>'
                for app_info in applicants:
                    applicant = app_info['applicant']
                    application = app_info['application']

                    html+= f'''
                    <p><strong>Name:</strong> {applicant.name}</p>
                    <p><strong>Email:</strong> {applicant.email}</p>
                    <p><strong>Status:</strong> 
                    <span style="padding:2px 6px; border-radius:3px; background:#e0e0e0;">
                                    {application.status}</span></p>
                    <p><strong>Applied on:</strong> {application.application_date}</p>
                    <details>
                        <summary><strong>View Resume/CV</strong></summary>
                        <div style="background:#f5f5f5; padding:10px; margin-top:10px; border-left:3px solid #4CAF50;">
                            <pre style="white-space:pre-wrap;">{application.resume if application.resume else 'No resume provided'}</pre>
                        </div>
                    </details>
                        
                    <form method="post" action="/update_status/{application.application_id}" style="margin-top:10px;">
                        <label>Update Status:</label>
                        <select name="new_status">
                            <option value="received" {'selected' if application.status == 'received' else ''}>Received</option>
                            <option value="reviewed" {'selected' if application.status == 'reviewed' else ''}>Reviewed</option>
                            <option value="interview" {'selected' if application.status == 'interview' else ''}>Interview</option>
                            <option value="accepted" {'selected' if application.status == 'accepted' else ''}>Accepted</option>
                            <option value="rejected" {'selected' if application.status == 'rejected' else ''}>Rejected</option>
                        </select>
                        <button type="submit">Update</button>
                    </form>
                </div>
                '''
            else:
                html += '<p>No applicants yet.</p>'
            html += '</div><hr>'
        html += '<br><a href="/">← Back to Home</a>'
    else:
        html += '<p>You haven\'t posted any jobs yet. <a href="/post">Post a job</a></p>'    
        html += '<br><a href="/">← Back to Home</a>'
    return html


@app.route('/update_status/<int:application_id>', methods=['POST'])
def update_status(application_id):
    new_status = request.form.get('new_status')
    if platform.update_application_status(application_id, new_status):
        return f"Status updated to '{new_status}'! <a href='/my_posted_jobs'>Back to my jobs</a>"  
    return "Application not found."

@app.route('/my_applications')
def my_applications():
    apps = platform.get_my_applications()
    html = '<h1>My Application</h1><hr>'

    if apps:
        for app in apps:
            html += f'''
            <div>
                <p>Job:{app.job.title}</p>
                <p>Company:{app.job.company}</p>
                <p>Status:{app.status}</p>
            </div>
            <hr>
            '''
    else:
        html += '<p>No applications found</p>'
    html += '<a href = "/">Back to home</a>'
    return html

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)