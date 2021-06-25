# TODO write overview
# TODO finish class
from pymongo import MongoClient
from db_pass import username, password, database_name, host_name


class DBUser:
    def __init__(self):
        client = MongoClient(host=host_name,
                             port=27017,
                             user=username,
                             password=password,
                             authSource='admin')
        db = client[database_name]

    def get_user_project(self):
        pass

    def get_project_structure(self):
        pass

    def get_part_detail(self):
        pass

    def create_user_project(self):
        pass

    def create_project_part(self):
        pass

    def create_part(self):
        pass

    def create_user(self):
        pass

    def update_project_structure(self):
        pass

    def update_part_detail(self):
        pass

    def update_user_projects(self):
        pass

    def update_user(self):
        pass

    
