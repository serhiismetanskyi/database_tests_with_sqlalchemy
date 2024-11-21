import pytest

from src.logger.logger import logger
from tests.factories.factories import fake
from tests.factories.factory_utils import (get_current_datetime,
                                           get_formatted_datetime,
                                           get_random_task,
                                           get_updated_datetime)


class TestTasks:
    @pytest.mark.usefixtures(
        "create_superuser",
        "create_role",
        "create_user",
        "create_status",
        "create_priority",
    )
    def test_get_task_by_title(self, create_task, task_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_task_by_title"
        logger.info(f"[tasks_tests] :: Running test case: {test_case_name}")

        expected_title = create_task["title"]

        result_task = task_actions.get_task_by_title(filter_value=expected_title)
        if result_task is not None:
            logger.info(f"{test_case_name} :: Found task by title: {result_task}")
        else:
            logger.info(
                f"{test_case_name} :: Task not found by title: {expected_title}"
            )

        assert result_task is not None, f"{test_case_name} :: Task not found by title"

        actual_title = result_task["title"]
        assert (
            actual_title == expected_title
        ), f"{test_case_name} :: The title received does not match expectations"

    @pytest.mark.usefixtures(
        "create_superuser",
        "create_role",
        "create_user",
        "create_status",
        "create_priority",
    )
    def test_get_task_description_field(self, create_task, task_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_task_description_field"
        logger.info(f"[tasks_tests] :: Running test case: {test_case_name}")

        task_title = create_task["title"]
        expected_description = create_task["description"]

        actual_description = task_actions.get_task_field(
            filter_param="title",
            filter_value=task_title,
            field_name="description",
        )
        if actual_description is not None:
            logger.info(
                f"{test_case_name} :: Task description received: {actual_description}"
            )
        else:
            logger.info(f"{test_case_name} :: Task not found by title: {task_title}")

        assert (
            actual_description is not None
        ), f"{test_case_name} :: Task not found by title"
        assert (
            actual_description == expected_description
        ), f"{test_case_name} :: The description received does not match expectations"

    @pytest.mark.usefixtures(
        "create_superuser",
        "create_roles",
        "create_users",
        "create_statuses",
        "create_priorities",
        "create_tasks",
    )
    def test_get_all_tasks_created_today(self, task_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_all_tasks_created_today"
        logger.info(f"[tasks_tests] :: Running test case: {test_case_name}")

        current_datetime = get_current_datetime()
        all_tasks_today = task_actions.get_all_tasks_by_filter(
            filter_param="created_at", filter_value=current_datetime
        )

        if all_tasks_today:
            logger.info(
                f"{test_case_name} :: Found tasks created today: {all_tasks_today}"
            )
        else:
            logger.info(f"{test_case_name} :: Tasks created today not found")

        assert all_tasks_today, f"{test_case_name} :: Tasks created today not found"

    @pytest.mark.usefixtures(
        "create_superuser",
        "create_role",
        "create_user",
        "create_status",
        "create_priority",
    )
    def test_update_task_deadline_field(self, create_task, task_actions):
        test_case_name = f"{self.__class__.__name__}.test_update_task_deadline_field"
        logger.info(f"[tasks_tests] :: Running test case: {test_case_name}")

        task_title = create_task["title"]

        result_task = task_actions.get_task_by_filter(
            filter_param="title", filter_value=task_title
        )
        if result_task is not None:
            logger.info(f"{test_case_name} :: Found task by title: {result_task}")
        else:
            logger.info(f"{test_case_name} :: Task not found by title: {task_title}")

        task_id = result_task["id"]
        new_deadline = get_updated_datetime(days=1, hours=2, minutes=30)

        task_actions.update_task_field(
            filter_param="id",
            filter_value=task_id,
            field_name="deadline",
            new_value=new_deadline,
        )
        logger.info(f"{test_case_name} :: Updated task with ID: {task_id}")

        updated_task = task_actions.get_task_by_filter(
            filter_param="id", filter_value=task_id
        )
        if updated_task is not None:
            logger.info(f"{test_case_name} :: Task found after update: {updated_task}")
        else:
            logger.info(f"{test_case_name} :: Task not found after update")

        current_deadline = get_formatted_datetime(date_time=updated_task["deadline"])
        assert (
            current_deadline == new_deadline
        ), f"{test_case_name} :: The task was not updated"

    @pytest.mark.usefixtures(
        "create_superuser",
        "create_role",
        "create_user",
        "create_status",
        "create_priority",
    )
    def test_update_task_fields(self, create_task, task_actions):
        test_case_name = f"{self.__class__.__name__}.test_update_task_fields"
        logger.info(f"[tasks_tests] :: Running test case: {test_case_name}")

        task_title = create_task["title"]

        result_task = task_actions.get_task_by_filter(
            filter_param="title", filter_value=task_title
        )
        if result_task is not None:
            logger.info(f"{test_case_name} :: Found task by title: {result_task}")
        else:
            logger.info(f"{test_case_name} :: Task not found by title: {task_title}")

        task_id = result_task["id"]

        new_data = {
            "title": fake.text(max_nb_chars=50),
            "description": fake.text(max_nb_chars=255),
        }
        task_actions.update_task_fields(
            filter_param="id", filter_value=task_id, updated_data=new_data
        )
        logger.info(f"{test_case_name} :: Updated task with ID: {task_id}")

        updated_task = task_actions.get_task_by_id(filter_value=task_id)

        if updated_task is not None:
            logger.info(
                f"{test_case_name} :: Task found after update: %s", updated_task
            )
        else:
            logger.info(f"{test_case_name} :: Task not found after update")

        assert updated_task is not None, f"{test_case_name} :: The task was not updated"

        assert (
            updated_task["title"] == new_data["title"]
        ), f"{test_case_name} :: title field not updated correctly"

        assert (
            updated_task["description"] == new_data["description"]
        ), f"{test_case_name} :: description field not updated correctly"

    @pytest.mark.usefixtures(
        "create_superuser",
        "create_role",
        "create_user",
        "create_status",
        "create_priority",
    )
    def test_delete_task(self, create_task, task_actions):
        test_case_name = f"{self.__class__.__name__}.test_delete_task"
        logger.info(f"[tasks_tests] :: Running test case: {test_case_name}")

        task_title = create_task["title"]

        result_task = task_actions.get_task_by_filter(
            filter_param="title", filter_value=task_title
        )
        if result_task is not None:
            logger.info(f"{test_case_name} :: Found task by title: {result_task}")
        else:
            logger.info(f"{test_case_name} :: Task not found by title: {task_title}")

        assert result_task is not None, f"{test_case_name} :: Task not found"

        task_id = result_task["id"]

        task_actions.delete_task(filter_param="id", filter_value=task_id)
        logger.info(f"{test_case_name} :: Deleted task with ID: {task_id}")

        deleted_task = task_actions.get_task_by_id(filter_value=task_id)
        if deleted_task is not None:
            logger.info(
                f"{test_case_name} :: Task found after deletion: {deleted_task}"
            )
        else:
            logger.info(f"{test_case_name} :: Task not found after deletion")

        assert deleted_task is None, f"{test_case_name} :: The task was not deleted"

    @pytest.mark.usefixtures(
        "create_superuser",
        "create_roles",
        "create_users",
        "create_statuses",
        "create_priorities",
        "create_tasks",
    )
    def test_delete_all_tasks(self, task_actions):
        test_case_name = f"{self.__class__.__name__}.test_delete_all_tasks"
        logger.info(f"[tasks_tests] :: Running test case: {test_case_name}")

        task_actions.delete_all_tasks()
        all_tasks = task_actions.get_all_tasks()
        if all_tasks is not None:
            logger.info(f"{test_case_name} :: Tasks found after deletion: {all_tasks}")
        else:
            logger.info(f"{test_case_name} :: No tasks found after deletion")

        assert all_tasks is None, f"{test_case_name} :: Tasks were not deleted"

    @pytest.mark.usefixtures(
        "create_superuser",
        "create_roles",
        "create_users",
        "create_statuses",
        "create_priorities",
        "create_tasks",
    )
    def test_get_task_priority(self, task_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_task_priority"
        logger.info(f"[tasks_tests] :: Running test case: {test_case_name}")

        random_task = get_random_task()
        if random_task is not None:
            logger.info(f"{test_case_name} :: Received random task: {random_task}")
        else:
            logger.info(f"{test_case_name} :: Random task not received")

        task_id = random_task["id"]

        task_priority = task_actions.get_task_priority(
            filter_param="id", filter_value=task_id
        )
        if task_priority is not None:
            logger.info(f"{test_case_name} :: Task priority found: {task_priority}")
        else:
            logger.info(f"{test_case_name} :: No task priority found")

        assert (
            random_task["priority_id"] == task_priority["id"]
        ), f"{test_case_name} :: Task priority do not contain the expected priority"

    @pytest.mark.usefixtures(
        "create_superuser",
        "create_roles",
        "create_users",
        "create_statuses",
        "create_priorities",
        "create_tasks",
    )
    def test_get_task_status(self, task_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_task_status"
        logger.info(f"[tasks_tests] :: Running test case: {test_case_name}")

        random_task = get_random_task()
        if random_task is not None:
            logger.info(f"{test_case_name} :: Received random task: {random_task}")
        else:
            logger.info(f"{test_case_name} :: Random task not received")

        task_id = random_task["id"]

        task_status = task_actions.get_task_status(
            filter_param="id", filter_value=task_id
        )
        if task_status is not None:
            logger.info(f"{test_case_name} :: Task status found: {task_status}")
        else:
            logger.info(f"{test_case_name} :: No task status found")

        assert (
            random_task["status_id"] == task_status["id"]
        ), f"{test_case_name} :: Task status does not contain the expected status"

    @pytest.mark.usefixtures(
        "create_superuser",
        "create_roles",
        "create_users",
        "create_statuses",
        "create_priorities",
        "create_tasks",
    )
    def test_get_task_creator(self, task_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_task_creator"
        logger.info(f"[tasks_tests] :: Running test case: {test_case_name}")

        random_task = get_random_task()
        if random_task is not None:
            logger.info(f"{test_case_name} :: Received random task: {random_task}")
        else:
            logger.info(f"{test_case_name} :: Random task not received")

        task_id = random_task["id"]

        task_creator = task_actions.get_task_creator(
            filter_param="id", filter_value=task_id
        )
        if task_creator is not None:
            logger.info(f"{test_case_name} :: Task creator found: {task_creator}")
        else:
            logger.info(f"{test_case_name} :: No task creator found")

        assert (
            random_task["creator_id"] == task_creator["id"]
        ), f"{test_case_name} :: Task creator does not contain the expected creator"

    @pytest.mark.usefixtures(
        "create_superuser",
        "create_roles",
        "create_users",
        "create_statuses",
        "create_priorities",
        "create_tasks",
    )
    def test_get_task_assignee(self, task_actions):
        test_case_name = f"{self.__class__.__name__}.test_get_task_assignee"
        logger.info(f"[tasks_tests] :: Running test case: {test_case_name}")

        random_task = get_random_task()
        if random_task is not None:
            logger.info(f"{test_case_name} :: Received random task: {random_task}")
        else:
            logger.info(f"{test_case_name} :: Random task not received")

        task_id = random_task["id"]

        task_assignee = task_actions.get_task_assignee(
            filter_param="id", filter_value=task_id
        )
        if task_assignee is not None:
            logger.info(f"{test_case_name} :: Task assignee found: {task_assignee}")
        else:
            logger.info(f"{test_case_name} :: No task assignee found")

        assert (
            random_task["assignee_id"] == task_assignee["id"]
        ), f"{test_case_name} :: Task assignee does not contain the expected assignee"
