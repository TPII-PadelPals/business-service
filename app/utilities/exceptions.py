from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, item: str) -> None:
        detail = f"{item.capitalize()} not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class NotAuthorizedException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized"
        )


class NotEnoughPermissionsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )


class BusinessNotFoundHTTPException(HTTPException):
    def __init__(self, error_message: str) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=error_message)


class BusinessNotFoundException(Exception):
    def __init__(self) -> None:
        super().__init__("Business not found")


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
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not the owner"
        )


class NotUniqueException(HTTPException):
    def __init__(self, item: str) -> None:
        detail = f"{item.capitalize()} already exists."
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class CourtAlreadyReservedException(HTTPException):
    def __init__(self, name: str) -> None:
        detail = f"The court {name} is already reserved."
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class ExternalServiceException(HTTPException):
    def __init__(self, service_name: str, detail: str) -> None:
        detail = f"EXT_SERVICE:{service_name}:{detail}"
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class ExternalServiceInvalidLocalizationException(HTTPException):
    def __init__(self, service_name: str) -> None:
        detail = f"EXT_SERVICE:{service_name}: Invalid location."
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )
