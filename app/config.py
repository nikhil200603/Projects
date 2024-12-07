

MONGO_URI="mongodb://assessment_project_user:assessment_project_pass@localhost:27017/assessment_project?authSource=admin"

class JwtCred:
    JWT_SECRET = "039adc7ef49111e10e5325c33b37dbd044493ecb09d7e926fe6e5d4ab0dcce1d"
    JWT_ALGORITHM = "HS256"
    JWT_VALIDITY = 60*60 
    ACCESS_TOKEN = "access_token"

class MongoDBCred:
    ALIAS = 'default'
    DB = 'assessment_project'
    HOST = 'localhost'
    PORT = 27017
    USERNAME = 'assessment_project_user'
    PASSWORD = 'assessment_project_pass'
    AUTHENTICATION_SOURCE = 'admin'
    AUTHENTICATION_MECHANISM = 'SCRAM-SHA-1'