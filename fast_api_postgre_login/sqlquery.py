# create_table = """CREATE TABLE IF NOT EXISTS users (name, surname, phone, mail)"""

insert_data = """INSERT INTO users (email,password,role) VALUES ('{email}', '{password}', '{role}')"""

check_login = """SELECT * FROM users WHERE email='{email}' AND password='{password}' """

update_token = """UPDATE users SET token='{token}', expire_time='{expire_time}' WHERE email='{email}'"""

check_token = """SELECT * FROM users WHERE token='{token}' and expire_time >'{now}'"""

create_lesson = """INSERT INTO lessons_notes (email,lesson,exam_marks,letter_grade) VALUES ('{email}', '{lesson}', '{exam_marks}', '{letter_grade}') """

check_lesson = """ SELECT * FROM lessons_notes WHERE email='{email}' """

check_email = """SELECT email FROM users WHERE token ='{token}' """

update_lesson = """UPDATE lessons_notes SET exam_marks = '{exam_marks}', letter_grade = '{letter_grade}'  WHERE email = '{email}' and lesson='{lesson}'"""