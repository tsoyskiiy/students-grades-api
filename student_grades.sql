DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;

CREATE TABLE students (
	student_id SERIAL PRIMARY KEY,
	full_name TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	born_on DATE,
	joined_on DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE courses(
	course_id SERIAL PRIMARY KEY,
	course_name TEXT NOT NULL,
	professor_name TEXT NOT NULL,
	credits INTEGER NOT NULL CHECK (credits > 0)
);

CREATE TABLE grades(
	grade_id SERIAL PRIMARY KEY,
	student_id INTEGER NOT NULL REFERENCES students(student_id),
	course_id INTEGER NOT NULL REFERENCES courses(course_id),
	grade NUMERIC(5, 2) NOT NULL CHECK (grade BETWEEN 0 AND 100),
	UNIQUE (student_id, course_id)
);

INSERT INTO courses (course_name, professor_name, credits) VALUES
	('Databases', 'John W.', 3),
	('Statistics', 'Chris D.', 2),
	('Algorithms', 'Jeff S.', 3);

INSERT INTO students (full_name, email, born_on) VALUES 
	('Den', 'den@gmail.com', '2001-08-26'),
	('Bob', 'bob@gmail.com', NULL),
	('Ann', 'ann@gmail.com', NULL);

INSERT INTO grades (student_id, course_id, grade) VALUES
	(1,1,85),
	(1,2, 90),
	(2,1, 95),
	(3,3, 65);

UPDATE students SET born_on = '1999-07-04' WHERE email = 'bob@gmail.com';
UPDATE students SET email = 'den1@gmail.com' WHERE student_id = 1;

DELETE FROM grades WHERE student_id = 3;
DELETE FROM students WHERE student_id = 3;

SELECT * FROM students;
SELECT s.full_name, c.course_name, g.grade
FROM grades g
JOIN students s ON s.student_id = g.student_id
JOIN courses c ON c.course_id = g.course_id;

