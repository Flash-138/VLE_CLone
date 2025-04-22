CREATE TABLE User (
    user_id INT PRIMARY KEY,
    role ENUM('admin', 'lecturer', 'student') NOT NULL
);

CREATE TABLE Course (
    course_id VARCHAR(25) UNIQUE Not Null PRIMARY KEY,
    course_name VARCHAR(100) Not Null
);

CREATE TABLE User_Course (
    user_id INT,
    course_id VARCHAR(25),
    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Logins (
    user_id INT PRIMARY KEY,
    user_password VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);



CREATE TABLE CalendarEvent (
    event_id INT PRIMARY KEY,
    title VARCHAR(100),
    event_date DATETIME 
);


CREATE TABLE CourseEvent (
    event_id INT,
    course_id VARCHAR(25),
    PRIMARY KEY (event_id, course_id),
    FOREIGN KEY (event_id) REFERENCES CalendarEvent(event_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Forum (
    forum_id INT PRIMARY KEY,
    title VARCHAR(100),
    info TEXT
);

CREATE TABLE Thread (
    thread_id INT PRIMARY KEY,
    message_info TEXT
);

CREATE TABLE Course_Forum (
    forum_id INT,
    course_id VARCHAR(25),
    PRIMARY KEY (forum_id, course_id),
    FOREIGN KEY (forum_id) REFERENCES Forum(forum_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE Forum_Thread (
    thread_id INT,
    forum_id INT,
    PRIMARY KEY (thread_id,forum_id),
    FOREIGN KEY (thread_id) REFERENCES Thread(thread_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (forum_id) REFERENCES Forum(forum_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE ThreadOwner (
    thread_id INT ,
    user_id INT,
    PRIMARY KEY (thread_id, user_id),
    FOREIGN KEY (thread_id) REFERENCES Thread(thread_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE Reply (
    reply_id INT PRIMARY KEY,
    user_id INT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Parent_reply (
    reply_id INT PRIMARY KEY,
    parent_reply_id INT,
    FOREIGN KEY (reply_id) REFERENCES Reply(reply_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (parent_reply_id) REFERENCES Reply(reply_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Thread_response (
    reply_id INT,
    thread_id INT,
    PRIMARY KEY (reply_id, thread_id),
    FOREIGN KEY (reply_id) REFERENCES Reply(reply_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (thread_id) REFERENCES Thread(thread_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE Section (
    section_id INT PRIMARY KEY,
    section_name VARCHAR(255)
);

Create Table Content(
    content_id INT PRIMARY KEY,
    contentName VARCHAR(255) UNIQUE,
    content_type VARCHAR(50),
    content_data LONGBLOB 
);


Create Table SectionContent(
    content_id INT,
    section_id INT,
    PRIMARY KEY (content_id, section_id),
    FOREIGN KEY (content_id) REFERENCES Content(content_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (section_id) REFERENCES Section(section_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE SectionCourse (
    section_id INT,
    course_id VARCHAR(25),
    PRIMARY KEY (section_id, course_id),
    FOREIGN KEY (section_id) REFERENCES Section(section_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE Assignment (
    assignment_id INT PRIMARY KEY,
    title VARCHAR(100),
    info TEXT,
    due_date DATE,
    document LONGBLOB 
);


CREATE TABLE Course_Assignment (
    assignment_id INT,
    course_id VARCHAR(25),
    PRIMARY KEY (assignment_id, course_id),
    FOREIGN KEY (assignment_id) REFERENCES Assignment(assignment_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Submission (
    submission_id INT PRIMARY KEY,
    submission_date DATETIME ,
    document LONGBLOB 
);

CREATE TABLE StudentSubmission (
    submission_id INT,
    user_id INT,
    PRIMARY KEY (submission_id, user_id),
    FOREIGN KEY (submission_id) REFERENCES Submission(submission_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Grade (
    assignment_id INT,
    submission_id INT,
    grade INT,
    PRIMARY KEY (assignment_id, submission_id),
    FOREIGN KEY (assignment_id) REFERENCES Assignment(assignment_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (submission_id) REFERENCES Submission(submission_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);