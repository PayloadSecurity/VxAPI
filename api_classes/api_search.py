from api_classes.api_caller import ApiCaller


class ApiSearch(ApiCaller):
    endpoint_url = '/api/search'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET
