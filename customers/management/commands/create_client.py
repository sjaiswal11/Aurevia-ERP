from django.core.management.base import BaseCommand, CommandError
from django_tenants.utils import schema_context
from customers.models import Client, Domain
from django.contrib.auth.models import User
from employee.models import Employee
import uuid

class Command(BaseCommand):
    help = 'Create a new client/tenant with domain and admin user'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, required=True, help='Client Name (e.g. "Acme Corp")')
        parser.add_argument('--schema', type=str, required=True, help='Schema Name (e.g. "acme")')
        parser.add_argument('--domain', type=str, required=True, help='Domain (e.g. "acme.localhost")')
        parser.add_argument('--email', type=str, required=True, help='Admin Email')
        parser.add_argument('--password', type=str, required=False, help='Admin Password (default: admin123)')

    def handle(self, *args, **options):
        name = options['name']
        schema_name = options['schema']
        domain_url = options['domain']
        email = options['email']
        email = options['email']
        password = options['password'] or "admin123"
        
        
        from django.db import transaction

        try:
            with transaction.atomic():
                # 1. Create Tenant (Client)
                if Client.objects.filter(schema_name=schema_name).exists():
                    self.stdout.write(self.style.WARNING(f'Tenant with schema "{schema_name}" already exists.'))
                    # We continue here to allow adding domain/user to existing tenant if needed, 
                    # but logic below assumes new tenant. 
                    # For atomic safety, let's fetch it.
                    client = Client.objects.get(schema_name=schema_name)
                else:
                    self.stdout.write(f"Creating tenant '{name}' with schema '{schema_name}'...")
                    client = Client(schema_name=schema_name, name=name, on_trial=True)
                    client.save()  # This triggers schema creation and migrations

                # 2. Create Domain
                if not Domain.objects.filter(domain=domain_url).exists():
                    self.stdout.write(f"Creating domain '{domain_url}'...")
                    domain = Domain()
                    domain.domain = domain_url
                    domain.tenant = client
                    domain.is_primary = True
                    domain.save()
                else:
                     self.stdout.write(self.style.WARNING(f"Domain '{domain_url}' already exists."))

        except Exception as e:
            raise CommandError(f"Error creating tenant/domain: {e}")

        # 3. Create Admin User within Tenant Schema (Outside atomic block for public schema)
        self.stdout.write(f"Creating admin user '{email}' in schema '{schema_name}'...")
        with schema_context(schema_name):
            try:
                if not User.objects.filter(email=email).exists():
                    # Create Superuser
                    user = User.objects.create_superuser(
                        username=email,
                        email=email,
                        password=password
                    )
                    
                    # Create Employee Profile (Required for Horilla login)
                    employee = Employee()
                    employee.employee_user_id = user
                    employee.employee_first_name = "Admin"
                    employee.employee_last_name = "User"
                    employee.email = email
                    employee.save()
                    
                    self.stdout.write(self.style.SUCCESS(f"Successfully created client '{name}'"))
                    self.stdout.write(self.style.SUCCESS(f"URL: http://{domain_url}:8000"))
                    self.stdout.write(self.style.SUCCESS(f"Login: {email} / {password}"))
                else:
                    self.stdout.write(self.style.WARNING(f"User '{email}' already exists in tenant."))
                
                # Create Default Company (Required for most apps)
                from base.models import Company
                if not Company.objects.exists():
                     Company.objects.create(
                         company=name,
                         hq=True,
                         address="Default Address",
                         country="US",
                         state="State",
                         city="City",
                         zip="00000"
                     )
                     self.stdout.write(self.style.SUCCESS(f"Created default company '{name}'"))

            except Exception as e:
                raise CommandError(f"Error creating user/company: {e}")
