
class DevelopmentConfig:
    db_password = "your_password"
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{db_password}@localhost/mechanic_shop_db'
    DEBUG = True

class TestingConfig:
    pass

class ProductionConfig:
    pass
