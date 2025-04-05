
class DevelopmentConfig:
    db_password = "yourpassword"
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{db_password}@localhost/mechanic_shop_db'
    DEBUG = True
    CACHE_TYPE = "SimpleCache"

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = "SimpleCache"

class ProductionConfig:
    pass
