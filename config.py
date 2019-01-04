import os


class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
    CSRF_ENABLED = True
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
    TESTING = True

app_config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    
}