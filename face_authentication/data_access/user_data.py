from face_authentication.config.database import MongodbClient
from face_authentication.constants.database import USER_COLLECTION_NAME
from face_authentication.entity.user import User


class UserData:

    def __init__(self) -> None:
        self.client = MongodbClient()
        self.collection_name = USER_COLLECTION_NAME
        self.collection = self.client.database[self.collection_name]

    def save_user(self, user: User) -> None:
        self.collection.insert_one(user)

    def get_user(self, query: dict):
        user = self.collection.find_one(query)
        return user
