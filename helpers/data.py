class StatusCodes:
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_ERROR = 500


class Messages:
    REQUIRED_FIELDS = 'Email, password and name are required fields'
    USER_EXISTS = 'User already exists'
    INVALID_CREDS = 'email or password are incorrect'
    UNAUTHORIZED = 'You should be authorised'
    NO_INGREDIENTS = 'Ingredient ids must be provided'
    LOGOUT_SUCCESS = 'Successful logout'