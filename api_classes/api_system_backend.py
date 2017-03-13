from api_classes.api_caller import ApiCaller


class ApiSystemBackend(ApiCaller):
    endpoint_url = '/system/backend'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET
    endpoint_auth_level = ApiCaller.CONST_API_AUTH_LEVEL_DEFAULT
