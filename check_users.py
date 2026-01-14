import django
from django.conf import settings
from django.db import connection

def check_users():
    with connection.cursor() as cursor:
        # Check Public Users
        cursor.execute("SELECT id, username FROM public.auth_user;")
        public_users = cursor.fetchall()
        print(f"\n--- Public Auth Users ({len(public_users)}) ---")
        for u in public_users:
            print(u)
            
        # Check Tenant Users
        tenant_schema = 'testco11'
        try:
            cursor.execute(f"SELECT id, username FROM {tenant_schema}.auth_user;")
            tenant_users = cursor.fetchall()
            print(f"\n--- Tenant {tenant_schema} Auth Users ({len(tenant_users)}) ---")
            for u in tenant_users:
                print(u)
        except Exception as e:
            print(f"Tenant auth_user query failed: {e}")

check_users()
