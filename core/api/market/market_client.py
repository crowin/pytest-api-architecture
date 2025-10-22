import allure
from requests import Session

from core.common.user import User
from core.common.config import Config


class MarketApi:

    def __init__(self, user: User):
        self.username = user.username
        self.session = Session()
        self.session.headers.update({'Authorization': f'Bearer {user.token}'})
        self.base_url = Config.MARKET_API_URL

    @allure.step('Get user cart - GET /cart')
    def get_cart(self):
        return self.session.get(f'{self.base_url}/cart')

    @allure.step('Clear user cart - DELETE /cart')
    def clear_cart(self):
        return self.session.delete(f'{self.base_url}/cart')

    @allure.step('Remove product from cart - DELETE /cart/{product_id}')
    def remove_product_from_cart(self, product_id):
        return self.session.delete(f'{self.base_url}/cart/{product_id}')

    @allure.step('Add product to cart - POST /cart')
    def add_product_to_cart(self, item_id, quantity=1):
        return self.session.put(f'{self.base_url}/cart', json={'itemId': item_id, 'quantity': quantity})

    @allure.step("Get products - GET /products")
    def get_products(self, page=0, limit=8):
        return self.session.get(f'{self.base_url}/products', params={'page': page, 'limit': limit})

