from face_authentication.config.database import MongodbClient
from face_authentication.constants.database import USER_EMBEDDING_COLLECTION_NAME


class UserEmbeddingData:
    def __init__(self) -> None:
        self.client = MongodbClient()
        self.collection_name = USER_EMBEDDING_COLLECTION_NAME
        self.collection = self.client.database[self.collection_name]

    def save_user_embedding(self, user_id: str, embedding_list) -> None:
        self.collection.insert_one({"user_id": user_id, "user_embed": embedding_list})

    def get_user_embedding(self, user_id: str) -> dict:
        user: dict = self.collection.find_one({"user_id": user_id})
        if user != None:
            return user
        else:
            return None