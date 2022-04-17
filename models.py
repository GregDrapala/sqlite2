import os
import json
import logging

import sqlite3
from sqlite3 import Error



SAVED_FOLDER_NAME = 'Save'
FILE_NAME = "books.db"
FILE_PATH = os.path.join(SAVED_FOLDER_NAME, FILE_NAME)


class Books_SQLite:
    def __init__(self, db_file=FILE_PATH):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self.execute_sql()
        self.table = "books"

    def execute_sql(self):
        """
        Create Table or add task
        """
        sql = """
        -- episodes table
        CREATE TABLE IF NOT EXISTS books (
            id integer PRIMARY KEY,
            title text NOT NULL,
            description text NOT NULL,
            author text NOT NUll
            );
         """
        try:
            c = self.conn.cursor()
            c.execute(sql)
        except sqlite3.OperationalError as e:
            logging.warning(e)


    def add_book(self, episode):
        sql = '''INSERT INTO books(title, description, author)
                VALUES(?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, episode)
        self.conn.commit()
        return cur.lastrowid


    def select_all(self):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {self.table}")
        rows = cur.fetchall()
        return rows


    def select_where(self, **query):
        cur = self.conn.cursor()
        qs = []
        values = ()
        for k, v in query.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)
        cur.execute(f"SELECT * FROM {self.table} WHERE {q}", values)
        rows = cur.fetchall()
        return rows


    def update(self, id, **kwargs):
        parameters = [f"{k} = ?" for k in kwargs]
        parameters = ", ".join(parameters)
        values = tuple(v for v in kwargs.values())
        values += (id, )

        sql = f''' UPDATE {self.table}
                    SET {parameters}
                    WHERE id = ?'''
        try:
            cur = self.conn.cursor()
            cur.execute(sql, values)
            self.conn.commit()
            logging.info(f"Update of {self.table} done.")
        except sqlite3.OperationalError as e:
            logging.warning(e)


    def delete_where(self, **kwargs):
        qs = []
        values = tuple()
        for k, v in kwargs.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)

        sql = f'DELETE FROM {self.table} WHERE {q}'
        cur = self.conn.cursor()
        cur.execute(sql, values)
        self.conn.commit()
        return "Deleted"


    def delete_all(self):
        sql = f'DELETE FROM {self.table}'
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        return f'Table {self.table} cleared'




class Books_SQLite_Task(Books_SQLite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table = "tasks"

    def execute_sql(self):
        sql = """
        -- tasks table
        CREATE TABLE IF NOT EXISTS tasks (
            id integer PRIMARY KEY,
            book_id integer NOT NULL,
            task VARCHAR(250) NOT NULL,
            task_description TEXT,
            status VARCHAR(15) NOT NULL,
            read_date text NOT NULL,
            FOREIGN KEY (book_id) REFERENCES books (id)
            );
        """
        try:
            c = self.conn.cursor()
            c.execute(sql)
        except sqlite3.OperationalError as e:
            logging.warning(e)

    def add_task(self, task):
        sql = '''INSERT INTO tasks(book_id, task, task_description, status, read_date)
                VALUES(?,?,?,?,?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, task)
        self.conn.commit()
        return cur.lastrowid


    def select_task_by_status(self, status):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE status=?", (status,))
        rows = cur.fetchall()
        return rows





def load_books_JSON_backup(db_file=FILE_PATH):
    Books_SQLite(db_file).delete_all()
    Books_SQLite_Task(db_file).delete_all()

    for book in books:
        title = book["title"]
        description = book["description"]
        author = book["author"]
        id = book["id"]
        read = book["read"]
        book = (title, description)

        Books_SQLite(db_file).add_book(book)
            
        if read:
            task = (
                    id,
                    "Przeczytaj",
                    "done",
                    "2022-06-19 18:00:00"
                    )
        else:
            task = (
                    id,
                    "Przeczytaj",
                    "Obejrzyj odcinek",
                    "open",
                    "2022-06-19 12:00:00"
                    )
            
        Books_SQLite_Task(db_file).add_task(task)
    return "Books and tasks restored from JSON backup"




books = Books_SQLite()
tasks = Books_SQLite_Task()