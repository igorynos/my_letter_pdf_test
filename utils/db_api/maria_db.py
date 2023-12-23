import pymysql
from data import config
import random


class Database:
    def __init__(self, path_to_db=(config.IP, config.PGUSER, config.PGPASSWORD, config.DATABASE, config.PORT)):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return pymysql.connect(host=self.path_to_db[0],
                               user=self.path_to_db[1],
                               password=self.path_to_db[2],
                               database=self.path_to_db[3],
                               port=self.path_to_db[4])

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):

        if not parameters:
            parameters = tuple()

        connection = self.connection
        cursor = connection.cursor()
        cursor.execute(sql, parameters)

        data = None

        if commit:
            connection.commit()

        if fetchone:
            data = cursor.fetchone()

        if fetchall:
            data = cursor.fetchall()

        connection.close()

        return data

    def create_table_users(self):
        sql = "CREATE TABLE `users` (\
                `id` int(11) NOT NULL PRIMARY KEY,\
                `name` text DEFAULT NULL,\
                `status` text DEFAULT NULL,\
                `adress` text DEFAULT NULL,\
                `phone` text DEFAULT NULL,\
                `email` text DEFAULT NULL,\
                `inn` text DEFAULT NULL,\
                `pasport` text DEFAULT NULL,\
                `born` text DEFAULT NULL,\
                `comment` text DEFAULT NULL,\
            )"
        self.execute(sql, commit=True)

    def create_table_cont_users(self):
        sql = "CREATE TABLE `cont_users` (\
                `name` text DEFAULT NULL,\
                `status` text DEFAULT NULL,\
                `adress` text DEFAULT NULL,\
                `phone` text DEFAULT NULL,\
                `email` text DEFAULT NULL,\
                `inn` text DEFAULT NULL,\
                `pasport` text DEFAULT NULL,\
                `born` text DEFAULT NULL,\
                `comment` text DEFAULT NULL,\
                `user` int(11) DEFAULT NULL,\
                `id` int(11) DEFAULT NULL,\
                KEY `cont_users_FK` (`user`),\
                CONSTRAINT `cont_users_FK` FOREIGN KEY (`user`) REFERENCES `users` (`id`)\
            )"

        self.execute(sql, commit=True)

    def create_table_template(self):
        sql = "CREATE TABLE IF NOT EXISTS template ( \
					name 	TEXT,\
					link 	TEXT,\
					id 	int(11)\
                    )"

        self.execute(sql, commit=True)

    def add_user(self, id: int,
                 name: str,
                 status='',
                 adress='',
                 phone='',
                 email='',
                 inn='',
                 pasport='',
                 born='',
                 comment=''):
        sql = "INSERT IGNORE INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        parameters = (id, name, status, adress, phone,
                      email, inn, pasport, born, comment)
        self.execute(sql, parameters=parameters, commit=True)

    def add_cont_user(self, org: str,
                      ogrn='',
                      adress='',
                      phone='',
                      email='',
                      inn='',
                      pasport='',
                      born='',
                      comment='',
                      fio='',
                      headstatus='',
                      fiocont='',
                      link='',
                      user=None,
                      id=random.randint(1000000, 9999999)):
        sql = "INSERT IGNORE INTO cont_users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        parameters = (org, ogrn, adress, phone,
                      email, inn, pasport, born, comment, fio, headstatus, fiocont, link, user, id)
        self.execute(sql, parameters=parameters, commit=True)

    def update_user(self, id: int,
                    name='',
                    status='',
                    adress='',
                    phone='',
                    email='',
                    inn='',
                    pasport='',
                    born='',
                    comment=''):
        lst_args = {
            "id": id,
            "name": name,
            "status": status,
            "adress": adress,
            "phone": phone,
            "email": email,
            "inn": inn,
            "pasport": pasport,
            "born": born,
            "comment": comment
        }
        for data in lst_args.items():
            if data[1] != '' and data[0] != 'id':
                sql = f"UPDATE users SET {data[0]}=%s WHERE id=%s;"
                self.execute(sql, parameters=(
                    data[1], lst_args['id']), commit=True)

    def update_cont_user(self, org='',
                         ogrn='',
                         adress='',
                         phone='',
                         email='',
                         inn='',
                         pasport='',
                         born='',
                         comment='',
                         fio='',
                         headstatus='',
                         fiocont='',
                         link=''
                         ):
        lst_args = {
            "org": org,
            "ogrn": ogrn,
            "adress": adress,
            "phone": phone,
            "email": email,
            "inn": inn,
            "pasport": pasport,
            "born": born,
            "comment": comment,
            "fio": fio,
            "headstatus": headstatus,
            "fiocont": fiocont,
            "link": link
        }
        for data in lst_args.items():
            if data[1] != '' and data[0] != 'org':
                sql = f"UPDATE cont_users SET {data[0]}=%s WHERE org=%s;"
                self.execute(sql, parameters=(
                    data[1], lst_args['org']), commit=True)

    def add_template(self, name: str, link: str, template_id: int):
        sql = "INSERT IGNORE INTO template VALUES (%s, %s, %s);"
        parameters = (name, link, template_id)
        self.execute(sql, parameters=parameters, commit=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM users", fetchone=True)

    def count_template(self):
        return self.execute("SELECT COUNT(*) FROM users", fetchone=True)
