import django
from django.conf import settings
from django_tenants.utils import schema_context
from datetime import date, datetime

def debug_attendance():
    from django.contrib.auth import get_user_model
    from employee.models import Employee, EmployeeShift
    from base.models import EmployeeShiftDay, EmployeeShiftSchedule

    User = get_user_model()
    
    with schema_context('testco11'):
        print(f"DEBUGGING ATTENDANCE FOR TENANT: testco11")
        
        # 1. Check User
        user = User.objects.filter(email='admin@testco11.com').first()
        if not user:
            print("ERROR: User 'admin@testco11.com' not found!")
            return
        print(f"User found: {user}")

        # 2. Check Employee
        try:
            employee = user.employee_get
            print(f"Employee found: {employee}")
        except Exception as e:
            print(f"ERROR: Employee profile not found for user! {e}")
            return

        # 3. Check EmployeeWorkInfo
        try:
            work_info = employee.employee_work_info
            print(f"EmployeeWorkInfo found: {work_info}")
        except Exception as e:
            print(f"ERROR: EmployeeWorkInfo not found for employee! {e}")
            # Try to see if we can access it via related name or query
            return

        # 4. Check Shift
        shift = work_info.shift_id
        if not shift:
            print("ERROR: No Shift assigned to Employee in EmployeeWorkInfo!")
        else:
            print(f"Shift assigned: {shift}")

            # 5. Check Schedule for Today
            today_day = date.today().strftime("%A").lower()
            print(f"Checking schedule for today ({today_day})...")
            
            try:
                day_obj = EmployeeShiftDay.objects.get(day=today_day)
                schedule = EmployeeShiftSchedule.objects.filter(shift_id=shift, day=day_obj).first()
                if schedule:
                    print(f"Schedule found: Start {schedule.start_time}, End {schedule.end_time}")
                else:
                    print(f"ERROR: No schedule found for {today_day} in shift {shift}")
            except Exception as e:
                print(f"ERROR checking schedule: {e}")

        # 6. Check Active Shifts in DB
        print("\n--- Available Shifts in DB ---")
        shifts = EmployeeShift.objects.all()
        for s in shifts:
            print(f"- {s}")

debug_attendance()
