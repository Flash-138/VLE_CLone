CREATE OR REPLACE VIEW vw_course_content AS
SELECT
  sc.course_id,
  s.section_id, s.section_name,
  c.content_id, c.contentName, c.content_type, c.content_data_url
FROM Section s
JOIN SectionCourse sc  ON s.section_id = sc.section_id
JOIN SectionContent sc2 ON s.section_id = sc2.section_id
JOIN Content c           ON sc2.content_id = c.content_id;

CREATE OR REPLACE VIEW vw_user_calendar AS
SELECT
  uc.user_id, ce.event_id, ce.title, ce.event_date
FROM User_Course uc
JOIN CourseEvent coe     ON uc.course_id = coe.course_id
JOIN CalendarEvent ce    ON coe.event_id = ce.event_id;


CREATE OR REPLACE VIEW vw_course_calendar AS
SELECT
  ce.event_id, ce.title, ce.event_date, coe.course_id
FROM CourseEvent coe
JOIN CalendarEvent ce ON coe.event_id = ce.event_id;

CREATE OR REPLACE VIEW PopularCourses AS
SELECT uc.course_id, COUNT(uc.user_id) AS student_count
FROM User_Course uc
JOIN User u ON uc.user_id = u.user_id
WHERE u.role = 'student'
GROUP BY uc.course_id
HAVING COUNT(uc.user_id) >= 50;

CREATE OR REPLACE VIEW ActiveStudents AS
SELECT user_id, COUNT(course_id) AS course_count
FROM User_Course
GROUP BY user_id
HAVING COUNT(course_id) >= 5;

CREATE OR REPLACE VIEW TopLecturers AS
SELECT uc.user_id, COUNT(uc.course_id) AS course_count
FROM User_Course uc
JOIN User u ON uc.user_id = u.user_id
WHERE u.role = 'lecturer'
GROUP BY uc.user_id
HAVING COUNT(uc.course_id) >= 3;

CREATE OR REPLACE VIEW TopEnrolledCourses AS
SELECT course_id, COUNT(user_id) AS enrollment_count
FROM User_Course
GROUP BY course_id
ORDER BY enrollment_count DESC
LIMIT 10;

CREATE OR REPLACE VIEW TopStudentsByGrade AS
SELECT 
    course_averages.user_id,
    ROUND(AVG(course_avg), 2) AS overall_avg
FROM (
    SELECT 
        ss.user_id,
        ca.course_id,
        AVG(g.grade) AS course_avg
    FROM Grade g
    JOIN StudentSubmission ss ON g.submission_id = ss.submission_id
    JOIN Submission s ON s.submission_id = ss.submission_id
    JOIN Course_Assignment ca ON g.assignment_id = ca.assignment_id
    JOIN User u ON ss.user_id = u.user_id
    WHERE u.role = 'student'
    GROUP BY ss.user_id, ca.course_id
) AS course_averages
GROUP BY course_averages.user_id
ORDER BY overall_avg DESC
LIMIT 10;
