"""
WWWizards Telegram Bot - Enums and Constants
"""
from enum import Enum


class LeadStatus(str, Enum):
    """Lead status enumeration."""
    NEW = "new"
    CONTACTED = "contacted"
    IN_PROGRESS = "in_progress"
    QUOTED = "quoted"
    CONVERTED = "converted"
    LOST = "lost"


class ServiceType(str, Enum):
    """Service type enumeration."""
    CORPORATE = "corporate"
    LANDING = "landing"
    SHOP = "shop"
    CATALOG = "catalog"
    REDESIGN = "redesign"
    SUPPORT = "support"


class BudgetRange(str, Enum):
    """Budget range enumeration."""
    UNDER_100K = "under_100k"
    BETWEEN_100K_300K = "between_100k_300k"
    BETWEEN_300K_500K = "between_300k_500k"
    BETWEEN_500K_1M = "between_500k_1m"
    OVER_1M = "over_1m"


class Timeline(str, Enum):
    """Project timeline enumeration."""
    WITHIN_MONTH = "within_month"
    ONE_TO_TWO_MONTHS = "one_to_two_months"
    TWO_TO_THREE_MONTHS = "two_to_three_months"
    THREE_TO_SIX_MONTHS = "three_to_six_months"
    NO_RUSH = "no_rush"


class NotificationType(str, Enum):
    """Notification type enumeration."""
    NEW_LEAD = "new_lead"
    CONTACT_REQUEST = "contact_request"
    SYSTEM_ALERT = "system_alert"


class StorageType(str, Enum):
    """Storage type enumeration."""
    GOOGLE_SHEETS = "google_sheets"
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"

