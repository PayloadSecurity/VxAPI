from api.callers.api_caller import ApiCaller


class ApiScanUrlForAnalysis(ApiCaller):
    endpoint_url = '/quick-scan/url-for-analysis'
    endpoint_auth_level = ApiCaller.CONST_API_AUTH_LEVEL_RESTRICTED
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_POST
