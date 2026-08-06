DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS instructors;

CREATE TABLE instructors (
    id   SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE students (
    id    SERIAL PRIMARY KEY,
    name  TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE courses (
    id            SERIAL PRIMARY KEY,
    name          TEXT NOT NULL,
    instructor_id INTEGER REFERENCES instructors(id)
);

CREATE TABLE enrollments (
    id         SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    course_id  INTEGER NOT NULL REFERENCES courses(id),
    score      NUMERIC(5,2),
    UNIQUE (student_id, course_id)
);
