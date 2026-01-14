from django_tenants.utils import schema_context
from base.models import Company, Department, JobPosition

TENANT_SCHEMA = 'testco11'

print(f"Seeding HR Data for {TENANT_SCHEMA}...")
with schema_context(TENANT_SCHEMA):
    company = Company.objects.first()
    if company:
        dept, created_dept = Department.objects.get_or_create(
            department="Human Resources"
        )
        if created_dept:
             dept.company_id.add(company)
             print("Created Department: Human Resources")
        
        job, created_job = JobPosition.objects.get_or_create(
            job_position="HR Manager",
            department_id=dept
        )
        if created_job:
            job.company_id.add(company)
            print("Created Job Position: HR Manager")
            
        print("Done seeding.")
    else:
        print("Error: Company not found.")
