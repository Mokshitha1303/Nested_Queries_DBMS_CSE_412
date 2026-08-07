# Student Course Enrollment Tracker

A full-stack web app built with **FastAPI** (Python) and **PostgreSQL**, demonstrating
**6 nested SQL queries**. Each query uses a different subquery pattern, written as raw
SQL so the nesting stays visible.

The frontend is a single HTML page with two sections: buttons to view the four raw
database tables, and buttons to run each nested query.




## Folder Structure

```

├── requirements.txt     # Python packages
├── schema.sql           # Creates the 4 tables
├── seed.py              # Loads sample data
├── db.py                # Connects to PostgreSQL, runs SQL
├── main.py              # FastAPI app, all API endpoints
└── static/
    └── index.html       # Frontend page
```

**What each file does**

| File | Purpose |
|---|---|
| `schema.sql` | Defines the four tables. Drops them first, so it's safe to re-run. |
| `seed.py` | Fills the tables with 3 instructors, 12 students, 5 courses, 21 enrollments. |
| `db.py` | Reads the password from `.env`, opens a connection, runs SQL, returns rows as Python dictionaries. |
| `main.py` | Every URL the app responds to. Each function holds one raw SQL query. |
| `static/index.html` | The whole frontend — buttons, styling, and the JavaScript that fetches data and builds the tables. |

## Database Schema

| Table | Columns |
|---|---|
| `instructors` | id, name |
| `students` | id, name, email |
| `courses` | id, name, instructor_id |
| `enrollments` | id, student_id, course_id, score |

`score` can be empty — a student may be enrolled but not yet graded.

## The 6 Nested Queries

### 1. Above Course Average
`GET /api/q1/above-course-average`

Finds students who scored higher than the average of their **own** course. Each course
gets its own average, so a 78 might pass in one course and fail in another.

*Pattern: correlated subquery in `WHERE`*

### 2. Popular Courses
`GET /api/q2/popular-courses`

Counts how many students are in each course, works out the average across all courses,
and shows only the courses above that average.

*Pattern: subquery in `HAVING`*

### 3. Top Per Course
`GET /api/q4/top-per-course`

Shows the highest scorer in every course. If two students tie for the top score, both
appear.

*Pattern: `MAX` per group in a correlated subquery*

### 4. Enrolled Students
`GET /api/q6/enrolled-students`

Lists students who are signed up for at least one course.

*Pattern: `EXISTS`*

### 5. Empty Courses
`GET /api/q7/empty-courses`

Lists courses that nobody has enrolled in.

*Pattern: `NOT EXISTS`*

### 6. Score Rankings
`GET /api/q8/ranked-scores`

Shows every score along with that student's rank in the course, worked out by counting
how many classmates scored higher. Results are displayed as a separate table per course.

*Pattern: scalar subquery in `SELECT`*

## Table Endpoints

Four extra endpoints show the raw contents of each table, so you can see the underlying
data the queries run against:

```
GET /api/tables/students
GET /api/tables/instructors
GET /api/tables/courses
GET /api/tables/enrollments
```
