import django
from django.conf import settings
from django_tenants.utils import schema_context
from datetime import time

def seed_attendance():
    from base.models import Company, EmployeeShift, EmployeeShiftDay, EmployeeShiftSchedule
    from employee.models import Employee, EmployeeWorkInformation
    from django.contrib.auth import get_user_model

    User = get_user_model()
    
    TENANT_SCHEMA = 'testco11'

    with schema_context(TENANT_SCHEMA):
        print(f"Seeding Attendance Data for: {TENANT_SCHEMA}")
        
        # 1. Get Company
        company = Company.objects.first()
        if not company:
            print("ERROR: Company not found. Run create_company.py first.")
            return
        
        # 2. Create/Get Shift
        shift_name = "Regular Shift"
        shift, created = EmployeeShift.objects.get_or_create(
            employee_shift=shift_name,
            defaults={
                'weekly_full_time': '40:00',
                'full_time': '160:00'
            }
        )
        shift.company_id.add(company)
        if created:
            print(f"Created Shift: {shift}")
        else:
            print(f"Found Shift: {shift}")

        # 3. Ensure Days and Schedules
        days_map = {
            'monday': 'Monday',
            'tuesday': 'Tuesday',
            'wednesday': 'Wednesday',
            'thursday': 'Thursday',
            'friday': 'Friday'
        }

        for day_code, day_label in days_map.items():
            # Get/Create Day
            day_obj, _ = EmployeeShiftDay.objects.get_or_create(day=day_code)
            day_obj.company_id.add(company)
            
            # Create Schedule
            schedule, sched_created = EmployeeShiftSchedule.objects.get_or_create(
                shift_id=shift,
                day=day_obj,
                defaults={
                    'start_time': time(9, 0),
                    'end_time': time(18, 0),
                    'minimum_working_hour': '08:00',
                    'is_night_shift': False
                }
            )
            if sched_created:
                print(f"Created Schedule for {day_label}")

        # 4. Assign Shift to Admin
        user = User.objects.filter(email='admin@testco11.com').first()
        if user and hasattr(user, 'employee_get'):
            employee = user.employee_get
            work_info, _ = EmployeeWorkInformation.objects.get_or_create(employee_id=employee)
            
            work_info.shift_id = shift
            work_info.company_id = company # Also ensure company is set
            work_info.save()
            print(f"Assigned '{shift}' to {employee}")
        else:
            print("ERROR: Admin user or employee profile not found.")

seed_attendance()
