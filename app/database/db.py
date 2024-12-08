from mongoengine import disconnect, register_connection, connection, connect

from app.config import MONGO_URI, MongoDBCred, MONGODB_AWS_LAMBDA_URI

def connect_db():
    # register_connection(  
    #         alias=MongoDBCred.ALIAS, # name of connection
    #         db=MongoDBCred.DB,
    #         host=MongoDBCred.HOST,
    #         port=MongoDBCred.PORT,
    #         username=MongoDBCred.USERNAME,
    #         password=MongoDBCred.PASSWORD,
    #         authentication_source=MongoDBCred.AUTHENTICATION_SOURCE,
    #         authentication_mechanism=MongoDBCred.AUTHENTICATION_MECHANISM
    #     ) #connecting to mongodb
    # print("MongoDB connnection established")
    try:
        connect(host=MONGODB_AWS_LAMBDA_URI)
        print("Connection Established")
    except Exception as e:
        print("connection not established")

def disconnect_db():
    disconnect()