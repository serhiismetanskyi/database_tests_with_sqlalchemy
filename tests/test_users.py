import pytest

from src.logger.logger import logger
from tests.factories.factories import fake
from tests.factories.factory_utils import get_current_datetime, get_random_user


class TestUsers:
    @pytest.mark.usefixtures("create_superuser", "create_role")
    def test_get_user_by_username(self, create_user, user_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_user_by_username"
        logger.info(f"[users_tests] :: Running test case: {test_case_name}")

        expected_username = create_user["username"]

        result_user = user_actions.get_user_by_username(filter_value=expected_username)
        if result_user is not None:
            logger.info(f"{test_case_name} :: Found user by username: {result_user}")
        else:
            logger.info(
                f"{test_case_name} :: User not found by username: {expected_username}"
            )

        assert (
            result_user is not None
        ), f"{test_case_name} :: User not found by username"

        actual_username = result_user["username"]
        assert (
            actual_username == expected_username
        ), f"{test_case_name} :: The username received does not match expectations"

    @pytest.mark.usefixtures("create_superuser", "create_role")
    def test_get_user_full_name_field(self, create_user, user_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_user_full_name_field"
        logger.info(f"[users_tests] :: Running test case: {test_case_name}")

        username = create_user["username"]
        expected_full_name = create_user["full_name"]

        actual_full_name = user_actions.get_user_field(
            filter_param="username",
            filter_value=username,
            field_name="full_name",
        )
        if actual_full_name is not None:
            logger.info(
                f"{test_case_name} :: User full name received: {actual_full_name}"
            )
        else:
            logger.info(
                f"{test_case_name} :: User not found by username: {expected_full_name}"
            )

        assert (
            actual_full_name is not None
        ), f"{test_case_name} :: User not found by username"
        assert (
            actual_full_name == expected_full_name
        ), f"{test_case_name} :: The full name received does not match expectations"

    @pytest.mark.usefixtures("create_superuser", "create_roles", "create_users")
    def test_get_all_users_registered_today(self, user_actions):
        test_case_name = (
            f"{self.__class__.__name__}.test_get_all_users_registered_today"
        )
        logger.info(f"[users_tests] :: Running test case: {test_case_name}")

        current_datetime = get_current_datetime()
        all_users_today = user_actions.get_all_users_by_filter(
            filter_param="registered_at", filter_value=current_datetime
        )

        if all_users_today:
            logger.info(
                f"{test_case_name} :: Found users created today: {all_users_today}"
            )
        else:
            logger.info(f"{test_case_name} :: Users created today not found")

        assert all_users_today, f"{test_case_name} :: Users created today not found"

    @pytest.mark.usefixtures("create_superuser", "create_role")
    def test_update_username_field(self, create_user, user_actions):
        test_case_name = f"{self.__class__.__name__}.test_update_username_field"
        logger.info(f"[users_tests] :: Running test case: {test_case_name}")

        username = create_user["username"]

        result_user = user_actions.get_user_by_filter(
            filter_param="username", filter_value=username
        )
        if result_user is not None:
            logger.info(f"{test_case_name} :: Found user by username: {result_user}")
        else:
            logger.info(f"{test_case_name} :: User not found by username: {username}")

        user_id = result_user["id"]

        new_username = fake.user_name()
        user_actions.update_user_field(
            filter_param="id",
            filter_value=user_id,
            field_name="username",
            new_value=new_username,
        )
        logger.info(f"{test_case_name} :: Updated user with ID: {user_id}")

        updated_user = user_actions.get_user_by_filter(
            filter_param="username", filter_value=new_username
        )
        if updated_user is not None:
            logger.info(f"{test_case_name} :: User found after update: {updated_user}")
        else:
            logger.info(f"{test_case_name} :: User not found after update")

        assert (
            updated_user["username"] == new_username
        ), f"{test_case_name} :: The user was not updated"

    @pytest.mark.usefixtures("create_superuser", "create_role")
    def test_update_user_fields(self, create_user, user_actions):
        test_case_name = f"{self.__class__.__name__}.test_update_user_fields"
        logger.info(f"[users_tests] :: Running test case: {test_case_name}")

        username = create_user["username"]

        result_user = user_actions.get_user_by_filter(
            filter_param="username", filter_value=username
        )
        if result_user is not None:
            logger.info(f"{test_case_name} :: Found user by username: {result_user}")
        else:
            logger.info(f"{test_case_name} :: User not found by username: {username}")

        user_id = result_user["id"]

        new_data = {"is_active": False, "is_superuser": False}
        user_actions.update_user_fields(
            filter_param="id", filter_value=user_id, updated_data=new_data
        )
        logger.info(f"{test_case_name} :: Updated user with ID: {user_id}")

        updated_user = user_actions.get_user_by_id(filter_value=user_id)

        if updated_user is not None:
            logger.info(f"{test_case_name} :: User found after update: {updated_user}")
        else:
            logger.info(f"{test_case_name} :: User not found after update")

        assert updated_user is not None, f"{test_case_name} :: The user was not updated"

        assert (
            updated_user["is_active"] == new_data["is_active"]
        ), f"{test_case_name} :: is_active field not updated correctly"

        assert (
            updated_user["is_superuser"] == new_data["is_superuser"]
        ), f"{test_case_name} :: is_superuser field not updated correctly"

    @pytest.mark.usefixtures("create_superuser", "create_role")
    def test_delete_user(self, create_user, user_actions):
        test_case_name = f"{self.__class__.__name__}.test_delete_user"
        logger.info(f"[users_tests] :: Running test case: {test_case_name}")

        username = create_user["username"]

        result_user = user_actions.get_user_by_filter(
            filter_param="username", filter_value=username
        )
        if result_user is not None:
            logger.info(f"{test_case_name} :: Found user by username: {result_user}")
        else:
            logger.info(f"{test_case_name} :: User not found by username: {username}")

        assert result_user is not None, f"{test_case_name} :: User not found"

        user_id = result_user["id"]

        user_actions.delete_user(filter_param="id", filter_value=user_id)
        logger.info(f"{test_case_name} :: Deleted user with ID: {user_id}")

        deleted_user = user_actions.get_user_by_id(filter_value=user_id)
        if deleted_user is not None:
            logger.info(
                f"{test_case_name} :: User found after deletion: {deleted_user}"
            )
        else:
            logger.info(f"{test_case_name} :: User not found after deletion")

        assert deleted_user is None, f"{test_case_name} :: The user was not deleted"

    @pytest.mark.usefixtures("create_superuser", "create_roles", "create_users")
    def test_delete_all_users(self, user_actions):
        test_case_name = f"{self.__class__.__name__}.test_delete_all_users"
        logger.info(f"[users_tests] :: Running test case: {test_case_name}")

        user_actions.delete_all_users()
        all_users = user_actions.get_all_users()
        if all_users is not None:
            logger.info(f"{test_case_name} :: Users found after deletion: {all_users}")
        else:
            logger.info(f"{test_case_name} :: No users found after deletion")

        assert all_users is None, f"{test_case_name} :: Users were not deleted"

    @pytest.mark.usefixtures("create_superuser", "create_roles", "create_users")
    def test_get_user_role(self, user_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_user_role"
        logger.info(f"[users_tests] :: Running test case: {test_case_name}")

        random_user = get_random_user()
        if random_user is not None:
            logger.info(f"{test_case_name} :: Received random user: {random_user}")
        else:
            logger.info(f"{test_case_name} :: Random user not received")

        user_id = random_user["id"]

        user_role = user_actions.get_user_role(filter_param="id", filter_value=user_id)
        if user_role is not None:
            logger.info(f"{test_case_name} :: User role found: {user_role}")
        else:
            logger.info(f"{test_case_name} :: No user role found")

        assert (
            random_user["role_id"] == user_role["id"]
        ), f"{test_case_name} :: User role do not contain the expected role"

    @pytest.mark.usefixtures(
        "create_superuser",
        "create_roles",
        "create_users",
        "create_statuses",
        "create_priorities",
        "create_tasks",
    )
    def test_get_user_created_tasks(self, user_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_user_created_tasks"
        logger.info(f"[users_tests] :: Running test case: {test_case_name}")

        random_user = get_random_user()
        if random_user is not None:
            logger.info(f"{test_case_name} :: Received random user: {random_user}")
        else:
            logger.info(f"{test_case_name} :: Random user not received")

        user_id = random_user["id"]

        user_created_tasks = user_actions.get_user_created_tasks(
            filter_param="id", filter_value=user_id
        )
        if user_created_tasks is not None:
            logger.info(
                f"{test_case_name} :: User created tasks found: {user_created_tasks}"
            )
        else:
            logger.info(f"{test_case_name} :: No created tasks found")

        for task in user_created_tasks:
            assert (
                task["creator_id"] == random_user["id"]
            ), f"{test_case_name} :: User created tasks do not contain the expected tasks"

    @pytest.mark.usefixtures(
        "create_superuser",
        "create_roles",
        "create_users",
        "create_statuses",
        "create_priorities",
        "create_tasks",
    )
    def test_get_user_assigned_tasks(self, user_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_user_assigned_tasks"
        logger.info(f"[users_tests] :: Running test case: {test_case_name}")

        random_user = get_random_user()
        if random_user is not None:
            logger.info(f"{test_case_name} :: Received random user: {random_user}")
        else:
            logger.info(f"{test_case_name} :: Random user not received")

        user_id = random_user["id"]

        user_assigned_tasks = user_actions.get_user_assigned_tasks(
            filter_param="id", filter_value=user_id
        )
        if user_assigned_tasks is not None:
            logger.info(
                f"{test_case_name} :: User assigned tasks found: {user_assigned_tasks}"
            )
        else:
            logger.info(f"{test_case_name} :: No assigned tasks found")

        for task in user_assigned_tasks:
            assert (
                task["assignee_id"] == random_user["id"]
            ), f"{test_case_name} :: User assigned tasks do not contain the expected tasks"
