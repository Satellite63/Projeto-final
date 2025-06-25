from django.db import connection

def execute_sql(query, params=None, fetchone=False):
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        if fetchone:
            return cursor.fetchone()
        return cursor.fetchall()