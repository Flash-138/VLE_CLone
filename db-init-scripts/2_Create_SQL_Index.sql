CREATE INDEX idx_usercourse_user ON User_Course(user_id);

CREATE INDEX idx_usercourse_course ON User_Course(course_id);

CREATE INDEX idx_event_date ON CalendarEvent(event_date);

CREATE INDEX idx_sectioncourse_course ON SectionCourse(course_id);

CREATE INDEX idx_sectioncontent_section ON SectionContent(section_id);

CREATE INDEX idx_sectioncontent_content ON SectionContent(content_id);

CREATE INDEX idx_course_assignment_course ON Course_Assignment(course_id);

CREATE INDEX idx_submission_id ON Submission(submission_id);

CREATE INDEX idx_studentsubmission_user ON StudentSubmission(user_id);

CREATE INDEX idx_grade_lookup ON Grade(assignment_id, submission_id);

CREATE INDEX idx_forumthread_forum ON Forum_Thread(forum_id);

CREATE INDEX idx_threadresponse_thread ON Thread_response(thread_id);

CREATE INDEX idx_parentreply_parent ON Parent_reply(parent_reply_id);

CREATE INDEX idx_courseevent_course ON CourseEvent(course_id);

CREATE INDEX idx_calendarevent_date ON CalendarEvent(event_date);





