class ServiceError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(ServiceError):
    def __init__(self, entity: str, id: str):
        super().__init__(f"{entity} with ID '{id}' not found", status_code=404)


class RepositoryError(ServiceError):
    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class ExternalServiceError(ServiceError):
    def __init__(self, service_name: str, message: str):
        super().__init__(
            f"External service '{service_name}' failed: {message}",
            status_code=502,
        )
