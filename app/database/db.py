from mongoengine import disconnect, register_connection, connection, connect

from config import MONGO_URI, MongoDBCred

def connect_db():
    register_connection(  
            alias=MongoDBCred.ALIAS, # name of connection
            db=MongoDBCred.DB,
            host=MongoDBCred.HOST,
            port=MongoDBCred.PORT,
            username=MongoDBCred.USERNAME,
            password=MongoDBCred.PASSWORD,
            authentication_source=MongoDBCred.AUTHENTICATION_SOURCE,
            authentication_mechanism=MongoDBCred.AUTHENTICATION_MECHANISM
        ) #connecting to mongodb
    print("MongoDB connnection established")

def disconnect_db():
    disconnect()