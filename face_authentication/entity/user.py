import uuid


class User:
    def __init__(
        self,
        name: str,
        username: str,
        email_id: str,
        phone_no: str,
        password: str,
        uuid_: str = None,
    ):
        self.name = name
        self.username = username
        self.email_id = email_id
        self.phone_no = phone_no
        self.password = password
        self.uuid_ = uuid_
        if not self.uuid_:
            self.uuid_ = str(uuid.uuid4()) + str(uuid.uuid4())[0:4]

    def to_dict(self) -> dict:
        return self.__dict__

    def __str__(self) -> str:
        return str(self.to_dict())