# create_table = """CREATE TABLE IF NOT EXISTS PhoneBook (name, surname, phone, mail)"""

insert_data = """INSERT INTO users (username,password) VALUES ('{username}', '{password}')"""

# list_data = """SELECT * FROM PhoneBook WHERE delete_info='FALSE'"""

# delete_number = """UPDATE PhoneBook SET delete_info='TRUE' WHERE ID={delete_id}"""

check_login = """SELECT * FROM users WHERE username='{username}' AND password='{password}' """

update_token = """UPDATE users SET token='{token}' WHERE username='{username}'"""

check_token = """SELECT * FROM users WHERE token='{token}' """