
SELECT COUNT(*) AS student_count
FROM User
WHERE role = 'student';

SELECT COUNT(*) AS course_count
FROM Course;

SELECT MAX(course_count) AS max_courses_per_student
FROM (
    SELECT user_id, COUNT(*) AS course_count
    FROM User_Course
    JOIN User USING(user_id)
    WHERE role = 'student'
    GROUP BY user_id
) AS student_courses;

SELECT MIN(course_count) AS min_courses_per_student
FROM (
    SELECT user_id, COUNT(*) AS course_count
    FROM User_Course
    JOIN User USING(user_id)
    WHERE role = 'student'
    GROUP BY user_id
) AS student_courses;

SELECT MIN(member_count) AS min_members_per_course
FROM (
    SELECT course_id, COUNT(*) AS member_count
    FROM User_Course
    GROUP BY course_id
) AS course_members;

SELECT MAX(course_count) AS max_courses_per_lecturer
FROM (
    SELECT user_id, COUNT(*) AS course_count
    FROM User_Course
    JOIN User USING(user_id)
    WHERE role = 'lecturer'
    GROUP BY user_id
) AS lecturer_courses;

SELECT MIN(course_count) AS min_courses_per_lecturer
FROM (
    SELECT user_id, COUNT(*) AS course_count
    FROM User_Course
    JOIN User USING(user_id)
    WHERE role = 'lecturer'
    GROUP BY user_id
) AS lecturer_courses;
