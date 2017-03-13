from api_classes.api_caller import ApiCaller


class ApiSystemState(ApiCaller):
    endpoint_url = '/system/state'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET
    endpoint_auth_level = ApiCaller.CONST_API_AUTH_LEVEL_DEFAULT
