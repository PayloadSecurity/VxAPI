class VxError(Exception):
    pass


class OptionNotDeclaredError(VxError):
    pass


class ResponseObjectNotExistError(VxError):
    pass


class FilesSavingMethodNotDeclaredError(VxError):
    pass


class FailedFileSavingError(VxError):
    pass


class ResponseTextContentTypeError(VxError):
    pass


class UrlBuildError(VxError):
    pass


class ExceededApiLimitsError(VxError):
    pass


class MissingConfigurationError(VxError):
    pass


class RetrievingApiKeyDataError(VxError):
    pass


class ReachedApiLimitError(VxError):
    pass


class JsonParseError(VxError):
    pass


class ConfigError(VxError):
    pass
