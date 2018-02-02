from api_classes.api_caller import ApiCaller


class ApiNssfList(ApiCaller):
    endpoint_url = '/api/nssf/list'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_POST
    endpoint_auth_level = ApiCaller.CONST_API_AUTH_LEVEL_ELEVATED
