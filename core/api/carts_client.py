import allure
from requests import Session

from core.api.user import User
from core.config import Config


class CartsApi:

    def __init__(self, user: User):
        self.username = user.username
        self.session = Session()
        self.session.headers.update({'Authorization': f'Bearer {user.token}'})
        self.base_url = Config.CARTS_API_URL

    @allure.step('Get carts')
    def get_carts(self):
        return self.session.get(self.base_url)

    @allure.step('Get cart by id')
    def get_cart(self, cart_id: int):
        return self.session.get(f'{self.base_url}/{cart_id}')

    @allure.step('Get user carts')
    def get_user_carts(self, user_id: int):
        return self.session.get(f'{self.base_url}/user/{user_id}')

