
def is_api_request(request):
    return request.headers.get("Accept") == "application/json" or request.is_json