import random

import pytest

from src.db.enums import StatusNames
from src.logger.logger import logger
from tests.factories.factory_utils import (get_current_datetime,
                                           get_random_task, random_user_id)


class TestStatuses:
    @pytest.mark.usefixtures("create_superuser", "create_role", "create_user")
    def test_get_status_by_name(self, create_status, status_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_status_by_name"
        logger.info(f"[statuses_tests] :: Running test case: {test_case_name}")

        expected_status_name = create_status["status_name"]

        result_status = status_actions.get_status_by_name(
            filter_value=expected_status_name
        )
        if result_status is not None:
            logger.info(f"{test_case_name} :: Found status by name: {result_status}")
        else:
            logger.info(
                f"{test_case_name} :: Status not found by name: {expected_status_name}"
            )

        assert (
            result_status is not None
        ), f"{test_case_name} :: Status not found by name"

        actual_status_name = result_status["status_name"]
        assert (
            actual_status_name == expected_status_name
        ), f"{test_case_name} :: The status name received does not match expectations"

    @pytest.mark.usefixtures("create_superuser", "create_role", "create_user")
    def test_get_status_name_field(self, create_status, status_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_status_name_field"
        logger.info(f"[statuses_tests] :: Running test case: {test_case_name}")

        expected_status_name = create_status["status_name"]

        actual_status_name = status_actions.get_status_field(
            filter_param="status_name",
            filter_value=create_status["status_name"],
            field_name="status_name",
        )
        if actual_status_name is not None:
            logger.info(
                f"{test_case_name} :: Status name received: {actual_status_name}"
            )
        else:
            logger.info(
                f"{test_case_name} :: Status not found by name: {expected_status_name}"
            )

        assert (
            actual_status_name is not None
        ), f"{test_case_name} :: Status not found by name"
        assert (
            actual_status_name == expected_status_name
        ), f"{test_case_name} :: The status name received does not match expectations"

    @pytest.mark.usefixtures(
        "create_superuser", "create_roles", "create_users", "create_statuses"
    )
    def test_get_all_statuses_created_today(self, status_actions):
        test_case_name = (
            f"{self.__class__.__name__}.test_get_all_statuses_created_today"
        )
        logger.info(f"[statuses_tests] :: Running test case: {test_case_name}")

        current_datetime = get_current_datetime()
        all_statuses_today = status_actions.get_all_statuses_by_filter(
            filter_param="created_at", filter_value=current_datetime
        )

        if all_statuses_today:
            logger.info(
                f"{test_case_name} :: Found statuses created today: {all_statuses_today}"
            )
        else:
            logger.info(f"{test_case_name} :: Statuses created today not found")

        assert (
            all_statuses_today
        ), f"{test_case_name} :: Statuses created today not found"

    @pytest.mark.usefixtures("create_superuser")
    def test_update_status_name_field(self, create_status, status_actions):
        test_case_name = f"{self.__class__.__name__}.test_update_status_name_field"
        logger.info(f"[statuses_tests] :: Running test case: {test_case_name}")

        status_name = create_status["status_name"]

        result_status = status_actions.get_status_by_filter(
            filter_param="status_name", filter_value=status_name
        )
        if result_status is not None:
            logger.info(f"{test_case_name} :: Found status by name: {result_status}")
        else:
            logger.info(f"{test_case_name} :: Status not found by name: {status_name}")

        status_id = result_status["id"]
        new_status_name = random.choice(list(StatusNames)).value

        status_actions.update_status_field(
            filter_param="id",
            filter_value=status_id,
            field_name="status_name",
            new_value=new_status_name,
        )
        logger.info(f"{test_case_name} :: Updated status with ID: {status_id}")

        updated_status = status_actions.get_status_by_filter(
            filter_param="status_name", filter_value=new_status_name
        )
        if updated_status is not None:
            logger.info(
                f"{test_case_name} :: Status found after update: {updated_status}"
            )
        else:
            logger.info(f"{test_case_name} :: Status not found after update")

        assert (
            updated_status["status_name"] == new_status_name
        ), f"{test_case_name} :: The status was not updated"

    @pytest.mark.usefixtures("create_superuser", "create_role", "create_user")
    def test_update_status_fields(self, create_status, status_actions):
        test_case_name = f"{self.__class__.__name__}.test_update_status_fields"
        logger.info(f"[statuses_tests] :: Running test case: {test_case_name}")

        status_name = create_status["status_name"]

        result_status = status_actions.get_status_by_filter(
            filter_param="status_name", filter_value=status_name
        )
        if result_status is not None:
            logger.info(f"{test_case_name} :: Found status by name: {result_status}")
        else:
            logger.info(f"{test_case_name} :: Status not found by name: {status_name}")

        status_id = result_status["id"]

        new_data = {
            "status_name": random.choice(list(StatusNames)).value,
            "creator_id": random_user_id(),
        }
        status_actions.update_status_fields(
            filter_param="id", filter_value=status_id, updated_data=new_data
        )
        logger.info(f"{test_case_name} :: Updated status with ID: {status_id}")

        updated_status = status_actions.get_status_by_id(filter_value=status_id)
        if updated_status is not None:
            logger.info(
                f"{test_case_name} :: Status found after update: %s", updated_status
            )
        else:
            logger.info(f"{test_case_name} :: Status not found after update")

        assert (
            updated_status is not None
        ), f"{test_case_name} :: The status was not updated"

        assert (
            updated_status["status_name"] == new_data["status_name"]
        ), f"{test_case_name} :: status_name field not updated correctly"

        assert (
            updated_status["creator_id"] == new_data["creator_id"]
        ), f"{test_case_name} :: creator_id field not updated correctly"

    @pytest.mark.usefixtures("create_superuser", "create_role", "create_user")
    def test_delete_status(self, create_status, status_actions):
        test_case_name = f"{self.__class__.__name__}.test_delete_status"
        logger.info(f"[statuses_tests] :: Running test case: {test_case_name}")

        status_name = create_status["status_name"]

        result_status = status_actions.get_status_by_filter(
            filter_param="status_name", filter_value=status_name
        )
        if result_status is not None:
            logger.info(f"{test_case_name} :: Found status by name: {result_status}")
        else:
            logger.info(f"{test_case_name} :: Status not found by name: {status_name}")

        assert result_status is not None, f"{test_case_name} :: Status not found"

        status_id = result_status["id"]

        status_actions.delete_status(filter_param="id", filter_value=status_id)
        logger.info(f"{test_case_name} :: Deleted status with ID: {status_id}")

        deleted_status = status_actions.get_status_by_id(filter_value=status_id)
        if deleted_status is not None:
            logger.info(
                f"{test_case_name} :: Status found after deletion: {deleted_status}"
            )
        else:
            logger.info(f"{test_case_name} :: Status not found after deletion")

        assert deleted_status is None, f"{test_case_name} :: The status was not deleted"

    @pytest.mark.usefixtures(
        "create_superuser", "create_roles", "create_users", "create_statuses"
    )
    def test_delete_all_statuses(self, status_actions):
        test_case_name = f"{self.__class__.__name__}.test_delete_all_statuses"
        logger.info(f"[statuses_tests] :: Running test case: {test_case_name}")

        status_actions.delete_all_statuses()
        all_statuses = status_actions.get_all_statuses()
        if all_statuses is not None:
            logger.info(
                f"{test_case_name} :: Statuses found after deletion: {all_statuses}"
            )
        else:
            logger.info(f"{test_case_name} :: No statuses found after deletion")

        assert all_statuses is None, f"{test_case_name} :: Statuses were not deleted"

    @pytest.mark.usefixtures(
        "create_superuser",
        "create_roles",
        "create_users",
        "create_statuses",
        "create_priorities",
        "create_tasks",
    )
    def test_get_status_tasks(self, status_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_status_tasks"
        logger.info(f"[statuses_tests] :: Running test case: {test_case_name}")

        random_task = get_random_task()
        if random_task is not None:
            logger.info(f"{test_case_name} :: Received random task: {random_task}")
        else:
            logger.info(f"{test_case_name} :: Random task not received")

        status_id = random_task["status_id"]

        status_tasks = status_actions.get_status_tasks(
            filter_param="id", filter_value=status_id
        )
        if status_tasks is not None:
            logger.info(f"{test_case_name} :: Status tasks found: {status_tasks}")
        else:
            logger.info(f"{test_case_name} :: No status tasks found")

        assert any(
            task["id"] == random_task["id"] for task in status_tasks
        ), f"{test_case_name} :: Status tasks do not contain the expected task"
