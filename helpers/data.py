class URLs:
    BASE = 'https://stellarburgers.nomoreparties.site/api'
    REGISTER = f'{BASE}/auth/register'
    LOGIN = f'{BASE}/auth/login'
    LOGOUT = f'{BASE}/auth/logout'
    USER = f'{BASE}/auth/user'
    INGREDIENTS = f'{BASE}/ingredients'
    ORDERS = f'{BASE}/orders'


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