from fastapi import FastAPI
from db import run_query

app = FastAPI(title="Student Course Enrollment Tracker")


@app.get("/api/q1/above-course-average")
def above_course_average():
    """Students who scored above the average score in the respective course."""
    sql = """
        SELECT s.name AS student, c.name AS course, e.score
        FROM enrollments e
        JOIN students s ON s.id = e.student_id
        JOIN courses  c ON c.id = e.course_id
        WHERE e.score > (
            SELECT AVG(e2.score)
            FROM enrollments e2
            WHERE e2.course_id = e.course_id
        )
        ORDER BY c.name, e.score DESC;
    """
    return run_query(sql)

@app.get("/api/q2/popular-courses")
def popular_courses():
    """Courses whose enrollment count is above the overall average enrollment."""
    sql = """
        SELECT c.name AS course, COUNT(e.id) AS enrollment_count
        FROM courses c
        LEFT JOIN enrollments e ON e.course_id = c.id
        GROUP BY c.id, c.name
        HAVING COUNT(e.id) > (
            SELECT AVG(cnt)
            FROM (
                SELECT COUNT(*) AS cnt
                FROM enrollments
                GROUP BY course_id
            ) AS per_course
        )
        ORDER BY enrollment_count DESC;
    """
    return run_query(sql)

@app.get("/api/q4/top-per-course")
def top_per_course():
    """The top-scoring student in each course."""
    sql = """
        SELECT c.name AS course, s.name AS student, e.score
        FROM enrollments e
        JOIN students s ON s.id = e.student_id
        JOIN courses  c ON c.id = e.course_id
        WHERE e.score = (
            SELECT MAX(e2.score)
            FROM enrollments e2
            WHERE e2.course_id = e.course_id
        )
        ORDER BY c.name;
    """
    return run_query(sql)


@app.get("/api/q6/enrolled-students")
def enrolled_students():
    """Students who have at least one enrollment."""
    sql = """
        SELECT s.id, s.name, s.email
        FROM students s
        WHERE EXISTS (
            SELECT 1
            FROM enrollments e
            WHERE e.student_id = s.id
        )
        ORDER BY s.name;
    """
    return run_query(sql)


@app.get("/api/q7/empty-courses")
def empty_courses():
    """Courses with no enrollments at all."""
    sql = """
        SELECT c.id, c.name, i.name AS instructor
        FROM courses c
        LEFT JOIN instructors i ON i.id = c.instructor_id
        WHERE NOT EXISTS (
            SELECT 1
            FROM enrollments e
            WHERE e.course_id = c.id
        )
        ORDER BY c.name;
    """
    return run_query(sql)

@app.get("/api/q8/ranked-scores")
def ranked_scores():
    """Each student's score with their rank within the course."""
    sql = """
        SELECT
            c.name AS course,
            s.name AS student,
            e.score,
            (
                SELECT COUNT(*) + 1
                FROM enrollments e2
                WHERE e2.course_id = e.course_id
                  AND e2.score > e.score
            ) AS rank_in_course
        FROM enrollments e
        JOIN students s ON s.id = e.student_id
        JOIN courses  c ON c.id = e.course_id
        WHERE e.score IS NOT NULL
        ORDER BY c.name, e.score DESC;
    """
    return run_query(sql)


@app.get("/api/tables/students")
def table_students():
    """Raw contents of the students table."""
    return run_query("SELECT id, name, email FROM students ORDER BY id;")


@app.get("/api/tables/instructors")
def table_instructors():
    """Raw contents of the instructors table."""
    return run_query("SELECT id, name FROM instructors ORDER BY id;")


@app.get("/api/tables/courses")
def table_courses():
    """Raw contents of the courses table."""
    return run_query("SELECT id, name, instructor_id FROM courses ORDER BY id;")


@app.get("/api/tables/enrollments")
def table_enrollments():
    """Raw contents of the enrollments table."""
    return run_query("SELECT id, student_id, course_id, score FROM enrollments ORDER BY id;")
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="static", html=True), name="static")
