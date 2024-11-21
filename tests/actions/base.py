from typing import Any, Callable, Dict, List, Optional, Type

from sqlalchemy import Executable, Result, func
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from sqlalchemy.orm import Session

from src.db.models import Base
from src.logger.logger import logger


def check_session(action: Callable) -> Callable:
    def wrapper(self, *args, **kwargs):
        self._check_session()
        return action(self, *args, **kwargs)

    return wrapper


class BaseActions:
    def __init__(self, model: Type[Base], session: Session) -> None:
        self.model = model
        self.session = session

    @check_session
    def create_table(self) -> str:
        try:
            self.model.__table__.create(self.session.get_bind())
            self.session.commit()
            message = f"Table for {self.model.__name__} model created successfully"
            logger.info(message)
            return message
        except SQLAlchemyError as error:
            self.session.rollback()
            error_message = f"Failed to create the table for {self.model.__name__} model: {str(error)}"
            logger.error(error_message)
            raise ValueError(error_message)

    @check_session
    def drop_table(self) -> str:
        try:
            self.model.__table__.drop(self.session.get_bind())
            self.session.commit()
            message = f"Table for {self.model.__name__} model dropped successfully"
            logger.info(message)
            return message
        except SQLAlchemyError as error:
            self.session.rollback()
            error_message = f"Failed to drop the table for {self.model.__name__} model: {str(error)}"
            logger.error(error_message)
            raise ValueError(error_message)

    @check_session
    def create_instance(self, instance_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            instance = self.model(**instance_data)
            self.session.add(instance)
            self.session.commit()
            message = f"Created a new instance of {self.model.__name__} model"
            logger.info(message)
            instance_dict = {
                column.name: getattr(instance, column.name)
                for column in instance.__table__.columns
            }
            return instance_dict
        except SQLAlchemyError as e:
            self.session.rollback()
            error_message = f"Failed to create a new instance of {self.model.__name__} model: {str(e)}"
            logger.error(error_message)
            raise ValueError(error_message)

    @check_session
    def get_all(self) -> Optional[List[Dict[str, Any]]]:
        try:
            instances = self.session.query(self.model).all()
            if instances:
                message = f"Retrieved all instances of {self.model.__name__} model"
                logger.info(message)
                instances_list = []
                for instance in instances:
                    instance_dict = {
                        column.name: getattr(instance, column.name)
                        for column in instance.__table__.columns
                    }
                    instances_list.append(instance_dict)
                return instances_list
            else:
                message = f"No instances found for {self.model.__name__} model"
                logger.info(message)
                return None
        except SQLAlchemyError as e:
            self.session.rollback()
            error_message = (
                f"Failed to retrieve instances of {self.model.__name__} model: {str(e)}"
            )
            logger.error(error_message)
            raise ValueError(error_message)

    @check_session
    def get_all_by_filter(
        self, filter_param: str, filter_value: Any
    ) -> Optional[List[Dict[str, Any]]]:
        try:
            instances = (
                self.session.query(self.model)
                .filter_by(**{filter_param: filter_value})
                .all()
            )
            if instances:
                message = f"Retrieved instances of {self.model.__name__} model with {filter_param}={filter_value}."
                logger.info(message)
                instances_list = []
                for instance in instances:
                    instance_dict = {
                        column.name: getattr(instance, column.name)
                        for column in instance.__table__.columns
                    }
                    instances_list.append(instance_dict)
                return instances_list
            else:
                message = f"No instances found for {self.model.__name__} model with {filter_param}={filter_value}."
                logger.info(message)
                return None
        except SQLAlchemyError as e:
            self.session.rollback()
            error_message = (
                f"Failed to retrieve instances of {self.model.__name__}: {str(e)}"
            )
            logger.error(error_message)
            raise ValueError(error_message)

    @check_session
    def filter_by(
        self, filter_param: str, filter_value: Any
    ) -> Optional[Dict[str, Any]]:
        try:
            instance = (
                self.session.query(self.model)
                .filter_by(**{filter_param: filter_value})
                .first()
            )
            if instance:
                message = f"Retrieved an instance of {self.model.__name__} model with {filter_param}={filter_value}."
                logger.info(message)
                instance_dict = {
                    column.name: getattr(instance, column.name)
                    for column in instance.__table__.columns
                }
                return instance_dict
            else:
                error_message = f"No instance found for {self.model.__name__} model with {filter_param}={filter_value}"
                logger.error(error_message)
                return None
        except SQLAlchemyError as e:
            self.session.rollback()
            error_message = f"Failed to retrieve an instance of {self.model.__name__} model: {str(e)}"
            logger.error(error_message)
            raise ValueError(error_message)

    @check_session
    def get_random(self) -> Optional[Dict[str, Any]]:
        try:
            random_instance = (
                self.session.query(self.model).order_by(func.random()).first()
            )
            if random_instance:
                message = f"Retrieved a random instance of {self.model.__name__} model"
                logger.info(message)
                random_dict = {
                    column.name: getattr(random_instance, column.name)
                    for column in random_instance.__table__.columns
                }
                return random_dict
            else:
                error_message = f"No instance found for {self.model.__name__} model"
                logger.error(error_message)
                return None
        except SQLAlchemyError as e:
            self.session.rollback()
            error_message = f"Failed to retrieve a random instance of {self.model.__name__} model: {str(e)}"
            logger.error(error_message)
            raise ValueError(error_message)

    @check_session
    def get_field_value(
        self, filter_param: str, filter_value: Any, field_name: str
    ) -> Any:
        try:
            instance = (
                self.session.query(self.model)
                .filter_by(**{filter_param: filter_value})
                .first()
            )
            if instance:
                field_value = getattr(instance, field_name)
                if field_value:
                    message = (
                        f"Retrieved the value of the instance field '{field_name}'"
                        f"for {self.model.__name__} model with {filter_param}={filter_value}."
                    )
                    logger.info(message)
                    return field_value
                else:
                    error_message = (
                        f"Could not retrieve the value of the instance field '{field_name}'"
                        f"for {self.model.__name__} model with {filter_param}={filter_value}."
                        f"The field value is not available."
                    )
                    logger.error(error_message)
                    return None
            else:
                error_message = f"No instance found for {self.model.__name__} model with {filter_param}={filter_value}"
                logger.error(error_message)
                raise NoResultFound(error_message)
        except SQLAlchemyError as e:
            self.session.rollback()
            error_message = (
                f"Failed to retrieve the value of the instance field"
                f"of {self.model.__name__} model: {str(e)}"
            )
            logger.error(error_message)
            raise ValueError(error_message)

    @check_session
    def update_field(
        self, filter_param: str, filter_value: Any, field_name: str, field_value: Any
    ) -> Dict[str, Any]:
        try:
            instance = (
                self.session.query(self.model)
                .filter_by(**{filter_param: filter_value})
                .first()
            )
            if instance:
                if hasattr(instance, field_name):
                    setattr(instance, field_name, field_value)
                    self.session.commit()
                    message = (
                        f"Updated the field '{field_name}'"
                        f"for {self.model.__name__} with {filter_param}={filter_value}."
                    )
                    logger.info(message)
                    instance_dict = {
                        column.name: getattr(instance, column.name)
                        for column in instance.__table__.columns
                    }
                    return instance_dict
                else:
                    error_message = (
                        f"The instance of {self.model.__name__} model"
                        f"does not have a field named {field_name}"
                    )
                    logger.error(error_message)
                    raise ValueError(error_message)
            else:
                error_message = f"No instance found for {self.model.__name__} model with {filter_param}={filter_value}"
                logger.error(error_message)
                raise NoResultFound(error_message)
        except SQLAlchemyError as e:
            self.session.rollback()
            error_message = f"Failed to update the field {field_name} for {self.model.__name__} model: {str(e)}"
            logger.error(error_message)
            raise ValueError(error_message)

    @check_session
    def update_fields(
        self, filter_param: str, filter_value: Any, updated_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        try:
            instance = (
                self.session.query(self.model)
                .filter_by(**{filter_param: filter_value})
                .first()
            )
            if instance:
                for field_name, field_value in updated_data.items():
                    if hasattr(instance, field_name):
                        setattr(instance, field_name, field_value)
                    else:
                        error_message = (
                            f"The model {self.model.__name__} model"
                            f"does not have a field named {field_name}"
                        )
                        logger.error(error_message)
                        raise ValueError(error_message)
                self.session.commit()
                message = (
                    f"Updated multiple fields for {self.model.__name__} model"
                    f"with {filter_param}={filter_value}."
                )
                logger.info(message)
                instance_dict = {
                    column.name: getattr(instance, column.name)
                    for column in instance.__table__.columns
                }
                return instance_dict
            else:
                error_message = f"No instance found for {self.model.__name__} model with {filter_param}={filter_value}"
                logger.error(error_message)
                raise NoResultFound(error_message)
        except SQLAlchemyError as e:
            self.session.rollback()
            error_message = f"Failed to update multiple fields for {self.model.__name__} model: {str(e)}"
            logger.error(error_message)
            raise ValueError(error_message)

    @check_session
    def delete(self, filter_param: str, filter_value: Any) -> str:
        try:
            instance = (
                self.session.query(self.model)
                .filter_by(**{filter_param: filter_value})
                .first()
            )
            if instance:
                self.session.delete(instance)
                self.session.commit()
                message = "The instance was successfully deleted."
                logger.info(message)
                return message
            else:
                error_message = f"No instance found for {self.model.__name__} model with {filter_param}={filter_value}"
                logger.error(error_message)
                raise NoResultFound(error_message)
        except IntegrityError:
            self.session.rollback()
            error_message = "Cannot delete the instance due to integrity constraints."
            logger.error(error_message)
            raise ValueError(error_message)
        except SQLAlchemyError as e:
            self.session.rollback()
            error_message = f"Failed to delete the instance for {self.model.__name__} model: {str(e)}"
            logger.error(error_message)
            raise ValueError(error_message)

    @check_session
    def delete_all(self) -> str:
        try:
            self.session.query(self.model).delete()
            self.session.commit()
            message = f"All instances with {self.model.__name__} model were successfully deleted."
            logger.info(message)
            return message
        except SQLAlchemyError as e:
            self.session.rollback()
            error_message = f"Failed to delete all records for {self.model.__name__} model: {str(e)}"
            logger.error(error_message)
            raise ValueError(error_message)

    @check_session
    def get_relationship(
        self, filter_param: str, filter_value: Any, relationship_name: str
    ) -> Optional[Any]:
        try:
            instance = (
                self.session.query(self.model)
                .filter_by(**{filter_param: filter_value})
                .first()
            )
            if instance:
                relationship = getattr(instance, relationship_name, None)
                if relationship is not None:
                    if isinstance(relationship, list):
                        related_instances = []
                        for related_instance in relationship:
                            related_dict = {
                                column.name: getattr(related_instance, column.name)
                                for column in related_instance.__table__.columns
                            }
                            related_instances.append(related_dict)
                        message = f"Retrieved {relationship_name} for {self.model.__name__} instance."
                        logger.info(message)
                        return related_instances
                    elif relationship is not None:
                        related_instance = {
                            column.name: getattr(relationship, column.name)
                            for column in relationship.__table__.columns
                        }
                        message = f"Retrieved {relationship_name} for {self.model.__name__} instance."
                        logger.info(message)
                        return related_instance
                else:
                    message = f"No relationship found for {self.model.__name__} model with name {relationship_name}."
                    logger.info(message)
                    return None
            else:
                error_message = f"No instance found for {self.model.__name__} model with {filter_param}={filter_value}"
                logger.error(error_message)
                raise NoResultFound(error_message)
        except SQLAlchemyError as e:
            self.session.rollback()
            error_message = (
                f"Failed to retrieve relationship {relationship_name} for {self.model.__name__} model:"
                f"{str(e)}"
            )
            logger.error(error_message)
            raise ValueError(error_message)

    @check_session
    def execute_query(self, query: Executable) -> Result:
        try:
            result = self.session.execute(query)
            message = "Executed SQL query successfully."
            logger.info(message)
            return result
        except SQLAlchemyError as e:
            self.session.rollback()
            error_message = f"Failed to execute SQL query: {str(e)}"
            logger.error(error_message)
            raise ValueError(error_message)

    def _check_session(self) -> None:
        if self.session is None:
            error_message = "No session provided. You must pass a valid session to perform database operations."
            raise ValueError(error_message)
