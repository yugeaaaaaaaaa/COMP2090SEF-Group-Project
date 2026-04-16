import sqlite3
from user_job_model import User, Job, Resume, Skill
from datetime import datetime

class RecruitmentDatabase:
    def __init__(self, db_name="recruitment.db"):
        self.db_name = db_name
        self._init_db()  

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        # USER TABLE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL CHECK(user_type IN ('seeker', 'recruiter')),
                skills TEXT
            )
        ''')

        # JOB TABLE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                description TEXT NOT NULL,
                post_time TEXT NOT NULL,
                posted_by INTEGER NOT NULL
            )
        ''')

        # RESUME TABLE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumes (
                resume_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                create_time TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        # SKILL TABLE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT
            )
        ''')

        # RESUME_LINKAGE WITH SKILL TABLE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resume_skills (
                resume_id INTEGER NOT NULL,
                skill_id INTEGER NOT NULL,
                PRIMARY KEY (resume_id, skill_id),
                FOREIGN KEY (resume_id) REFERENCES resumes(resume_id),
                FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
            )
        ''')

        # JOB_LINKAGE WITH SKILL TABLE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_skills (
                job_id INTEGER NOT NULL,
                skill_id INTEGER NOT NULL,
                PRIMARY KEY (job_id, skill_id),
                FOREIGN KEY (job_id) REFERENCES jobs(job_id),
                FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
            )
        ''')

        # APPLICATION TABLE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                application_id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                applicant_id INTEGER NOT NULL,
                resume TEXT,
                status TEXT DEFAULT 'received',
                application_date TEXT NOT NULL,
                FOREIGN KEY (job_id) REFERENCES jobs(job_id),
                FOREIGN KEY (applicant_id) REFERENCES users(user_id)
            )
        ''')

        # RESULT TABLE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS match_results (
                match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                tfidf_score REAL NOT NULL,
                match_time TEXT NOT NULL,
                FOREIGN KEY (resume_id) REFERENCES resumes(resume_id),
                FOREIGN KEY (job_id) REFERENCES jobs(job_id)
            )
        ''')

        conn.commit()
        conn.close()



    def add_user(self, user: User) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (name, email,password, user_type, skills)
                VALUES (?, ?, ?, ?, ?)
            ''', (user.name, user.email,user.password,user.user_type,','.join(user.skills)))
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            print(f"Email {user.email} exist")
            return -1
        finally:
            conn.close()

    def add_job(self, job: Job, posted_by: int) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO jobs (title, company, description, post_time,posted_by)
            VALUES (?, ?, ?, ?,?)
        ''', (job.title, job.company, job.description, job.post_time,posted_by))
        job_id = cursor.lastrowid

        for skill_name in job.skills:
            cursor.execute('INSERT OR IGNORE INTO skills (name) VALUES (?)', (skill_name,))
            cursor.execute('SELECT skill_id FROM skills WHERE name = ?', (skill_name,))
            skill_id = cursor.fetchone()[0]
            cursor.execute('''
                INSERT OR IGNORE INTO job_skills (job_id, skill_id)
                VALUES (?, ?)
            ''', (job_id, skill_id))
        conn.commit()
        conn.close()
        return job_id

    def add_resume(self, resume: Resume) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO resumes (user_id, content, create_time)
            VALUES (?, ?, ?)
        ''', (resume.user_id, resume.content, resume.create_time))
        resume_id = cursor.lastrowid

        for skill in resume.skills:
            cursor.execute('INSERT OR IGNORE INTO skills (name) VALUES (?)', (skill.name,))
            cursor.execute('SELECT skill_id FROM skills WHERE name = ?', (skill.name,))
            skill_id = cursor.fetchone()[0]
            cursor.execute('''
                INSERT OR IGNORE INTO resume_skills (resume_id, skill_id)
                VALUES (?, ?)
            ''', (resume_id, skill_id))
        conn.commit()
        conn.close()
        return resume_id

    def add_application(self,job_id,applicant_id,resume,status,application_date):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO applications (job_id, applicant_id, resume, status, application_date)
        VALUES (?, ?, ?, ?, ?)''', (job_id, applicant_id, resume, status, application_date))
        app_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return app_id

    def get_all_resumes_for_tfidf(self) -> list[tuple[int, str]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        # READ RESUME + SKILL
        cursor.execute('''
            SELECT r.resume_id, r.content, GROUP_CONCAT(s.name, ' ')
            FROM resumes r
            LEFT JOIN resume_skills rs ON r.resume_id = rs.resume_id
            LEFT JOIN skills s ON rs.skill_id = s.skill_id
            GROUP BY r.resume_id
        ''')
        results = cursor.fetchall()
        conn.close()
        return [(rid, f"{content} {skills if skills else ''}") for rid, content, skills in results]

    def get_all_jobs_for_tfidf(self) -> list[tuple[int, str]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT j.job_id, j.title, j.description, GROUP_CONCAT(s.name, ' ')
            FROM jobs j
            LEFT JOIN job_skills js ON j.job_id = js.job_id
            LEFT JOIN skills s ON js.skill_id = s.skill_id
            GROUP BY j.job_id
        ''')
        results = cursor.fetchall()
        conn.close()
        return [(jid, f"{title} {description} {skills if skills else ''}") for jid, title, description, skills in results]

    def save_tfidf_match_result(self, resume_id: int, job_id: int, score: float):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO match_results 
            (resume_id, job_id, tfidf_score, match_time)
            VALUES (?, ?, ?, ?)
        ''', (resume_id, job_id, round(score, 4), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

    def get_match_result(self, resume_id: int, job_id: int) -> float:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT tfidf_score FROM match_results
            WHERE resume_id = ? AND job_id = ?
            ORDER BY match_time DESC LIMIT 1
        ''', (resume_id, job_id))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0.0
    
    def get_user_by_email(self, email: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, name, email, password, user_type, skills FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {'user_id': row[0], 'name': row[1], 'email': row[2], 'password': row[3], 'user_type': row[4],'skills': row[5] if len(row) > 5 and row[5] else ''}
        return None

    def update_application_status(self, application_id: int, new_status: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE applications SET status = ? WHERE application_id = ?', (new_status, application_id))
        conn.commit()
        conn.close()