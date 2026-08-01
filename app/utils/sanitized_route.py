import json
from typing import Callable
from fastapi import Request, Response
from fastapi.routing import APIRoute


class SanitizedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_handler = super().get_route_handler()

        async def custom_handler(request: Request) -> Response:
            raw_body = await request.body()
            try:
                data = json.loads(raw_body, strict=False)
                request._body = json.dumps(data).encode("utf-8")
            except json.JSONDecodeError:
                pass  # let FastAPI's normal handler raise its usual clear error
            return await original_handler(request)

        return custom_handler
