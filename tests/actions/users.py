from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from src.db.models import User
from tests.actions.base import BaseActions


class UserActions(BaseActions):
    def __init__(self, session: Session = None):
        super().__init__(model=User, session=session)

    def create_users_table(self) -> str:
        return self.create_table()

    def drop_users_table(self) -> str:
        return self.drop_table()

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.create_instance(user_data)

    def get_user_by_id(self, filter_value: int) -> Optional[Dict[str, Any]]:
        return self.get_user_by_filter("id", filter_value)

    def get_user_by_username(self, filter_value: str) -> Optional[Dict[str, Any]]:
        return self.get_user_by_filter("username", filter_value)

    def get_user_by_filter(
        self, filter_param: str, filter_value: Any
    ) -> Optional[Dict[str, Any]]:
        return self.filter_by(filter_param, filter_value)

    def get_random_user(self) -> Optional[Dict[str, Any]]:
        return self.get_random()

    def get_user_field(
        self, filter_param: str, filter_value: Any, field_name: str
    ) -> Any:
        return self.get_field_value(filter_param, filter_value, field_name)

    def get_all_users(self) -> Optional[List[Dict[str, Any]]]:
        return self.get_all()

    def get_all_users_by_filter(
        self, filter_param: str, filter_value: Any
    ) -> Optional[List[Dict[str, Any]]]:
        return self.get_all_by_filter(filter_param, filter_value)

    def get_user_role(self, filter_param: str, filter_value: Any) -> Dict[str, Any]:
        return self.get_user_relationship(filter_param, filter_value, "role")

    def get_user_created_tasks(
        self, filter_param: str, filter_value: Any
    ) -> List[Dict[str, Any]]:
        return self.get_user_relationship(filter_param, filter_value, "created_tasks")

    def get_user_assigned_tasks(
        self, filter_param: str, filter_value: Any
    ) -> List[Dict[str, Any]]:
        return self.get_user_relationship(filter_param, filter_value, "assigned_tasks")

    def get_user_relationship(
        self, filter_param: str, filter_value: Any, relationship_name: str
    ) -> List[Dict[str, Any]] | Dict[str, Any]:
        return self.get_relationship(filter_param, filter_value, relationship_name)

    def update_user_field(
        self, filter_param: str, filter_value: Any, field_name: str, new_value: Any
    ) -> Dict[str, Any]:
        return self.update_field(filter_param, filter_value, field_name, new_value)

    def update_user_fields(
        self, filter_param: str, filter_value: Any, updated_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self.update_fields(filter_param, filter_value, updated_data)

    def delete_user(self, filter_param: str, filter_value: Any) -> str:
        return self.delete(filter_param, filter_value)

    def delete_all_users(self) -> str:
        return self.delete_all()
