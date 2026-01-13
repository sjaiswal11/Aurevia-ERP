from django.core.management.base import BaseCommand
from customers.models import Client, Domain

class Command(BaseCommand):
    help = 'Initialize Public and Demo tenants'

    def handle(self, *args, **kwargs):
        # Public Tenant
        if not Client.objects.filter(schema_name='public').exists():
            public = Client(schema_name='public', name='Aurevia Public')
            public.save()
            domain = Domain()
            domain.domain = 'localhost' # or your production domain
            domain.tenant = public
            domain.is_primary = True
            domain.save()
            self.stdout.write(self.style.SUCCESS('Successfully created Public tenant'))
        else:
            self.stdout.write('Public tenant already exists')

        # Demo Tenant
        if not Client.objects.filter(schema_name='demo').exists():
            demo = Client(schema_name='demo', name='Demo Company', on_trial=True)
            demo.save()
            domain = Domain()
            domain.domain = 'demo.localhost'
            domain.tenant = demo
            domain.is_primary = True
            domain.save()
            self.stdout.write(self.style.SUCCESS('Successfully created Demo tenant'))
        else:
            self.stdout.write('Demo tenant already exists')
