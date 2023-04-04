class Embedding:

    def __init__(self, user_id: str = None, user_embedding=None) -> None:
        self.user_id = user_id
        self.user_embedding = user_embedding

    def to_dict(self) -> dict:
        return self.__dict__

    def __str__(self) -> str:
        return str(self.to_dict())