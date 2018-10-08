from api.callers.api_caller import ApiCaller


class ApiReportEnhancedSummary(ApiCaller):
    endpoint_url = '/report/$id/enhanced-summary'
    endpoint_auth_level = ApiCaller.CONST_API_AUTH_LEVEL_ELEVATED
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET
