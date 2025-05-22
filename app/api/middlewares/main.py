from urllib.parse import parse_qs, urlencode

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class HeaderToQueryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        scope = request.scope
        headers = dict(scope["headers"])
        query_string = scope["query_string"].decode()

        query_params = parse_qs(query_string)

        x_user_id = headers.get(b"x-user-id")
        if x_user_id:
            user_id_value = x_user_id.decode()
            if "owner_id" not in query_params:
                query_params["owner_id"] = [user_id_value]

        new_query_string = urlencode(query_params, doseq=True)
        scope["query_string"] = new_query_string.encode()

        return await call_next(request)
