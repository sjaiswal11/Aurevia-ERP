import django
from django.conf import settings
from django.db import connection

def check_audit_schema():
    with connection.cursor() as cursor:
        # Check public schema
        cursor.execute("SELECT to_regclass('public.auditlog_logentry');")
        public_exists = cursor.fetchone()[0]
        print(f"Public auditlog_logentry exists: {public_exists}")

        # Check tenant schema
        tenant_schema = 'testco11'
        cursor.execute(f"SELECT to_regclass('{tenant_schema}.auditlog_logentry');")
        tenant_exists = cursor.fetchone()[0]
        print(f"Tenant '{tenant_schema}' auditlog_logentry exists: {tenant_exists}")
        
        # Check auth_user in tenant
        cursor.execute(f"SELECT to_regclass('{tenant_schema}.auth_user');")
        tenant_auth_user = cursor.fetchone()[0]
        print(f"Tenant '{tenant_schema}' auth_user exists: {tenant_auth_user}")
        
        # Check if Constraint exists in Tenant
        if tenant_exists:
            cursor.execute(f"""
                SELECT conname, confrelid::regclass 
                FROM pg_constraint 
                WHERE conrelid = '{tenant_schema}.auditlog_logentry'::regclass
                AND conname LIKE '%fk_auth_user_id%';
            """)
            constraints = cursor.fetchall()
            print(f"Constraints on {tenant_schema}.auditlog_logentry: {constraints}")

check_audit_schema()
