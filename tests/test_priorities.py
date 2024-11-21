import random

import pytest

from src.db.enums import PriorityNames
from src.logger.logger import logger
from tests.factories.factory_utils import (get_current_datetime,
                                           get_random_task, random_user_id)


class TestPriorities:
    @pytest.mark.usefixtures("create_superuser", "create_role", "create_user")
    def test_get_priority_by_name(self, create_priority, priority_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_priority_by_name"
        logger.info(f"[priorities_tests] :: Running test case: {test_case_name}")

        expected_priority_name = create_priority["priority_name"]

        result_priority = priority_actions.get_priority_by_name(
            filter_value=expected_priority_name
        )
        if result_priority is not None:
            logger.info(
                f"{test_case_name} :: Found priority by name: {result_priority}"
            )
        else:
            logger.info(
                f"{test_case_name} :: Priority not found by name: {expected_priority_name}"
            )

        assert (
            result_priority is not None
        ), f"{test_case_name} :: Priority not found by name"

        actual_priority_name = result_priority["priority_name"]
        assert (
            actual_priority_name == expected_priority_name
        ), f"{test_case_name} :: The priority name received does not match expectations"

    @pytest.mark.usefixtures("create_superuser", "create_role", "create_user")
    def test_get_priority_name_field(self, create_priority, priority_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_priority_name_field"
        logger.info(f"[priorities_tests] :: Running test case: {test_case_name}")

        expected_priority_name = create_priority["priority_name"]

        actual_priority_name = priority_actions.get_priority_field(
            filter_param="priority_name",
            filter_value=create_priority["priority_name"],
            field_name="priority_name",
        )
        if actual_priority_name is not None:
            logger.info(
                f"{test_case_name} :: Priority name received: {actual_priority_name}"
            )
        else:
            logger.info(
                f"{test_case_name} :: Priority not found by name: {expected_priority_name}"
            )

        assert (
            actual_priority_name is not None
        ), f"{test_case_name} :: Priority not found by name"
        assert (
            actual_priority_name == expected_priority_name
        ), f"{test_case_name} :: The priority name received does not match expectations"

    @pytest.mark.usefixtures(
        "create_superuser", "create_roles", "create_users", "create_priorities"
    )
    def test_get_all_priorities_created_today(self, priority_actions):
        test_case_name = (
            f"{self.__class__.__name__}.test_get_all_priorities_created_today"
        )
        logger.info(f"[priorities_tests] :: Running test case: {test_case_name}")

        current_datetime = get_current_datetime()
        all_priorities_today = priority_actions.get_all_priorities_by_filter(
            filter_param="created_at", filter_value=current_datetime
        )

        if all_priorities_today:
            logger.info(
                f"{test_case_name} :: Found priorities created today: {all_priorities_today}"
            )
        else:
            logger.info(f"{test_case_name} :: Priorities created today not found")

        assert (
            all_priorities_today
        ), f"{test_case_name} :: Priorities created today not found"

    @pytest.mark.usefixtures("create_superuser")
    def test_update_priority_name_field(self, create_priority, priority_actions):
        test_case_name = f"{self.__class__.__name__}.test_update_priority_name_field"
        logger.info(f"[priorities_tests] :: Running test case: {test_case_name}")

        result_priority = priority_actions.get_priority_by_filter(
            filter_param="priority_name", filter_value=create_priority["priority_name"]
        )
        if result_priority is not None:
            logger.info(
                f"{test_case_name} :: Found priority by name: {result_priority}"
            )
        else:
            logger.info(
                f"{test_case_name} :: Priority not found by name: {result_priority}"
            )

        priority_id = result_priority["id"]
        new_priority_name = random.choice(list(PriorityNames)).value

        priority_actions.update_priority_field(
            filter_param="id",
            filter_value=priority_id,
            field_name="priority_name",
            new_value=new_priority_name,
        )
        logger.info(f"{test_case_name} :: Updated priority with ID: {priority_id}")

        updated_priority = priority_actions.get_priority_by_filter(
            filter_param="priority_name", filter_value=new_priority_name
        )
        if updated_priority is not None:
            logger.info(
                f"{test_case_name} :: User found after update: {updated_priority}",
            )
        else:
            logger.info(f"{test_case_name} :: User not found after update,")

        assert (
            updated_priority["priority_name"] == new_priority_name
        ), f"{test_case_name} :: The priority was not updated"

    @pytest.mark.usefixtures("create_superuser", "create_role", "create_user")
    def test_update_priority_fields(self, create_priority, priority_actions):
        test_case_name = f"{self.__class__.__name__}.test_update_priority_fields"
        logger.info(f"[priorities_tests] :: Running test case: {test_case_name}")

        priority_name = create_priority["priority_name"]

        result_priority = priority_actions.get_priority_by_filter(
            filter_param="priority_name", filter_value=priority_name
        )
        if result_priority is not None:
            logger.info(
                f"{test_case_name} :: Found priority by name: {result_priority}"
            )
        else:
            logger.info(
                f"{test_case_name} :: Priority not found by name: {priority_name}"
            )

        priority_id = result_priority["id"]

        new_data = {
            "priority_name": random.choice(list(PriorityNames)).value,
            "creator_id": random_user_id(),
        }
        priority_actions.update_priority_fields(
            filter_param="id", filter_value=priority_id, updated_data=new_data
        )
        logger.info(f"{test_case_name} :: Updated priority with ID: {priority_id}")

        updated_priority = priority_actions.get_priority_by_id(filter_value=priority_id)
        if updated_priority is not None:
            logger.info(
                f"{test_case_name} :: Priority found after update: {updated_priority}"
            )
        else:
            logger.info(f"{test_case_name} :: Priority not found after update")

        assert (
            updated_priority is not None
        ), f"{test_case_name} :: The priority was not updated"

        assert (
            updated_priority["priority_name"] == new_data["priority_name"]
        ), f"{test_case_name} :: priority_name field not updated correctly"

        assert (
            updated_priority["creator_id"] == new_data["creator_id"]
        ), f"{test_case_name} :: creator_id field not updated correctly"

    @pytest.mark.usefixtures("create_superuser", "create_role", "create_user")
    def test_delete_priority(self, create_priority, priority_actions):
        test_case_name = f"{self.__class__.__name__}.test_delete_priority"
        logger.info(f"[priorities_tests] :: Running test case: {test_case_name}")

        priority_name = create_priority["priority_name"]

        result_priority = priority_actions.get_priority_by_filter(
            filter_param="priority_name", filter_value=priority_name
        )
        if result_priority is not None:
            logger.info(
                f"{test_case_name} :: Found priority by name: {result_priority}"
            )
        else:
            logger.info(
                f"{test_case_name} :: Priority not found by name: {priority_name}"
            )

        priority_id = result_priority["id"]

        assert result_priority is not None, f"{test_case_name} :: Priority not found"

        priority_actions.delete_priority(filter_param="id", filter_value=priority_id)
        logger.info(f"{test_case_name} :: Deleted priority with ID: {priority_id}")

        deleted_priority = priority_actions.get_priority_by_id(filter_value=priority_id)
        if deleted_priority is not None:
            logger.info(
                f"{test_case_name} :: Priority found after deletion: %s",
                deleted_priority,
            )
        else:
            logger.info(f"{test_case_name} :: Priority not found after deletion")

        assert (
            deleted_priority is None
        ), f"{test_case_name} :: The priority was not deleted"

    @pytest.mark.usefixtures(
        "create_superuser", "create_roles", "create_users", "create_priorities"
    )
    def test_delete_all_priorities(self, priority_actions):
        test_case_name = f"{self.__class__.__name__}.test_delete_all_priorities"
        logger.info(f"[priorities_tests] :: Running test case: {test_case_name}")

        priority_actions.delete_all_priorities()
        all_priorities = priority_actions.get_all_priorities()
        if all_priorities is not None:
            logger.info(
                f"{test_case_name} :: Priorities found after deletion: {all_priorities}"
            )
        else:
            logger.info(f"{test_case_name} :: No priorities found after deletion")

        assert (
            all_priorities is None
        ), f"{test_case_name} :: Priorities were not deleted"

    @pytest.mark.usefixtures(
        "create_superuser",
        "create_roles",
        "create_users",
        "create_statuses",
        "create_priorities",
        "create_tasks",
    )
    def test_get_priority_tasks(self, priority_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_priority_tasks"
        logger.info(f"[priorities_tests] :: Running test case: {test_case_name}")

        random_task = get_random_task()
        if random_task is not None:
            logger.info(f"{test_case_name} :: Received random task: {random_task}")
        else:
            logger.info(f"{test_case_name} :: Random task not received")

        priority_id = random_task["priority_id"]

        priority_tasks = priority_actions.get_priority_tasks(
            filter_param="id", filter_value=priority_id
        )
        if priority_tasks is not None:
            logger.info(f"{test_case_name} :: Priority tasks found: {priority_tasks}")
        else:
            logger.info(f"{test_case_name} :: No priority tasks found")

        assert any(
            task["id"] == random_task["id"] for task in priority_tasks
        ), f"{test_case_name} :: Priority tasks do not contain the expected task"
