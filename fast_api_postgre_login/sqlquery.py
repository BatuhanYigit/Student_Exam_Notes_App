# create_table = """CREATE TABLE IF NOT EXISTS PhoneBook (name, surname, phone, mail)"""

insert_data = """INSERT INTO users (email,password,role) VALUES ('{email}', '{password}', '{role}')"""

# list_data = """SELECT * FROM PhoneBook WHERE delete_info='FALSE'"""

# delete_number = """UPDATE PhoneBook SET delete_info='TRUE' WHERE ID={delete_id}"""

check_login = """SELECT * FROM users WHERE email='{email}' AND password='{password}' """

update_token = """UPDATE users SET token='{token}', expire_time='{expire_time}' WHERE email='{email}'"""

check_token = """SELECT * FROM users WHERE token='{token}' and expire_time > '{now}'"""

create_lesson = """INSERT INTO lessons_note (email,lesson,exam_marks,letter_grade) VALUES ('{email}', '{lesson}', '{exam_marks}', '{letter_grade}') """