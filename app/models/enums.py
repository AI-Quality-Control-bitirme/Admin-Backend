import enum


class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    COMPANY_ADMIN = "company_admin"
    HR = "hr"
    OPERATOR = "operator"
