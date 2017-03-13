from api_classes.api_caller import ApiCaller


class ApiDroppedFileSubmit(ApiCaller):
    endpoint_url = '/api/droppedfilesubmit/:sha256'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_POST
    endpoint_auth_level = ApiCaller.CONST_API_AUTH_LEVEL_DEFAULT
