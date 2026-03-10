# Configuration file for Chat Application
import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENVIRONMENT = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENVIRONMENT = 'production'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    ENVIRONMENT = 'testing'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
