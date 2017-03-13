from api_classes.api_caller import ApiCaller


class ApiRelationships(ApiCaller):
    endpoint_url = '/api/relationships/:sha256'
    request_method_name = ApiCaller.CONST_REQUEST_METHOD_GET
