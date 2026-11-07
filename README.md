# TalentHub – Campus Placement Management System

TalentHub is a web-based campus placement management system built with **Python, Flask, HTML, CSS, and SQLite**. It supports three roles: Student, Company, and Placement Coordinator.

## Features

- Student and company registration and login
- Student profile management, including CGPA, department, year, active backlogs, and skills
- Company job posting and applicant viewing
- Automatic eligibility checking using minimum CGPA, maximum active backlogs, and eligible departments
- Prevention of duplicate applications
- Application status management
- Interview scheduling
- Offer creation and student offer responses
- Student notifications
- Role-based access checks and password hashing

## Technology stack

| Part | Technology |
|---|---|
| Backend | Python 3, Flask |
| Frontend | HTML, CSS, Jinja templates |
| Default database | SQLite |
| Alternate schema script | MySQL 8 (`schema_mysql.sql`) |

**Database note:** The application currently connects to SQLite by default and creates its database automatically at `instance/talenthub.db`. The `schema_mysql.sql` file is a MySQL 8 version of the database design; the current Flask database connection layer has not been converted to MySQL.

## Run the project on Windows

1. Install Python 3.10 or later.
2. Extract the ZIP file.
3. Open the extracted `TalentHub-Python-Flask` folder in VS Code.
4. In VS Code, select **Terminal → New Terminal**.
5. Run these commands one at a time:

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python seed.py
   python run.py
   ```

6. Open this address in your browser:

   `http://127.0.0.1:5000`

The `python seed.py` command is optional. Run it once to insert sample users, companies, jobs, and skills into a fresh database. If you run it again after demo data already exists, it reports that the demo data is already present.

### Demo login accounts

After running `python seed.py`:

| Role | Email | Password |
|---|---|---|
| Student | `asha@student.edu` | `Password@123` |
| Student | `ravi@student.edu` | `Password@123` |
| Company | `hr@technova.com` | `Password@123` |
| Company | `hr@dataworks.com` | `Password@123` |
| Coordinator | `coordinator@talenthub.local` | `Admin@1234` |

The Ravi student account is intended to demonstrate cases where a student does not meet some job eligibility conditions.

## Run the automated tests

After installing the requirements, run:

```powershell
python -m unittest discover -s tests -v
```

## Project structure

```text
TalentHub-Python-Flask/
│
├── app/
│   ├── routes/             Flask routes for each role
│   ├── templates/          HTML/Jinja pages
│   ├── static/              CSS
│   ├── db.py                SQLite connection and schema setup
│   ├── repositories.py      Database queries
│   ├── services.py          Validation and business rules
│   └── schema.sql           SQLite database schema
│
├── tests/                   Automated tests
├── instance/                Runtime SQLite database location
├── schema_mysql.sql         MySQL 8 schema reference
├── seed.py                  Sample data loader
├── run.py                   Application entry point
├── requirements.txt         Python dependencies
└── README.md
```

## Eligibility rules

When a student applies for a job, the backend checks the criteria configured for that job:

- Student CGPA must be greater than or equal to the minimum CGPA.
- Student active backlog count must be less than or equal to the maximum permitted active backlogs, when a maximum is specified.
- Student department must be in the allowed department list, when the company specifies one.

The checks are performed on the server, not only in the browser. A student who does not satisfy the criteria is prevented from applying and is shown the reasons.

## Important notes before publishing

- Do not upload personal database files, passwords, or secret keys.
- The `.gitignore` file excludes the local virtual environment, SQLite database folder, and `.env` files.
- The default secret key and coordinator credentials are for local coursework/demo use. Change them before any real deployment.
- This project is configured for local development and is not production-hardened.
