from fastapi import status

# Common responses
NOT_ENOUGH_PERMISSIONS = {
    status.HTTP_403_FORBIDDEN: {"description": "Not enough permissions"}
}

# Item responses
ITEM_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "Item not found"}}
ITEM_RESPONSES = {**ITEM_NOT_FOUND, **NOT_ENOUGH_PERMISSIONS}

# Business responses
BUSINESS_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "Business not found"}}
BUSINESS_RESPONSES = {**BUSINESS_NOT_FOUND, **NOT_ENOUGH_PERMISSIONS}
BUSINESS_CREATE = {
    status.HTTP_404_NOT_FOUND: {"description": "Business not found"},
    status.HTTP_201_CREATED: {},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "The necessary data (owner public ID) has not been provided"
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Error with Google location service communication"
    },
}

# available_date
AVAILABLE_DATE_UNAUTHORIZED_OWNED = {
    status.HTTP_401_UNAUTHORIZED: {"description": "User is not the owner"}
}
AVAILABLE_DATE_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {"description": "Business or court not found"}
}
AVAILABLE_DATE_NOT_UNIQUE = {
    status.HTTP_409_CONFLICT: {"description": "Available date already created"}
}
AVAILABLE_DATE_NOT_ACCEPTABLE = {
    status.HTTP_406_NOT_ACCEPTABLE: {"description": "The information is not acceptable"}
}
AVAILABLE_DATE_ALREADY_RESERVED = {
    status.HTTP_409_CONFLICT: {"description": "Available date already created"}
}

AVAILABLE_DATE_POST_RESPONSES = {
    **AVAILABLE_DATE_NOT_FOUND,
    **AVAILABLE_DATE_UNAUTHORIZED_OWNED,
    **AVAILABLE_DATE_NOT_UNIQUE,
    **AVAILABLE_DATE_NOT_ACCEPTABLE,
}
AVAILABLE_DATE_DELETE_RESPONSES = {
    **AVAILABLE_DATE_NOT_FOUND,
    **AVAILABLE_DATE_UNAUTHORIZED_OWNED,
}
AVAILABLE_DATE_GET_RESPONSES = {
    status.HTTP_200_OK: {
        "description": "Returns a list of available matches given a date"
    }
}
AVAILABLE_DATE_PATCH_RESPONSES = {
    **AVAILABLE_DATE_NOT_FOUND,
    **AVAILABLE_DATE_ALREADY_RESERVED,
}
