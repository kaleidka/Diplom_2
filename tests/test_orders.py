import allure
from helpers.api_client import APIClient
from helpers.data import StatusCodes

@allure.feature('Управление заказами')
class TestOrders:
    @allure.title('Создание заказа с авторизацией и ингредиентами')
    def test_create_order_with_auth(self, registered_user, ingredients):
        _, api_client = registered_user
        response = api_client.create_order(ingredients)
        assert response.status_code == StatusCodes.OK
        assert response.json()['success'] is True
        assert 'order' in response.json()
        assert isinstance(response.json()['order']['number'], int)

    @allure.title('Попытка создания заказа без авторизации')
    def test_create_order_without_auth(self, ingredients):
        api_client = APIClient()
        response = api_client.create_order(ingredients, auth=False)
        assert response.status_code in [401, 403], f"Expected 401 or 403, got {response.status_code}"
        assert 'message' in response.json()

    @allure.title('Попытка создания заказа без ингредиентов')
    def test_create_order_no_ingredients(self, registered_user):
        _, api_client = registered_user
        response = api_client.create_order([])
        assert response.status_code in [StatusCodes.BAD_REQUEST, StatusCodes.FORBIDDEN]
        assert 'message' in response.json()

    @allure.title('Попытка создания заказа с неверным хешем ингредиентов')
    def test_create_order_invalid_ingredients(self, registered_user):
        _, api_client = registered_user
        response = api_client.create_order(["invalid_hash_123"])
        assert response.status_code in [StatusCodes.INTERNAL_ERROR, StatusCodes.FORBIDDEN]

    @allure.title('Попытка получения заказов без авторизации')
    def test_get_orders_without_auth(self):
        api_client = APIClient()
        response = api_client.get_orders()
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @allure.title('Получение списка заказов авторизованного пользователя')
    def test_get_orders_with_auth(self, registered_user, ingredients):
        _, api_client = registered_user
        api_client.create_order(ingredients)
        response = api_client.get_orders()
        assert response.status_code == StatusCodes.OK
        assert response.json()['success'] is True
        assert 'orders' in response.json()