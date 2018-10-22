from api.callers.api_caller import ApiCaller


class ApiSubmitReanalyze(ApiCaller):
    endpoint_url = '/submit/reanalyze'
    endpoint_auth_level = ApiCaller.CONST_API_AUTH_LEVEL_ELEVATED
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_POST
