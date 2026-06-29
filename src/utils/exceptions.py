from typing import Any, Dict, List, Optional


class CustomException(Exception):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class AppException(CustomException):
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)


class InvalidIdFormatError(AppException):
    def __init__(self, entity_id: str, reason: Optional[str] = None):
        self.entity_id = entity_id
        message = f"Invalid ID format: {entity_id}"
        if reason:
            message += f" ({reason})"
        super().__init__(message, {"entity_id": entity_id, "reason": reason})


class EntityNotFoundError(AppException):
    def __init__(self, entity_type: str, entity_id: str, message: Optional[str] = None):
        self.entity_type = entity_type
        self.entity_id = entity_id
        default_message = f"{entity_type} not found with ID: {entity_id}"
        super().__init__(
            message or default_message,
            {"entity_type": entity_type, "entity_id": entity_id},
        )


class ItemNotFoundError(EntityNotFoundError):
    def __init__(self, item_id: str, message: Optional[str] = None):
        super().__init__("Item", item_id, message)


class BatchOperationError(AppException):
    def __init__(
        self,
        message: str,
        successful_ids: List[str],
        failed_ids: List[str],
        errors: Dict[str, str],
    ):
        self.successful_ids = successful_ids
        self.failed_ids = failed_ids
        self.errors = errors
        super().__init__(
            message,
            {
                "successful_ids": successful_ids,
                "failed_ids": failed_ids,
                "errors": errors,
            },
        )


class ValidationError(AppException):
    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        details = {"field": field} if field else {}
        super().__init__(message, details)
