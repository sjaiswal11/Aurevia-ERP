from django_tenants.utils import schema_context
from base.models import Company, JobPosition
from recruitment.models import Recruitment
from datetime import date

TENANT_SCHEMA = 'testco11'

print(f"Seeding Recruitment for {TENANT_SCHEMA}...")
with schema_context(TENANT_SCHEMA):
    company = Company.objects.first()
    job_position = JobPosition.objects.filter(job_position="HR Manager").first()
    
    if company and job_position:
        recruitment, created = Recruitment.objects.get_or_create(
            title="Hiring HR Manager",
            defaults={
                'job_position_id': job_position,
                'company_id': company,
                'vacancy': 1,
                'is_published': True,
                'start_date': date.today(),
                'optional_resume': True,
                'optional_profile_image': True
            }
        )
        if created:
             # Link the job position to open_positions M2M field
             recruitment.open_positions.add(job_position)
             print(f"Created Recruitment: {recruitment.title}")
        else:
             print(f"Recruitment already exists: {recruitment.title}")
            
        print("Done seeding recruitment.")
    else:
        print("Error: Company or Job Position not found. Run seed_hr.py first.")
