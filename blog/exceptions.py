from rest_framework.exceptions import APIException

class NoPermission(APIException):
    status_code = 401
    default_detail = 'User does not own the post.'
    default_code = 'Incorrect_User'