import django
from django.conf import settings
from django_tenants.utils import schema_context
from datetime import date
from django.contrib.auth.models import User, Permission
import random

def seed_employees():
    from base.models import Company, Department, JobPosition, EmployeeShift, EmployeeType
    from employee.models import Employee, EmployeeWorkInformation
    
    from django.db import connection

    TENANT_SCHEMA = 'testco11'
    
    with schema_context(TENANT_SCHEMA):
        print(f"Seeding Employees for: {TENANT_SCHEMA}")
        
        # --- CLEANUP START ---
        # 1. Drop Tenant Auth User Table if exists (fix mismatch)
        # using CASCADE to remove bad constraints on Employee table
        with connection.cursor() as cursor:
            # 1. Drop Tenant Auth User (fix mismatch)
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {TENANT_SCHEMA}.auth_user CASCADE;")
                print("Dropped tenant auth_user table.")
            except Exception as e:
                print(f"Error dropping auth_user: {e}")

            # 2. Raw Delete Employees and WorkInfo (avoid ORM accessing missing users)
            # Order matters due to constraints (though CASCADE handles it, we want to be sure)
            try:
                cursor.execute(f"TRUNCATE TABLE {TENANT_SCHEMA}.employee_employeeworkinformation CASCADE;")
                cursor.execute(f"TRUNCATE TABLE {TENANT_SCHEMA}.employee_employee CASCADE;")
                print("Truncated employee tables via Raw SQL.")
            except Exception as e:
                print(f"Error truncating tables: {e}")
                # Fallback to delete if truncate checks FKs too strictly (it does)
                # But here we want to wipe them.
                cursor.execute(f"DELETE FROM {TENANT_SCHEMA}.employee_employeeworkinformation;")
                cursor.execute(f"DELETE FROM {TENANT_SCHEMA}.employee_employee;")
        
        # We don't use ORM delete here because it tries to load instances and fails on missing User

        
        # Reset Admin Employee?
        # We need to recreate Admin Employee since we deleted it
        # --- CLEANUP END ---
        
        company = Company.objects.first()
        if not company:
            print("Company not found!")
            return

        shift = EmployeeShift.objects.first()
        if not shift:
            print("Shift not found! Run seed_attendance.py first.")
            return

        # 1. Create/Get Employee Type
        emp_type, _ = EmployeeType.objects.get_or_create(employee_type="Permanent")
        emp_type.company_id.add(company)

        # 2. Define Departments and Job Positions
        structure = {
            "Human Resources": ["HR Manager", "Recruiter"],
            "Engineering": ["Engineering Manager", "Senior Developer", "Junior Developer", "DevOps Engineer"],
            "Sales": ["Sales Manager", "Sales Associate"],
            "Marketing": ["Marketing Lead", "Content Creator"]
        }
        
        dept_objs = {}
        role_objs = {}

        for dept_name, roles in structure.items():
            dept, created = Department.objects.get_or_create(department=dept_name)
            if created:
                dept.company_id.add(company)
            dept_objs[dept_name] = dept
            print(f"Department: {dept}")
            
            for role in roles:
                jp, created = JobPosition.objects.get_or_create(job_position=role, defaults={'department_id': dept})
                if created:
                    jp.company_id.add(company)
                role_objs[role] = jp
                print(f"  Role: {jp}")

        # 3. Define Employees to Seed
        # Format: (First, Last, Email, Phone, Dept, Role, IsAdmin/HR)
        employees_data = [
            ("Alice", "HR", "alice.hr@testco11.com", "9000000001", "Human Resources", "HR Manager", True),
            ("Bob", "Engineer", "bob.eng@testco11.com", "9000000002", "Engineering", "Engineering Manager", False),
            ("Charlie", "Dev", "charlie.dev@testco11.com", "9000000003", "Engineering", "Senior Developer", False),
            ("David", "Junior", "david.jr@testco11.com", "9000000004", "Engineering", "Junior Developer", False),
            ("Eve", "Ops", "eve.ops@testco11.com", "9000000005", "Engineering", "DevOps Engineer", False),
            ("Frank", "Sales", "frank.sales@testco11.com", "9000000006", "Sales", "Sales Manager", False),
            ("Grace", "Sell", "grace.sell@testco11.com", "9000000007", "Sales", "Sales Associate", False),
            ("Heidi", "Market", "heidi.mkt@testco11.com", "9000000008", "Marketing", "Marketing Lead", False),
            ("Ivan", "Content", "ivan.content@testco11.com", "9000000009", "Marketing", "Content Creator", False),
            ("Judy", "Recruit", "judy.rec@testco11.com", "9000000010", "Human Resources", "Recruiter", False),
            ("Admin", "User", "admin@testco11.com", "9000000000", "Human Resources", "HR Manager", True), # Re-create Admin
        ]

        # 4. Create Employees
        for first, last, email, phone, dept_name, role_name, is_hr_admin in employees_data:
            # Create User
            username = email
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password="password123")
                if is_hr_admin:
                    user.is_staff = True # Give HR Manager access to admin site/modules
                    user.is_superuser = True # For "All Access"
                    user.save()
                print(f"Created User: {username}")
            else:
                user = User.objects.get(username=username)
                print(f"User exists: {username}")

            # Create Employee Profile
            emp, created = Employee.objects.get_or_create(
                email=email,
                defaults={
                    'employee_first_name': first,
                    'employee_last_name': last,
                    'phone': phone,
                    'gender': 'male', # Simplifying
                    'employee_user_id': user,
                    'is_active': True
                }
            )
            
            # Ensure Link
            if not emp.employee_user_id:
                emp.employee_user_id = user
                emp.save()

            # Work Info
            work_info, _ = EmployeeWorkInformation.objects.get_or_create(employee_id=emp)
            work_info.company_id = company
            work_info.department_id = dept_objs[dept_name]
            work_info.job_position_id = role_objs[role_name]
            work_info.shift_id = shift
            work_info.employee_type_id = emp_type
            work_info.save()
            
            print(f"Seeded Employee: {first} {last} - {role_name}")

seed_employees()
