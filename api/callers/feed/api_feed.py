from api.callers.api_caller import ApiCaller


class ApiFeed(ApiCaller):
    endpoint_url = '/feed/$days/days'
    endpoint_auth_level = ApiCaller.CONST_API_AUTH_LEVEL_ELEVATED
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET
