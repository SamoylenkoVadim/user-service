
def is_api_request(request):
    return request.headers.get("Accept") == "application/json" or request.is_json


validation_schema = {
    "type": "object",
    "properties": {
        "firstName": {"type": "string", "nullable": True},
        "lastName": {"type": "string", "nullable": True},
        "emails": {"type": "array", "items": {"type": "string", "nullable": True}},
        "phone_numbers": {"type": "array", "items": {"type": "string", "nullable": True}}
    },
    "required": []
}