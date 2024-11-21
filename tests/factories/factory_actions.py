from typing import Any, Dict, List

from src.logger.logger import logger
from tests.factories.factories import (PriorityFactory, RoleFactory,
                                       StatusFactory, TaskFactory, UserFactory)


class RoleFactoryActions:
    @classmethod
    def create_role(cls) -> Dict[str, Any]:
        role = RoleFactory.role_dict()
        logger.info("Created Role: %s", role)
        return role

    @classmethod
    def create_roles(cls, num_roles: int) -> List[Dict[str, Any]]:
        roles = RoleFactory.roles_dict(num_roles)
        logger.info("Created %d roles using %s", num_roles, cls.__name__)
        return roles


class UserFactoryActions:
    @classmethod
    def create_user(cls, **kwargs) -> Dict[str, Any]:
        user = UserFactory.user_dict(**kwargs)
        logger.info("Created User: %s", user)
        return user

    @classmethod
    def create_users(cls, num_users: int) -> List[Dict[str, Any]]:
        users = UserFactory.users_dict(num_users)
        logger.info("Created %d users using %s", num_users, cls.__name__)
        return users


class PriorityFactoryActions:
    @classmethod
    def create_priority(cls, **kwargs) -> Dict[str, Any]:
        priority = PriorityFactory.priority_dict(**kwargs)
        logger.info("Created Priority: %s", priority)
        return priority

    @classmethod
    def create_priorities(cls, num_priorities: int) -> List[Dict[str, Any]]:
        priorities = PriorityFactory.priorities_dict(num_priorities)
        logger.info("Created %d priorities using %s", num_priorities, cls.__name__)
        return priorities


class StatusFactoryActions:
    @classmethod
    def create_status(cls, **kwargs) -> Dict[str, Any]:
        status = StatusFactory.status_dict(**kwargs)
        logger.info("Created Status: %s", status)
        return status

    @classmethod
    def create_statuses(cls, num_statuses: int) -> List[Dict[str, Any]]:
        statuses = StatusFactory.statuses_dict(num_statuses)
        logger.info("Created %d statuses using %s", num_statuses, cls.__name__)
        return statuses


class TaskFactoryActions:
    @classmethod
    def create_task(cls, **kwargs) -> Dict[str, Any]:
        task = TaskFactory.task_dict(**kwargs)
        logger.info("Created Task: %s", task)
        return task

    @classmethod
    def create_tasks(cls, num_tasks: int) -> List[Dict[str, Any]]:
        tasks = TaskFactory.tasks_dict(num_tasks)
        logger.info("Created %d tasks using %s", num_tasks, cls.__name__)
        return tasks
