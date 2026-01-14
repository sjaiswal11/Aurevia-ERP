from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Feature(models.Model):
    name = models.CharField(max_length=100)
    code = models.SlugField(unique=True, help_text="Module name e.g., 'leave', 'payroll'")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Plan(models.Model):
    name = models.CharField(max_length=100)
    features = models.ManyToManyField(Feature, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)
    
    # Feature Management
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    custom_features = models.ManyToManyField(Feature, blank=True, help_text="Additional features specifically for this client")

    # Default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def get_enabled_modules(self):
        """
        Returns a set of feature codes enabled for this client.
        Combines plan features and custom features.
        """
        modules = set()
        if self.plan:
            modules.update(self.plan.features.values_list('code', flat=True))
        
        modules.update(self.custom_features.values_list('code', flat=True))
        return modules

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    def __str__(self):
        return self.domain

from django.contrib.auth.models import User
# User patch moved to base/models.py
