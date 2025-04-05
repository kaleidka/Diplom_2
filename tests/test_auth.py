import allure
import pytest
from helpers.data import StatusCodes, Messages
from helpers.generators import generate_user
from helpers.api_client import APIClient


@allure.feature('Авторизация и регистрация')
class TestAuth:
    @allure.title('Успешная регистрация нового пользователя')
    def test_register_valid_user(self):
        with allure.step('Подготовить тестовые данные'):
            user_data = generate_user()
            api_client = APIClient()

        with allure.step('Отправить запрос на регистрацию'):
            response = api_client.register(user_data)

        with allure.step('Проверить код ответа и тело'):
            assert response.status_code == StatusCodes.OK
            assert response.json()['success'] is True
            assert 'accessToken' in response.json()

    @allure.title('Регистрация уже существующего пользователя')
    def test_register_existing_user(self, registered_user):
        user_data, _ = registered_user
        api_client = APIClient()

        with allure.step('Отправить запрос на регистрацию с существующими данными'):
            response = api_client.register(user_data)

        with allure.step('Проверить код ответа и сообщение об ошибке'):
            assert response.status_code == StatusCodes.FORBIDDEN
            assert response.json()['message'] == Messages.USER_EXISTS

    @allure.title('Регистрация без обязательного поля: {missing_field}')
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_register_missing_field(self, missing_field):
        with allure.step('Подготовить тестовые данные'):
            user_data = generate_user()
            user_data.pop(missing_field)
            api_client = APIClient()

        with allure.step('Отправить запрос на регистрацию'):
            response = api_client.register(user_data)

        with allure.step('Проверить код ответа и сообщение об ошибке'):
            assert response.status_code == StatusCodes.FORBIDDEN
            assert response.json()['message'] == Messages.REQUIRED_FIELDS

    @allure.title('Успешный логин под существующим пользователем')
    def test_login_valid_user(self, registered_user):
        user_data, _ = registered_user
        api_client = APIClient()

        with allure.step('Отправить запрос на авторизацию'):
            response = api_client.login({
                'email': user_data['email'],
                'password': user_data['password']
            })

        with allure.step('Проверить код ответа и тело'):
            assert response.status_code == StatusCodes.OK
            assert response.json()['success'] is True

    @allure.title('Логин с неверными данными')
    @pytest.mark.parametrize('wrong_data', [
        {'email': 'wrong@test.com', 'password': 'valid_password'},
        {'email': 'valid@test.com', 'password': 'wrong_password'}
    ])
    def test_login_invalid_credentials(self, registered_user, wrong_data):
        user_data, _ = registered_user
        api_client = APIClient()

        with allure.step('Подготовить тестовые данные'):
            test_data = {
                'email': wrong_data.get('email', user_data['email']),
                'password': wrong_data.get('password', user_data['password'])
            }

        with allure.step('Отправить запрос на авторизацию с неверными данными'):
            response = api_client.login(test_data)

        with allure.step('Проверить код ответа и сообщение об ошибке'):
            assert response.status_code == StatusCodes.UNAUTHORIZED
            assert response.json()['message'] == Messages.INVALID_CREDS

    @allure.title('Успешный выход из системы')
    def test_logout(self, registered_user):
        _, api_client = registered_user

        with allure.step('Отправить запрос на выход из системы'):
            response = api_client.logout()

        with allure.step('Проверить код ответа и сообщение'):
            assert response.status_code == StatusCodes.OK
            assert response.json()['message'] == Messages.LOGOUT_SUCCESS