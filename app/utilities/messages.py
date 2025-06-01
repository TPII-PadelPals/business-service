from fastapi import status

# Common responses
NOT_ENOUGH_PERMISSIONS = {
    status.HTTP_403_FORBIDDEN: {"description": "Permisos insuficientes"}
}

# Item responses
ITEM_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "No se encontró Item"}}
ITEM_RESPONSES = {**ITEM_NOT_FOUND, **NOT_ENOUGH_PERMISSIONS}

# Business responses
BUSINESS_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {"description": "No se encontró establecimiento"}
}
BUSINESS_RESPONSES = {**BUSINESS_NOT_FOUND, **NOT_ENOUGH_PERMISSIONS}
BUSINESS_CREATE = {
    status.HTTP_404_NOT_FOUND: {"description": "No se encontró establecimiento"},
    status.HTTP_201_CREATED: {
        "description": "Business created",
        "content": {
            "application/json": {
                "examples": {
                    "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "latitude": 0.1,
                    "longitude": 0.4,
                    "name": "Padel SI",
                    "location": "Av Paseo Colon 850",
                    "id": "3fa85f64-5747-4562-b3fc-2c963f66afa8",
                }
            }
        },
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "The necessary data (owner public ID) has not been provided"
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Error with Google location service communication"
    },
}
BUSINESS_UPDATE = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "No autorizado. Usuario no es el dueño"
    },
    **BUSINESS_RESPONSES,
}

COURT_UPDATE = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "No autorizado. Usuario no es el dueño"
    },
    status.HTTP_404_NOT_FOUND: {"description": "Court or Business, not found"},
    status.HTTP_200_OK: {"description": "Returns court updated."},
}

COURT_EXTENDED_GET = {
    status.HTTP_200_OK: {
        "description": "Get court extended with business info.",
        "content": {
            "application/json": {
                "example": {
                    "data": [
                        {
                            "business_public_id": "98671492-667d-4b48-a77e-a92f0519ded1",
                            "owner_id": "11f19bef-8e11-4ab3-9aaa-bc4c15def106",
                            "latitude": 0.3,
                            "longitude": 0.4,
                            "court_public_id": "b2b4e866-d7aa-4886-b0d6-622f64769ee6",
                            "name": "API Court A",
                            "price_per_hour": "100.00",
                            "business_name": "API Court Business 1",
                            "business_location": "API Court Location 1",
                        }
                    ],
                    "count": 1,
                }
            }
        },
    },
    status.HTTP_400_BAD_REQUEST: {
        "description": "Both business_public_id and user_id must be provided together or both omitted."
    },
    status.HTTP_404_NOT_FOUND: {"description": "Court or Business, not found"},
}

# available_date
AVAILABLE_DATE_UNAUTHORIZED_OWNED = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "No autorizado. Usuario no es el dueño"
    }
}
AVAILABLE_DATE_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {"description": "Business or court not found"}
}
AVAILABLE_DATE_NOT_UNIQUE = {
    status.HTTP_409_CONFLICT: {"description": "Available date already created"}
}
AVAILABLE_DATE_NOT_ACCEPTABLE = {
    status.HTTP_406_NOT_ACCEPTABLE: {"description": "Información no aceptada"}
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
