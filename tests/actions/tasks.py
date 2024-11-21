from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from src.db.models import Task
from tests.actions.base import BaseActions


class TaskActions(BaseActions):
    def __init__(self, session: Session = None):
        super().__init__(model=Task, session=session)

    def create_tasks_table(self) -> str:
        return self.create_table()

    def drop_tasks_table(self) -> str:
        return self.drop_table()

    def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.create_instance(task_data)

    def get_task_by_id(self, filter_value: int) -> Optional[Dict[str, Any]]:
        return self.get_task_by_filter("id", filter_value)

    def get_task_by_title(self, filter_value: str) -> Optional[Dict[str, Any]]:
        return self.get_task_by_filter("title", filter_value)

    def get_task_by_filter(
        self, filter_param: str, filter_value: Any
    ) -> Optional[Dict[str, Any]]:
        return self.filter_by(filter_param, filter_value)

    def get_random_task(self) -> Optional[Dict[str, Any]]:
        return self.get_random()

    def get_task_field(
        self, filter_param: str, filter_value: Any, field_name: str
    ) -> Any:
        return self.get_field_value(filter_param, filter_value, field_name)

    def get_all_tasks(self) -> Optional[List[Dict[str, Any]]]:
        return self.get_all()

    def get_all_tasks_by_filter(
        self, filter_param: str, filter_value: Any
    ) -> Optional[List[Dict[str, Any]]]:
        return self.get_all_by_filter(filter_param, filter_value)

    def get_task_priority(self, filter_param: str, filter_value: Any) -> Dict[str, Any]:
        return self.get_task_relationship(filter_param, filter_value, "priority")

    def get_task_status(self, filter_param: str, filter_value: Any) -> Dict[str, Any]:
        return self.get_task_relationship(filter_param, filter_value, "status")

    def get_task_creator(self, filter_param: str, filter_value: Any) -> Dict[str, Any]:
        return self.get_task_relationship(filter_param, filter_value, "creator")

    def get_task_assignee(self, filter_param: str, filter_value: Any) -> Dict[str, Any]:
        return self.get_task_relationship(filter_param, filter_value, "assignee")

    def get_task_relationship(
        self, filter_param: str, filter_value: Any, relationship_name: str
    ) -> List[Dict[str, Any]] | Dict[str, Any]:
        return self.get_relationship(filter_param, filter_value, relationship_name)

    def update_task_field(
        self, filter_param: str, filter_value: Any, field_name: str, new_value: Any
    ) -> Dict[str, Any]:
        return self.update_field(filter_param, filter_value, field_name, new_value)

    def update_task_fields(
        self, filter_param: str, filter_value: Any, updated_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self.update_fields(filter_param, filter_value, updated_data)

    def delete_task(self, filter_param: str, filter_value: Any) -> str:
        return self.delete(filter_param, filter_value)

    def delete_all_tasks(self) -> str:
        return self.delete_all()
