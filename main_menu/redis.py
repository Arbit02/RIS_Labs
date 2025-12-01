from redis_config import RedisConfig
from cart_with_config import JSONConfigCart

class RedisCart:
    def __init__(self):
        self.cart = None

    def init_app(self, app):
        config_file = app.config.get('REDIS_CONFIG_FILE', '../data/redis_config.json')
        self.cart = JSONConfigCart(config_file)

redis_cart = RedisCart()