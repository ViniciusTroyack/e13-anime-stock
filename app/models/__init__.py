import os
import psycopg2

configs = {
    "host": os.environ.get("HOST"),
    "database": os.environ.get("DB"),
    "user": os.environ.get("USER"),
    "password": os.environ.get("PASS"),
}


def conn_cur():
    conn = psycopg2.connect(**configs)
    cur = conn.cursor()

    return conn, cur


def commit_and_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()
