class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '$cott2x4'
    DB_NAME = 'VelocIT-PROD'
    DB_USERNAME = "root"
    DB_PASSWORD = '$cott2x4'
    
    UPLOAD = "/home/scott.hunt041395/VelocIT/flaskr/app"
    
    
class ProdConf(Config):
    pass 

class DevConf(Config):
    DEBUG = True
    DB_NAME = 'VelocIT-DEV'
    DB_USERNAME = "root"
    DB_PASSWORD = '$cott2x4'
    


class TestConf(Config):
    TESTING = True
    DB_NAME = 'VelocIT-DEV'
    DB_USERNAME = "root"
    DB_PASSWORD = '$cott2x4'