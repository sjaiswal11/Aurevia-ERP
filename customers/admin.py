from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from customers.models import Client, Domain, Feature, Plan

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")
    prepopulated_fields = {"code": ("name",)}

class FeatureInline(admin.TabularInline):
    model = Plan.features.through
    extra = 1

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "get_features_count")
    search_fields = ("name",)
    filter_horizontal = ("features",)
    
    def get_features_count(self, obj):
        return obj.features.count()
    get_features_count.short_description = "Features"

@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("name", "schema_name", "plan", "on_trial", "paid_until", "created_on")
    list_filter = ("on_trial", "plan")
    search_fields = ("name", "schema_name")
    filter_horizontal = ("custom_features",)
    fieldsets = (
        (None, {"fields": ("name", "schema_name")}),
        ("Plan & Features", {"fields": ("plan", "custom_features")}),
        ("Status", {"fields": ("on_trial", "paid_until")}),
    )
    
    # Note: TenantAdminMixin might conflict with fieldsets if not careful, 
    # but usually it's fine for simple tenants. 
    # Let's keep it simple for now, sticking closer to standard ModelAdmin for the mixin compatibility.
    # Actually, removing fieldsets to avoid messing up TenantMixin's internal logic for now.
    filter_horizontal = ("custom_features",)

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("domain", "tenant", "is_primary")
    list_filter = ("is_primary",)
    search_fields = ("domain", "tenant__name")
