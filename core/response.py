from rest_framework.response import Response


def success_response(
    data=None,
    message: str = "Success.",
    status: int = 200,
    pagination: dict | None = None,
    **kwargs
) -> Response:
    body = {
        "success": True,
        "status": status,
        "message": message,
        "data": data,
    }
    if pagination is not None:
        body["pagination"] = pagination

    return Response(body, status=status , **kwargs)
