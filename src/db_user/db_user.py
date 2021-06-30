"""
Database accessor class

This should be the only module that touches the database
"""
from pymongo import MongoClient
from .db_pass import USERNAME, PASSWORD, DATABASE_NAME, HOST_NAME


class DBUser:
    """Only class that touches database"""

    def __init__(self):
        client = MongoClient(
            host=HOST_NAME,
            port=27017,
            user=USERNAME,
            password=PASSWORD,
            authSource="admin",
        )
        self.database = client[DATABASE_NAME]

    def get_user_projects(self, username):
        """READS user collection and pull all projects user has access to"""
        collection = self.database["users"]
        query = {"username": username}
        return collection.find_one(query)

    def get_project_structure(self, project_id):
        """
        READS parts collection and pulls all parts under a given project name

        Traverses the linked list and created a ragged array of the project structure
        """
        collection = self.database["parts"]
        query = {"project-id": project_id}
        return collection.find(query)

    # def get_part_detail(self):
    #     """READS parts collection for certain part number"""
    #     pass

    # def create_user_project(self):
    #     """WRITES new project to projects collection, updates user to add project"""
    #     pass

    # def create_project_part(self):
    #     pass

    # def create_part(self):
    #     pass

    # def create_user(self):
    #     pass

    # def update_project_structure(self):
    #     pass

    # def update_part_detail(self):
    #     pass

    # def update_user_projects(self):
    #     pass

    # def update_user(self):
    #     pass
