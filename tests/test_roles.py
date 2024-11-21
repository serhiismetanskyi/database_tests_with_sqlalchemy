import random

import pytest

from src.db.enums import RoleNames
from src.logger.logger import logger
from tests.factories.factory_utils import (get_current_datetime,
                                           get_random_user, random_user_id)


class TestRoles:
    @pytest.mark.usefixtures("create_superuser", "create_role", "create_user")
    def test_get_role_by_name(self, create_role, role_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_role_by_name"
        logger.info(f"[roles_tests] :: Running test case: {test_case_name}")

        expected_role_name = create_role["role_name"]

        result_role = role_actions.get_role_by_name(filter_value=expected_role_name)
        if result_role is not None:
            logger.info(f"{test_case_name} :: Found role by name: {result_role}")
        else:
            logger.info(
                f"{test_case_name} :: Role not found by name: {expected_role_name}"
            )

        assert result_role is not None, f"{test_case_name} :: Role not found by name"

        actual_role_name = result_role["role_name"]
        assert (
            actual_role_name == expected_role_name
        ), f"{test_case_name} :: The role name received does not match expectations"

    @pytest.mark.usefixtures("create_superuser", "create_role", "create_user")
    def test_get_role_name_field(self, create_role, role_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_role_name_field"
        logger.info(f"[roles_tests] :: Running test case: {test_case_name}")

        expected_role_name = create_role["role_name"]

        actual_role_name = role_actions.get_role_field(
            filter_param="role_name",
            filter_value=create_role["role_name"],
            field_name="role_name",
        )
        if actual_role_name is not None:
            logger.info(f"{test_case_name} :: Role name received: {actual_role_name}")
        else:
            logger.info(
                f"{test_case_name} :: Role not found by name: {expected_role_name}"
            )

        assert actual_role_name is not None, f"[roles_tests] :: Role not found by name"
        assert (
            actual_role_name == expected_role_name
        ), f"{test_case_name} :: The role name received does not match expectations"

    @pytest.mark.usefixtures("create_superuser", "create_roles", "create_users")
    def test_get_all_roles_created_today(self, role_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_all_roles_created_today"
        logger.info(f"[roles_tests] :: Running test case: {test_case_name}")

        current_datetime = get_current_datetime()
        all_roles_today = role_actions.get_all_roles_by_filter(
            filter_param="created_at", filter_value=current_datetime
        )

        if all_roles_today:
            logger.info(
                f"{test_case_name} :: Found roles created today: {all_roles_today}"
            )
        else:
            logger.info(f"{test_case_name} :: Roles created today not found")

        assert all_roles_today, f"{test_case_name} :: Roles created today not found"

    @pytest.mark.usefixtures("create_superuser")
    def test_update_role_name_field(self, create_role, role_actions):
        test_case_name = f"{self.__class__.__name__}.test_update_role_name_field"
        logger.info(f"[roles_tests] :: Running test case: {test_case_name}")

        role_name = create_role["role_name"]

        result_role = role_actions.get_role_by_filter(
            filter_param="role_name", filter_value=role_name
        )
        if result_role is not None:
            logger.info(f"{test_case_name} :: Found role by name: {result_role}")
        else:
            logger.info(f"{test_case_name} :: Role not found by name: {role_name}")

        role_id = result_role["id"]
        new_role_name = random.choice(list(RoleNames)).value

        role_actions.update_role_field(
            filter_param="id",
            filter_value=role_id,
            field_name="role_name",
            new_value=new_role_name,
        )
        logger.info(f"{test_case_name} :: Updated role with ID: {role_id}")

        updated_role = role_actions.get_role_by_filter(
            filter_param="role_name", filter_value=new_role_name
        )
        if updated_role is not None:
            logger.info(f"{test_case_name} :: Role found after update: {updated_role}")
        else:
            logger.info(f"{test_case_name} :: Role not found after update")

        assert (
            updated_role["role_name"] == new_role_name
        ), f"{test_case_name} :: The role was not updated"

    @pytest.mark.usefixtures("create_superuser", "create_role", "create_user")
    def test_update_role_fields(self, create_role, role_actions):
        test_case_name = f"{self.__class__.__name__}.test_update_role_fields"
        logger.info(f"[roles_tests] :: Running test case: {test_case_name}")

        role_name = create_role["role_name"]

        result_role = role_actions.get_role_by_filter(
            filter_param="role_name", filter_value=role_name
        )
        if result_role is not None:
            logger.info(f"{test_case_name} :: Found role by name: {result_role}")
        else:
            logger.info(f"{test_case_name} :: Role not found by name: {role_name}")

        role_id = result_role["id"]

        new_data = {
            "role_name": random.choice(list(RoleNames)).value,
            "creator_id": random_user_id(),
        }
        role_actions.update_role_fields(
            filter_param="id", filter_value=role_id, updated_data=new_data
        )
        logger.info(f"{test_case_name} :: Updated role with ID: {role_id}")

        updated_role = role_actions.get_role_by_id(filter_value=role_id)
        if updated_role is not None:
            logger.info(f"{test_case_name} :: Role found after update: {updated_role}")
        else:
            logger.info(f"{test_case_name} :: Role not found after update")

        assert updated_role is not None, f"{test_case_name} :: The role was not updated"

        assert (
            updated_role["role_name"] == new_data["role_name"]
        ), f"{test_case_name} :: role_name field not updated correctly"

        assert (
            updated_role["creator_id"] == new_data["creator_id"]
        ), f"{test_case_name} :: creator_id field not updated correctly"

    @pytest.mark.usefixtures("create_superuser", "create_role", "create_user")
    def test_delete_role(self, create_role, role_actions):
        test_case_name = f"{self.__class__.__name__}.test_delete_role"
        logger.info(f"[roles_tests] :: Running test case: {test_case_name}")

        role_name = create_role["role_name"]

        result_role = role_actions.get_role_by_filter(
            filter_param="role_name", filter_value=role_name
        )
        if result_role is not None:
            logger.info(f"{test_case_name} :: Found role by name: {result_role}")
        else:
            logger.info(f"{test_case_name} :: Role not found by name: {role_name}")

        role_id = result_role["id"]

        assert result_role is not None, f"{test_case_name} :: Role not found"

        role_actions.delete_role(filter_param="id", filter_value=role_id)
        logger.info(f"{test_case_name} :: Deleted role with ID: {role_id}")

        deleted_role = role_actions.get_role_by_id(filter_value=role_id)
        if deleted_role is not None:
            logger.info(
                f"{test_case_name} :: Role found after deletion: {deleted_role}"
            )
        else:
            logger.info(f"{test_case_name} :: Role not found after deletion")

        assert deleted_role is None, f"{test_case_name} :: The role was not deleted"

    @pytest.mark.usefixtures(
        "create_superuser", "create_roles", "create_users", "create_roles"
    )
    def test_delete_all_roles(self, role_actions):
        test_case_name = f"{self.__class__.__name__}.test_delete_all_roles"
        logger.info(f"[roles_tests] :: Running test case: {test_case_name}")

        role_actions.delete_all_roles()
        all_roles = role_actions.get_all_roles()
        if all_roles is not None:
            logger.info(f"{test_case_name} :: Roles found after deletion: {all_roles}")
        else:
            logger.info(f"{test_case_name} :: No roles found after deletion")

        assert all_roles is None, f"{test_case_name} :: Roles were not deleted"

    @pytest.mark.usefixtures("create_superuser", "create_roles", "create_users")
    def test_get_role_users(self, role_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_role_users"
        logger.info(f"[roles_tests] :: Running test case: {test_case_name}")

        random_user = get_random_user()
        if random_user is not None:
            logger.info(f"{test_case_name} :: Received random user: {random_user}")
        else:
            logger.info(f"{test_case_name} :: Random user not received")

        role_id = random_user["role_id"]

        role_users = role_actions.get_role_users(
            filter_param="id", filter_value=role_id
        )
        if role_users is not None:
            logger.info(f"{test_case_name} :: Role users found: {role_users}")
        else:
            logger.info(f"{test_case_name} :: No role users found")

        assert any(
            task["id"] == random_user["id"] for task in role_users
        ), f"{test_case_name} :: Role users do not contain the expected task"
