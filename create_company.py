from django_tenants.utils import schema_context
from base.models import Company

TENANT_SCHEMA = 'testco11'

print(f"Creating Company for {TENANT_SCHEMA}...")
with schema_context(TENANT_SCHEMA):
    if not Company.objects.exists():
        Company.objects.create(
            company='Test Co 11',
            hq=True,
            address='123 Main St',
            country='USA',
            state='NY',
            city='New York',
            zip='10001'
        )
        print("Success: Company created.")
    else:
        print("Info: Company already exists.")
