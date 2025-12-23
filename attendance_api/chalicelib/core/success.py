def json_ok(data=None, status=200):
    body = {
        "success": True,
    }
    if data is not None:
        body["data"] = data
        return body, status
