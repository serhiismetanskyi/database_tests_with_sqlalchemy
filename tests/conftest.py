from typing import Any, Dict, List

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import settings
from tests.actions.priorities import PriorityActions
from tests.actions.roles import RoleActions
from tests.actions.statuses import StatusActions
from tests.actions.tasks import TaskActions
from tests.actions.users import UserActions
from tests.factories.factory_actions import (PriorityFactoryActions,
                                             RoleFactoryActions,
                                             StatusFactoryActions,
                                             TaskFactoryActions,
                                             UserFactoryActions)

DATABASE_URI: str = settings.db.uri


@pytest.fixture
def db_engine() -> create_engine:
    engine: create_engine = create_engine(DATABASE_URI)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(db_engine: create_engine) -> Session:
    session_maker: sessionmaker = sessionmaker(bind=db_engine)
    session: Session = session_maker()
    yield session
    session.close()


@pytest.fixture(autouse=True)
def clear_database(db_session):
    yield
    RoleActions(db_session).delete_all_roles()
    UserActions(db_session).delete_all_users()
    PriorityActions(db_session).delete_all_priorities()
    StatusActions(db_session).delete_all_statuses()
    TaskActions(db_session).delete_all_tasks()


@pytest.fixture
def create_superuser() -> Dict[str, Any]:
    superuser: Dict[str, Any] = UserFactoryActions.create_user(
        role_id=None, is_active=True, is_superuser=True
    )
    return superuser


@pytest.fixture
def create_role(db_session: Session) -> Dict[str, Any]:
    role: Dict[str, Any] = RoleFactoryActions.create_role()
    return role


@pytest.fixture
def create_roles() -> List[Dict[str, Any]]:
    num_roles = 3
    roles: List[Dict[str, Any]] = RoleFactoryActions.create_roles(num_roles)
    return roles


@pytest.fixture
def role_actions(db_session: Session) -> RoleActions:
    role_actions: RoleActions = RoleActions(db_session)
    return role_actions


@pytest.fixture
def create_user() -> Dict[str, Any]:
    user: Dict[str, Any] = UserFactoryActions.create_user()
    return user


@pytest.fixture
def create_users() -> List[Dict[str, Any]]:
    num_users = 3
    users: List[Dict[str, Any]] = UserFactoryActions.create_users(num_users)
    return users


@pytest.fixture
def user_actions(db_session: Session) -> UserActions:
    user_actions: UserActions = UserActions(db_session)
    return user_actions


@pytest.fixture
def create_priority() -> Dict[str, Any]:
    priority: Dict[str, Any] = PriorityFactoryActions.create_priority()
    return priority


@pytest.fixture
def create_priorities() -> List[Dict[str, Any]]:
    num_priorities = 3
    priorities: List[Dict[str, Any]] = PriorityFactoryActions.create_priorities(
        num_priorities
    )
    return priorities


@pytest.fixture
def priority_actions(db_session: Session) -> PriorityActions:
    priority_actions: PriorityActions = PriorityActions(db_session)
    return priority_actions


@pytest.fixture
def create_status() -> Dict[str, Any]:
    status: Dict[str, Any] = StatusFactoryActions.create_status()
    return status


@pytest.fixture
def create_statuses() -> List[Dict[str, Any]]:
    num_statuses = 3
    statuses: List[Dict[str, Any]] = StatusFactoryActions.create_statuses(num_statuses)
    return statuses


@pytest.fixture
def status_actions(db_session: Session) -> StatusActions:
    status_actions: StatusActions = StatusActions(db_session)
    return status_actions


@pytest.fixture
def create_task() -> Dict[str, Any]:
    task: Dict[str, Any] = TaskFactoryActions.create_task()
    return task


@pytest.fixture
def create_tasks() -> List[Dict[str, Any]]:
    num_tasks = 3
    tasks: List[Dict[str, Any]] = TaskFactoryActions.create_tasks(num_tasks)
    return tasks


@pytest.fixture
def task_actions(db_session: Session) -> TaskActions:
    task_actions: TaskActions = TaskActions(db_session)
    return task_actions
