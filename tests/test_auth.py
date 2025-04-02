import allure
import pytest
from helpers.data import StatusCodes, Messages
from helpers.generators import generate_user


@allure.feature('Авторизация и регистрация')
class TestAuth:
    @allure.title('Успешная регистрация нового пользователя')
    def test_register_valid_user(self, api_client):
        user_data = generate_user()
        response = api_client.register(user_data)
        assert response.status_code == StatusCodes.OK
        assert response.json()['success'] is True
        assert 'accessToken' in response.json()

    @allure.title('Регистрация уже существующего пользователя')
    def test_register_existing_user(self, registered_user, api_client):
        user_data, _ = registered_user
        response = api_client.register(user_data)
        assert response.status_code == StatusCodes.FORBIDDEN
        assert response.json()['message'] == Messages.USER_EXISTS

    @allure.title('Регистрация без обязательного поля: {missing_field}')
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_register_missing_field(self, api_client, missing_field):
        user_data = generate_user()
        user_data.pop(missing_field)
        response = api_client.register(user_data)
        assert response.status_code == StatusCodes.FORBIDDEN
        assert response.json()['message'] == Messages.REQUIRED_FIELDS

    @allure.title('Успешный логин под существующим пользователем')
    def test_login_valid_user(self, registered_user, api_client):
        user_data, _ = registered_user
        response = api_client.login({'email': user_data['email'], 'password': user_data['password']})
        assert response.status_code == StatusCodes.OK
        assert response.json()['success'] is True

    @allure.title('Логин с неверными данными')
    @pytest.mark.parametrize('wrong_data', [
        {'email': 'wrong@test.com', 'password': 'valid_password'},
        {'email': 'valid@test.com', 'password': 'wrong_password'}
    ])
    def test_login_invalid_credentials(self, registered_user, api_client, wrong_data):
        user_data, _ = registered_user
        test_data = {
            'email': wrong_data.get('email', user_data['email']),
            'password': wrong_data.get('password', user_data['password'])
        }
        response = api_client.login(test_data)
        assert response.status_code == StatusCodes.UNAUTHORIZED
        assert response.json()['message'] == Messages.INVALID_CREDS

    @allure.title('Успешный выход из системы')
    def test_logout(self, registered_user):
        _, api_client = registered_user
        response = api_client.logout()
        assert response.status_code == StatusCodes.OK
        assert response.json()['message'] == Messages.LOGOUT_SUCCESS