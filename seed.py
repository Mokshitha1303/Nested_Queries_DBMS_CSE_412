import psycopg
from db import DATABASE_URL

INSTRUCTORS = [("Dr. Alan Reyes",), ("Dr. Maya Chen",), ("Dr. Omar Haddad",)]

STUDENTS = [
    ("Aisha Khan", "aisha.khan@asu.edu"),
    ("Brian Lopez", "brian.lopez@asu.edu"),
    ("Chen Wei", "chen.wei@asu.edu"),
    ("Diana Novak", "diana.novak@asu.edu"),
    ("Ethan Brooks", "ethan.brooks@asu.edu"),
    ("Farida Osei", "farida.osei@asu.edu"),
    ("Grace Kim", "grace.kim@asu.edu"),
    ("Hector Ramos", "hector.ramos@asu.edu"),
    ("Ivy Patel", "ivy.patel@asu.edu"),
    ("Jonas Muller", "jonas.muller@asu.edu"),
    ("Kavya Nair", "kavya.nair@asu.edu"),
    ("Liam O'Connor", "liam.oconnor@asu.edu"),
]

# (course name, instructor index 1-3)
COURSES = [
    ("Database Systems", 1),
    ("Operating Systems", 1),
    ("Machine Learning", 2),
    ("Computer Networks", 3),
    ("Compiler Design", 2),
]

# (student_id, course_id, score) -- None means enrolled but ungraded
ENROLLMENTS = [
    (1, 1, 92.5), (2, 1, 78.0), (3, 1, 85.5), (4, 1, 61.0), (5, 1, 88.0),
    (6, 1, None), (7, 1, 95.0), (8, 1, 70.5),
    (1, 2, 74.0), (3, 2, 89.5), (5, 2, 66.0), (9, 2, 91.0), (10, 2, 55.5),
    (2, 3, 97.0), (4, 3, 83.0), (6, 3, 79.5), (11, 3, 68.0), (12, 3, None),
    (7, 4, 81.0), (9, 4, 90.5), (11, 4, 72.0),
]


def main():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE enrollments, courses, students, instructors RESTART IDENTITY CASCADE;")
            cur.executemany("INSERT INTO instructors (name) VALUES (%s)", INSTRUCTORS)
            cur.executemany("INSERT INTO students (name, email) VALUES (%s, %s)", STUDENTS)
            cur.executemany("INSERT INTO courses (name, instructor_id) VALUES (%s, %s)", COURSES)
            cur.executemany(
                "INSERT INTO enrollments (student_id, course_id, score) VALUES (%s, %s, %s)",
                ENROLLMENTS,
            )
        conn.commit()
    print("Seeded.")


if __name__ == "__main__":
    main()
