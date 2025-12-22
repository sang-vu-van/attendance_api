from chalice import Response


def json_error(message: str, status_code: int = 400, details=None):
    body = {"error": message}
    if details is not None:
        body["details"] = details
    return Response(
        body=body, status_code=status_code, headers={"Content-Type": "application/json"}
    )
