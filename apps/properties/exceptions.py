from rest_framework.exceptions import APIException


class PropertyNotFound(APIException):
    status_code = 404
    default_detail = "The requested Property does not exist"
