# Student Course Enrollment Tracker

A minimal full-stack app demonstrating 8 nested/subquery SQL patterns.

**Stack:** FastAPI (Python) · PostgreSQL · plain HTML/JS

For a walkthrough of how everything works, see [EXPLANATION.md](EXPLANATION.md).

## Prerequisites

- Python 3.11+
- PostgreSQL 18, running locally on port 5432

If `psql` isn't on your PATH, use the full path instead:
`"C:\Program Files\PostgreSQL\18\bin\psql.exe"`

## Setup

**1. Create the database**

```powershell
psql -U postgres -c "CREATE DATABASE enrollment_tracker;"
```

**2. Create the virtual environment and install dependencies**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**3. Configure credentials**

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/enrollment_tracker
```

If your password contains special characters, percent-encode them (`@` → `%40`).

**4. Create the tables**

```powershell
psql -U postgres -d enrollment_tracker -f schema.sql
```

**5. Load sample data**

```powershell
python seed.py
```

Seeds 3 instructors, 12 students, 5 courses, and 21 enrollments.

**6. Start the server**

```powershell
uvicorn main:app --reload
```

- App: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs

## The 8 Queries

| # | Endpoint | SQL Pattern |
|---|---|---|
| 1 | `/api/q1/above-course-average` | Correlated subquery in `WHERE` |
| 2 | `/api/q2/popular-courses` | Subquery in `HAVING` |
| 3 | `/api/q3/not-taught-by/{instructor_id}` | `NOT IN` + subquery |
| 4 | `/api/q4/top-per-course` | `MAX` per group in `WHERE` |
| 5 | `/api/q5/busy-instructors` | Subquery in `FROM` (derived table) |
| 6 | `/api/q6/enrolled-students` | `EXISTS` (correlated) |
| 7 | `/api/q7/empty-courses` | `NOT EXISTS` |
| 8 | `/api/q8/ranked-scores` | Scalar subquery in `SELECT` |

All queries are raw SQL so the nesting stays visible. They live in `main.py`, and
`queries.sql` has the same eight with commentary for reading standalone.

## Project Structure

```
├── .env                 # DB credentials (not committed)
├── requirements.txt
├── schema.sql           # Table definitions
├── seed.py              # Sample data loader
├── db.py                # Connection + query helper
├── main.py              # FastAPI app, 8 endpoints
├── queries.sql          # The 8 queries, annotated
├── EXPLANATION.md       # How it all works
└── static/index.html    # Single-page frontend
```

## Schema

- `instructors` (id, name)
- `students` (id, name, email)
- `courses` (id, name, instructor_id → instructors)
- `enrollments` (id, student_id → students, course_id → courses, score)

`score` is nullable — a student can be enrolled but ungraded.
