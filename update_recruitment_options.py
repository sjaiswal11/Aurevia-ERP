from django_tenants.utils import schema_context
from recruitment.models import Recruitment

TENANT_SCHEMA = 'testco11'

print(f"Updating Recruitment Options for {TENANT_SCHEMA}...")
with schema_context(TENANT_SCHEMA):
    recruitments = Recruitment.objects.all()
    updated_count = 0
    for r in recruitments:
        r.optional_resume = True
        r.optional_profile_image = True
        r.save()
        print(f"Updated '{r.title}': optional_resume=True, optional_profile_image=True")
        updated_count += 1
    
    if updated_count == 0:
        print("No recruitments found to update.")
