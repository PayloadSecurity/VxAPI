from api_classes.api_caller import ApiCaller


class ApiUrlHash(ApiCaller):
    endpoint_url = '/api/url-hash'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_POST
    endpoint_auth_level = ApiCaller.CONST_API_AUTH_LEVEL_RESTRICTED
