from customers.models import Feature
from horilla.horilla_apps import SIDEBARS

print("Seeding Features...")
for app_code in SIDEBARS:
    feature, created = Feature.objects.get_or_create(
        code=app_code,
        defaults={'name': app_code.replace('_', ' ').title()}
    )
    if created:
        print(f"Created feature: {feature}")
    else:
        print(f"Feature already exists: {feature}")

print("Done.")
