from enum import Enum


class RoleNames(Enum):
    ADMIN = "Admin"
    USER = "User"
    GUEST = "Guest"


class RolePermission(Enum):
    CREATE = "Create"
    READ = "Read"
    UPDATE = "Update"
    DELETE = "Delete"


class PriorityNames(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class StatusNames(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class StatusPermission(Enum):
    CREATE = "Create"
    READ = "Read"
    UPDATE = "Update"
    DELETE = "Delete"
