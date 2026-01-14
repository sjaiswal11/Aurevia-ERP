"""
horilla_apps

This module is used to register horilla addons
"""

from horilla import settings
from horilla.settings import INSTALLED_APPS

if "accessibility" not in INSTALLED_APPS:
    INSTALLED_APPS.append("accessibility")
if "horilla_audit" not in INSTALLED_APPS:
    INSTALLED_APPS.append("horilla_audit")
if "horilla_widgets" not in INSTALLED_APPS:
    INSTALLED_APPS.append("horilla_widgets")
if "horilla_crumbs" not in INSTALLED_APPS:
    INSTALLED_APPS.append("horilla_crumbs")
if "horilla_documents" not in INSTALLED_APPS:
    INSTALLED_APPS.append("horilla_documents")
if "horilla_views" not in INSTALLED_APPS:
    INSTALLED_APPS.append("horilla_views")
if "horilla_automations" not in INSTALLED_APPS:
    INSTALLED_APPS.append("horilla_automations")

if "biometric" not in INSTALLED_APPS:
    INSTALLED_APPS.append("biometric")
if "helpdesk" not in INSTALLED_APPS:
    INSTALLED_APPS.append("helpdesk")
if "offboarding" not in INSTALLED_APPS:
    INSTALLED_APPS.append("offboarding")
if "horilla_backup" not in INSTALLED_APPS:
    INSTALLED_APPS.append("horilla_backup")
if "project" not in INSTALLED_APPS:
    INSTALLED_APPS.append("project")
if settings.env("AWS_ACCESS_KEY_ID", default=None) and "storages" not in INSTALLED_APPS:
    INSTALLED_APPS.append("storages")


AUDITLOG_INCLUDE_ALL_MODELS = True

AUDITLOG_EXCLUDE_TRACKING_MODELS = (
    # "<app_name>",
    # "<app_name>.<model>"
)

setattr(settings, "AUDITLOG_INCLUDE_ALL_MODELS", AUDITLOG_INCLUDE_ALL_MODELS)
setattr(settings, "AUDITLOG_EXCLUDE_TRACKING_MODELS", AUDITLOG_EXCLUDE_TRACKING_MODELS)

settings.MIDDLEWARE.append(
    "auditlog.middleware.AuditlogMiddleware",
)

SETTINGS_EMAIL_BACKEND = getattr(settings, "EMAIL_BACKEND", False)
setattr(settings, "EMAIL_BACKEND", "base.backends.ConfiguredEmailBackend")
if SETTINGS_EMAIL_BACKEND:
    setattr(settings, "EMAIL_BACKEND", SETTINGS_EMAIL_BACKEND)


SIDEBARS = [
    "recruitment",
    "onboarding",
    "employee",
    "attendance",
    "leave",
    "payroll",
    "pms",
    "offboarding",
    "asset",
    "helpdesk",
    "project",
]

WHITE_LABELLING = False
NESTED_SUBORDINATE_VISIBILITY = False
TWO_FACTORS_AUTHENTICATION = False
