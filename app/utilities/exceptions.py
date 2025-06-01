from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, item: str) -> None:
        detail = f"No se encontró {item.capitalize()}"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class NotAuthorizedException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado"
        )


class NotEnoughPermissionsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permisos insuficientes"
        )


class BusinessNotFoundHTTPException(HTTPException):
    def __init__(self, error_message: str) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=error_message)


class BusinessNotFoundException(Exception):
    def __init__(self) -> None:
        super().__init__("No se encontró establecimiento")


class UnauthorizedPadelCourtOperationException(Exception):
    pass


class NotAcceptableException(HTTPException):
    def __init__(self, reason: str) -> None:
        super().__init__(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"The information is not acceptable. Reason: {reason}.",
        )


class UnauthorizedUserException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado. Usuario no es el dueño",
        )


class NotUniqueException(HTTPException):
    def __init__(self, item: str) -> None:
        detail = f"{item.capitalize()} ya existente."
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class CourtAlreadyReservedException(HTTPException):
    def __init__(self, name: str) -> None:
        detail = f"La cancha {name} está reservada."
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class ExternalServiceException(HTTPException):
    def __init__(self, service_name: str, detail: str) -> None:
        detail = f"EXT_SERVICE:{service_name}:{detail}"
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class ExternalServiceInvalidLocalizationException(HTTPException):
    def __init__(self, service_name: str) -> None:
        detail = f"EXT_SERVICE:{service_name}:Dirección inválida."
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )
