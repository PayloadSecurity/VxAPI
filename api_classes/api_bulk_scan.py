from api_classes.api_caller import ApiCaller


class ApiBulkScan(ApiCaller):
    endpoint_url = '/api/scan'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_POST
