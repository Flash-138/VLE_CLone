DELIMITER //

-- 1. CONTENT MODULE ------------------------------------------------------

CREATE PROCEDURE sp_add_content(
    IN p_content_id      INT,
    IN p_content_name    VARCHAR(100),
    IN p_content_type    VARCHAR(50),
    IN p_content_data_url VARCHAR(255),
    IN p_section_id      INT,
    IN p_course_id       VARCHAR(25)
)
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM SectionCourse
        WHERE section_id = p_section_id
          AND course_id  = p_course_id
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Section not part of course';
    END IF;

    INSERT INTO Content(content_id, contentName, content_type, content_data_url)
    VALUES(p_content_id, p_content_name, p_content_type, p_content_data_url);

    INSERT INTO SectionContent(content_id, section_id)
    VALUES(p_content_id, p_section_id);
END;
//

-- 2. ASSIGNMENT SUBMISSION & GRADING -------------------------------------

CREATE PROCEDURE sp_submit_assignment(
    IN p_submission_id INT,
    IN p_user_id       INT,
    IN p_course_id     VARCHAR(25),
    IN p_assignment_id INT,
    IN p_document      BLOB
)
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM Course_Assignment
        WHERE course_id     = p_course_id
          AND assignment_id = p_assignment_id
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Assignment not associated with this course';
    END IF;

    INSERT INTO Submission(submission_id, submission_date, document)
    VALUES(p_submission_id, NOW(), p_document);

    INSERT INTO StudentSubmission(submission_id, user_id)
    VALUES(p_submission_id, p_user_id);
END;
//

CREATE PROCEDURE sp_grade_assignment(
    IN p_assignment_id INT,
    IN p_submission_id INT,
    IN p_grade         TINYINT
)
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM Submission
        WHERE submission_id = p_submission_id
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Submission does not exist';
    END IF;

    REPLACE INTO Grade(assignment_id, submission_id, grade)
    VALUES(p_assignment_id, p_submission_id, p_grade);
END;
//

-- 3. COURSE REGISTRATION -------------------------------------------------

CREATE PROCEDURE sp_register_course(
    IN p_user_id   INT,
    IN p_course_id VARCHAR(25)
)
BEGIN
    IF (p_user_id DIV 10000 = 100
        AND p_user_id BETWEEN 1000000 AND 1009999) THEN

        IF EXISTS (
            SELECT 1 FROM User_Course
            WHERE course_id = p_course_id
              AND user_id   BETWEEN 1000000 AND 1009999
        ) THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Lecturer already assigned to a course';
        END IF;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM Course
        WHERE course_id = p_course_id
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'No course called ';
    END IF;

    INSERT INTO User_Course(user_id, course_id)
    VALUES(p_user_id, p_course_id);
END//

-- 4. FORUM & THREAD MANAGEMENT -------------------------------------------

CREATE PROCEDURE sp_create_forum(
    IN p_forum_id INT,
    IN p_title    VARCHAR(255),
    IN p_info     TEXT,
    IN p_course_id VARCHAR(25)
)
BEGIN
    INSERT INTO Forum(forum_id, title, info)
    VALUES(p_forum_id, p_title, p_info);

    INSERT INTO Course_Forum(forum_id, course_id)
    VALUES(p_forum_id, p_course_id);
END;
//

CREATE PROCEDURE sp_create_thread(
    IN p_thread_id   INT,
    IN p_message_info TEXT,
    IN p_forum_id     INT,
    IN p_user_id      INT
)
BEGIN
    INSERT INTO Thread(thread_id, message_info)
    VALUES(p_thread_id, p_message_info);

    INSERT INTO Forum_Thread(thread_id, forum_id)
    VALUES(p_thread_id, p_forum_id);

    INSERT INTO ThreadOwner(thread_id, user_id)
    VALUES(p_thread_id, p_user_id);
END;
//

CREATE PROCEDURE sp_reply_to_thread(
    IN p_reply_id        INT,
    IN p_user_id         INT,
    IN p_message         TEXT,
    IN p_thread_id       INT,
    IN p_parent_reply_id INT  
)
BEGIN
    INSERT INTO Reply(reply_id, user_id, message)
    VALUES(p_reply_id, p_user_id, p_message);

    INSERT INTO Thread_response(reply_id, thread_id)
    VALUES(p_reply_id, p_thread_id);

    IF p_parent_reply_id IS NOT NULL THEN
        INSERT INTO Parent_reply(reply_id, parent_reply_id)
        VALUES(p_reply_id, p_parent_reply_id);
    END IF;
END;
//

-- 5. CALENDAR EVENTS ------------------------------------------------------

CREATE PROCEDURE sp_create_calendar_event(
    IN p_event_id   INT,
    IN p_title      VARCHAR(255),
    IN p_event_date DATETIME,
    IN p_course_id  VARCHAR(25)
)
BEGIN
    INSERT INTO CalendarEvent(event_id, title, event_date)
    VALUES(p_event_id, p_title, p_event_date);

    INSERT INTO CourseEvent(event_id, course_id)
    VALUES(p_event_id, p_course_id);
END;
//

DELIMITER ;
