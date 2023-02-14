create_table = """CREATE TABLE IF NOT EXISTS PhoneBook (name, surname, phone, mail)"""

check_data = """SELECT COUNT(*) FROM PhoneBook"""

insert_data = """INSERT INTO users (username,password) VALUES ('{username}', '{password}')"""

list_data = """SELECT * FROM PhoneBook WHERE delete_info='FALSE'"""

delete_number = """UPDATE PhoneBook SET delete_info='TRUE' WHERE ID={delete_id}"""

check_login = """SELECT * FROM users WHERE username='{username}' AND password='{password}' """