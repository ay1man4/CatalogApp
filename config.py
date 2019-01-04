import os


class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
    CSRF_ENABLED = True
    SECRET_KEY = b'\xfe=Hzo\xd1\x9bY_hW1\n\x07\xc6\xff'
    SQLALCHEMY_DATABASE_URI = 'postgresql://ayman:ayman@localhost:5432/catalog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False


class StagingConfig(Config):
    """
    Production configurations
    """
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.db?check_same_thread=False'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    """
    Testing configurations
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://vagrant:vagrant@localhost:5432/catalogdb'
    TESTING = True

app_config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    
}