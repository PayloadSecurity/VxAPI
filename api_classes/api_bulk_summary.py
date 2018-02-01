from api_classes.api_caller import ApiCaller


class ApiBulkSummary(ApiCaller):
    endpoint_url = '/api/summary'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_POST
