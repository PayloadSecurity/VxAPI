from api.callers.api_caller import ApiCaller


class ApiNssfList(ApiCaller):
    endpoint_url = '/nssf/list'
    endpoint_auth_level = ApiCaller.CONST_API_AUTH_LEVEL_ELEVATED
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_POST
