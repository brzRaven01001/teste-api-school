class Config:
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'chave_secreta'
    DATABASE_PATH = 'data/banco.db'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DATABASE_PATH = 'data/teste_banco.db'

class ProductionConfig(Config):
    DEBUG = False
