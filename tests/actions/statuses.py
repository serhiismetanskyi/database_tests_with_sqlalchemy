from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from src.db.models import Status
from tests.actions.base import BaseActions


class StatusActions(BaseActions):
    def __init__(self, session: Session = None):
        super().__init__(model=Status, session=session)

    def create_statuses_table(self) -> str:
        return self.create_table()

    def drop_statuses_table(self) -> str:
        return self.drop_table()

    def create_status(self, status_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.create_instance(status_data)

    def get_status_by_id(self, filter_value: int) -> Optional[Dict[str, Any]]:
        return self.get_status_by_filter("id", filter_value)

    def get_status_by_name(self, filter_value: str) -> Optional[Dict[str, Any]]:
        return self.get_status_by_filter("status_name", filter_value)

    def get_status_by_filter(
        self, filter_param: str, filter_value: Any
    ) -> Optional[Dict[str, Any]]:
        return self.filter_by(filter_param, filter_value)

    def get_random_status(self) -> Optional[Dict[str, Any]]:
        return self.get_random()

    def get_status_field(
        self, filter_param: str, filter_value: Any, field_name: str
    ) -> Any:
        return self.get_field_value(filter_param, filter_value, field_name)

    def get_all_statuses(self) -> Optional[List[Dict[str, Any]]]:
        return self.get_all()

    def get_all_statuses_by_filter(
        self, filter_param: str, filter_value: Any
    ) -> Optional[List[Dict[str, Any]]]:
        return self.get_all_by_filter(filter_param, filter_value)

    def get_status_tasks(
        self, filter_param: str, filter_value: Any
    ) -> List[Dict[str, Any]]:
        return self.get_status_relationship(filter_param, filter_value, "tasks")

    def get_status_relationship(
        self, filter_param: str, filter_value: Any, relationship_name: str
    ) -> List[Dict[str, Any]] | Dict[str, Any]:
        return self.get_relationship(filter_param, filter_value, relationship_name)

    def update_status_field(
        self, filter_param: str, filter_value: Any, field_name: str, new_value: Any
    ) -> Dict[str, Any]:
        return self.update_field(filter_param, filter_value, field_name, new_value)

    def update_status_fields(
        self, filter_param: str, filter_value: Any, updated_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self.update_fields(filter_param, filter_value, updated_data)

    def delete_status(self, filter_param: str, filter_value: Any) -> str:
        return self.delete(filter_param, filter_value)

    def delete_all_statuses(self) -> str:
        return self.delete_all()
