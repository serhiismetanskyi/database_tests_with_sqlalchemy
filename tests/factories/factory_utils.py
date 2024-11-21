import random
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from passlib.context import CryptContext

from src.db.db import session
from src.db.enums import RolePermission, StatusPermission
from tests.actions.priorities import PriorityActions
from tests.actions.roles import RoleActions
from tests.actions.statuses import StatusActions
from tests.actions.tasks import TaskActions
from tests.actions.users import UserActions

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

num_permissions = random.randint(1, 4)
roles_permissions = [
    random.choice(list(RolePermission)).value for _ in range(num_permissions)
]
status_permissions = [
    random.choice(list(StatusPermission)).value for _ in range(num_permissions)
]


def random_role_id() -> int:
    random_role = RoleActions(session).get_random_role()
    if "id" in random_role:
        role_id = random_role["id"]
        return role_id
    else:
        raise ValueError("Role ID not found in the random_role dictionary")


def random_user_id() -> int:
    random_user = UserActions(session).get_random_user()
    if "id" in random_user:
        user_id = random_user["id"]
        return user_id
    else:
        raise ValueError("User ID not found in the random_user dictionary")


def random_priority_id() -> int:
    random_priority = PriorityActions(session).get_random_priority()
    if "id" in random_priority:
        priority_id = random_priority["id"]
        return priority_id
    else:
        raise ValueError("Priority ID not found in the random_priority dictionary")


def random_status_id() -> int:
    random_status = StatusActions(session).get_random_status()
    if "id" in random_status:
        status_id = random_status["id"]
        return status_id
    else:
        raise ValueError("Status ID not found in the random_status dictionary")


def get_random_task() -> Optional[Dict[str, Any]]:
    random_task = TaskActions(session).get_random_task()
    return random_task


def get_random_user() -> Optional[Dict[str, Any]]:
    while True:
        random_user = UserActions(session).get_random_user()
        if random_user and random_user.get("role_id") is not None:
            return random_user


def get_current_datetime() -> str:
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
    return formatted_datetime


def get_updated_datetime(days: int = 3, hours: int = 2, minutes: int = 10) -> str:
    current_datetime = datetime.now()
    updated_datetime = current_datetime + timedelta(
        days=days, hours=hours, minutes=minutes
    )
    formatted_updated_datetime = updated_datetime.strftime("%Y-%m-%d %H:%M")
    return formatted_updated_datetime


def get_formatted_datetime(date_time) -> str:
    formatted_datetime = date_time.strftime("%Y-%m-%d %H:%M")
    return formatted_datetime
