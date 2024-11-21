import json
import random
from typing import Any, Dict, List

from factory import LazyAttribute
from faker import Faker

from src.db.enums import PriorityNames, RoleNames, StatusNames
from src.db.models import Priority, Role, Status, Task, User
from tests.factories.base import BaseFactory
from tests.factories.factory_utils import (get_current_datetime,
                                           get_updated_datetime, pwd_context,
                                           random_priority_id, random_role_id,
                                           random_status_id, random_user_id,
                                           roles_permissions,
                                           status_permissions)

fake = Faker()


class RoleFactory(BaseFactory):
    class Meta:
        model = Role

    role_name = LazyAttribute(lambda obj: random.choice(list(RoleNames)).value)
    permissions = LazyAttribute(
        lambda obj: json.dumps({"permissions": roles_permissions})
    )
    creator_id = LazyAttribute(lambda obj: random_user_id())
    created_at = LazyAttribute(lambda obj: get_current_datetime())

    @classmethod
    def role_dict(cls, **kwargs) -> Dict[str, Any]:
        role = cls.create(**kwargs)

        role_dict = {
            "role_name": role.role_name,
            "permissions": role.permissions,
            "creator_id": role.creator_id,
            "created_at": role.created_at,
        }

        return role_dict

    @classmethod
    def roles_dict(cls, count: int, **kwargs) -> List[Dict[str, Any]]:
        roles = cls.create_batch(count, **kwargs)

        roles_dicts = []
        for role in roles:
            role_dict = {
                "role_name": role.role_name,
                "permissions": role.permissions,
                "creator_id": role.creator_id,
                "created_at": role.created_at,
            }
            roles_dicts.append(role_dict)

        return roles_dicts


class UserFactory(BaseFactory):
    class Meta:
        model = User

    username = LazyAttribute(lambda obj: fake.user_name())
    full_name = LazyAttribute(lambda obj: fake.name())
    email = LazyAttribute(lambda obj: fake.email())
    hashed_password = LazyAttribute(
        lambda obj: pwd_context.hash(fake.password(length=16))
    )
    role_id = LazyAttribute(lambda obj: random_role_id())
    is_active = LazyAttribute(lambda obj: fake.boolean())
    is_superuser = LazyAttribute(lambda obj: fake.boolean())
    ipaddress = LazyAttribute(lambda obj: random.choice([fake.ipv4(), fake.ipv6()]))
    last_login_at = LazyAttribute(
        lambda obj: get_updated_datetime(days=1, hours=1, minutes=30)
    )
    updated_at = LazyAttribute(
        lambda obj: get_updated_datetime(days=2, hours=3, minutes=10)
    )
    registered_at = LazyAttribute(lambda obj: get_current_datetime())

    @classmethod
    def user_dict(cls, **kwargs) -> Dict[str, Any]:
        user = cls.create(**kwargs)

        user_dict = {
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "role_id": user.role_id,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "ipaddress": user.ipaddress,
            "last_login_at": user.last_login_at,
            "updated_at": user.updated_at,
            "registered_at": user.registered_at,
        }

        return user_dict

    @classmethod
    def users_dict(cls, count: int, **kwargs) -> List[Dict[str, Any]]:
        users = cls.create_batch(count, **kwargs)

        users_dicts = []
        for user in users:
            user_dict = {
                "username": user.username,
                "full_name": user.full_name,
                "email": user.email,
                "hashed_password": user.hashed_password,
                "role_id": user.role_id,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
                "ipaddress": user.ipaddress,
                "last_login_at": user.last_login_at,
                "updated_at": user.updated_at,
                "registered_at": user.registered_at,
            }
            users_dicts.append(user_dict)

        return users_dicts


class PriorityFactory(BaseFactory):
    class Meta:
        model = Priority

    priority_name = LazyAttribute(lambda obj: random.choice(list(PriorityNames)).value)
    creator_id = LazyAttribute(lambda obj: random_user_id())
    created_at = LazyAttribute(lambda obj: get_current_datetime())

    @classmethod
    def priority_dict(cls, **kwargs) -> Dict[str, Any]:
        priority = cls.create(**kwargs)

        priority_dict = {
            "priority_name": priority.priority_name,
            "creator_id": priority.creator_id,
            "created_at": priority.created_at,
        }

        return priority_dict

    @classmethod
    def priorities_dict(cls, count: int, **kwargs) -> List[Dict[str, Any]]:
        priorities = cls.create_batch(count, **kwargs)

        priorities_dicts = []
        for priority in priorities:
            priority_dict = {
                "priority_name": priority.priority_name,
                "creator_id": priority.creator_id,
                "created_at": priority.created_at,
            }
            priorities_dicts.append(priority_dict)

        return priorities_dicts


class StatusFactory(BaseFactory):
    class Meta:
        model = Status

    status_name = LazyAttribute(lambda obj: random.choice(list(StatusNames)).value)
    permissions = LazyAttribute(
        lambda obj: json.dumps({"permissions": status_permissions})
    )
    creator_id = LazyAttribute(lambda obj: random_user_id())
    created_at = LazyAttribute(lambda obj: get_current_datetime())

    @classmethod
    def status_dict(cls, **kwargs) -> Dict[str, Any]:
        status = cls.create(**kwargs)

        status_dict = {
            "status_name": status.status_name,
            "permissions": status.permissions,
            "creator_id": status.creator_id,
            "created_at": status.created_at,
        }

        return status_dict

    @classmethod
    def statuses_dict(cls, count: int, **kwargs) -> List[Dict[str, Any]]:
        statuses = cls.create_batch(count, **kwargs)

        statuses_dicts = []
        for status in statuses:
            status_dict = {
                "status_name": status.status_name,
                "permissions": status.permissions,
                "creator_id": status.creator_id,
                "created_at": status.created_at,
            }
            statuses_dicts.append(status_dict)

        return statuses_dicts


class TaskFactory(BaseFactory):
    class Meta:
        model = Task

    title = LazyAttribute(lambda obj: fake.text(max_nb_chars=50))
    description = LazyAttribute(lambda obj: fake.text(max_nb_chars=255))
    deadline = LazyAttribute(
        lambda obj: get_updated_datetime(days=1, hours=1, minutes=30)
    )
    priority_id = LazyAttribute(lambda obj: random_priority_id())
    status_id = LazyAttribute(lambda obj: random_status_id())
    assignee_id = LazyAttribute(lambda obj: random_user_id())
    creator_id = LazyAttribute(lambda obj: random_user_id())
    created_at = LazyAttribute(lambda obj: get_current_datetime())

    @classmethod
    def task_dict(cls, **kwargs) -> Dict[str, Any]:
        task = cls.create(**kwargs)

        task_dict = {
            "title": task.title,
            "description": task.description,
            "deadline": task.deadline,
            "priority_id": task.priority_id,
            "status_id": task.status_id,
            "assignee_id": task.assignee_id,
            "creator_id": task.creator_id,
            "created_at": task.created_at,
        }

        return task_dict

    @classmethod
    def tasks_dict(cls, count: int, **kwargs) -> List[Dict[str, Any]]:
        tasks = cls.create_batch(count, **kwargs)

        tasks_dicts = []
        for task in tasks:
            task_dict = {
                "title": task.title,
                "description": task.description,
                "deadline": task.deadline,
                "priority_id": task.priority_id,
                "status_id": task.status_id,
                "assignee_id": task.assignee_id,
                "creator_id": task.creator_id,
                "created_at": task.created_at,
            }
            tasks_dicts.append(task_dict)

        return tasks_dicts
