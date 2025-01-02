from fastapi.responses import Response

from src.api.schema.base import MessageSchema

MESSAGE_500 = Response(
    status_code=500,
    content=MessageSchema(message="Internal server error").model_dump_json(),
    headers={"Content-Type": "application/json"},
)
