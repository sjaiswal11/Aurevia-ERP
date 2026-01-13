from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT to_regclass('auditlog_logentry');")
    res = cursor.fetchone()
    print(f'Table exists: {res[0]}')
