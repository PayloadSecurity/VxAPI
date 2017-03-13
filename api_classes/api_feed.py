from api_classes.api_caller import ApiCaller


class ApiFeed(ApiCaller):
    endpoint_url = '/api/feed/:days'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET
