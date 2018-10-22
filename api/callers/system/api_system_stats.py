from api.callers.api_caller import ApiCaller


class ApiSystemStats(ApiCaller):
    endpoint_url = '/system/stats'
    endpoint_auth_level = ApiCaller.CONST_API_AUTH_LEVEL_DEFAULT
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET
