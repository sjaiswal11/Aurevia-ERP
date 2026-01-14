import django
from django.conf import settings
from django_tenants.utils import schema_context
from django.contrib.auth import get_user_model

def verify_access():
    User = get_user_model()
    TENANT_SCHEMA = 'testco11'
    
    with schema_context(TENANT_SCHEMA):
        print(f"Verifying Access for: {TENANT_SCHEMA}")
        users = User.objects.all().order_by('username')
        
        print(f"{'Username':<25} | {'Role':<20} | {'Staff':<5} | {'Super':<5} | {'Employee Profile'}")
        print("-" * 90)
        
        for user in users:
            is_staff = "YES" if user.is_staff else "NO"
            is_super = "YES" if user.is_superuser else "NO"
            
            try:
                emp = user.employee_get
                role = emp.employee_work_info.job_position_id.job_position if hasattr(emp, 'employee_work_info') and emp.employee_work_info.job_position_id else "No Job"
                profile_status = "OK"
            except:
                role = "N/A"
                profile_status = "MISSING"
                
            print(f"{user.username:<25} | {role:<20} | {is_staff:<5} | {is_super:<5} | {profile_status}")

            # Check specific permissions if needed
            # print(f"  - Perms: {user.get_all_permissions()}")

verify_access()
