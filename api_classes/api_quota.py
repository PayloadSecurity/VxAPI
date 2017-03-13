from api_classes.api_caller import ApiCaller


class ApiQuota(ApiCaller):
    endpoint_url = '/api/quota'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET
