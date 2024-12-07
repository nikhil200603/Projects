from mongoengine import Document, StringField, EnumField
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"

class User(Document):
    user_name = StringField(max_length=15, required=True, unique=True)
    password = StringField(max_length=100, required=True)
    role = EnumField(RoleEnum, required=True)
    
    meta = {
        'collection': 'users'
    }

class Project(Document):
    project_title = StringField(max_length=100, required=True, unique=True)
    description = StringField(max_length=200)
    status = StringField(choices=['Active', 'Completed', 'Archived'], required=True)
    owner = StringField(max_length=20, required=True)

    meta = {
        'collection': 'projects'
    }
