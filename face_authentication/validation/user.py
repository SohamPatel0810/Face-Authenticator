import re
import sys
from typing import Optional

from passlib.context import CryptContext

from face_authentication.data_access.user_data import UserData
from face_authentication.entity.user import User
from face_authentication.exception import AppException
from face_authentication.logger import logging

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginValidation:
  
    def __init__(self, email_id: str, password: str):
        """
        Args:
            email_id (str): _description_
            password (str): _description_
        """
        self.email_id = email_id
        self.password = password
        self.regex = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )

    def validate(self) -> bool:
        """validate: This validates the user input
        Args:
            email_id (str): email_id of the user
            password (str): password of the user
        """
        try:
            msg = ""
            if not self.email_id:
                msg += "Email Id is required"
            if not self.password:
                msg += "Password is required"
            if not self.is_email_valid():
                msg += "Invalid Email Id"
            return msg
        except Exception as e:
            raise e

    def is_email_valid(self) -> bool:
        if re.fullmatch(self.regex, self.email_id):
            return True
        else:
            return False

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify hashed password and plain password.
        Args:
            plain_password (str): _description_
            hashed_password (str): _description_
        Returns:
            bool: _description_
        """
        return bcrypt_context.verify(plain_password, hashed_password)

    def validate_login(self) -> dict:

        """This checks all the validation conditions for the user registration"""
        if len(self.validate()) != 0:
            return {"status": False, "msg": self.validate()}
        return {"status": True}

    def authenticate_user_login(self) -> Optional[str]:
        """This authenticates the user and returns the token if the user is authenticated
        Args:
            email_id (str): _description_
            password (str): _description_
        """
        try:

            logging.info("Authenticating the user details.....")
            if self.validate_login()["status"]:
                userdata = UserData()
                logging.info("Fetching the user details from the database.....")
                user_details = userdata.get_user({"email_id": self.email_id})
                if not user_details:
                    logging.info("User not found!")
                    return False
                if not self.verify_password(self.password, user_details["password"]):
                    logging.info("Password is incorrect")
                    return False
                logging.info("User authenticated successfully....")
                return user_details
            return False
        except Exception as e:
            raise AppException(e, sys) from e


class RegisterValidation:

    """ This authenticates the user and returns the status - SignUp process. """

    def __init__(self, user: User) -> None:
        try:
            self.user = user
            self.regex = re.compile(
                r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
            )
            self.uuid = self.user.uuid_
            self.userdata = UserData()
            self.bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        except Exception as e:
            raise e

    def validate(self) -> bool:

        """This checks all the validation conditions for the user registration
        Returns:
            _type_: string
        """
        try:
            msg = ""
            if self.user.name == None:
                msg += "Name is required"

            if self.user.username == None:
                msg += "Username is required"

            if self.user.email_id == None:
                msg += "Email is required"

            if self.user.phone_no == None:
                msg += "Phone Number is required"

            if self.user.password == None:
                msg += "Password is required"


            if not self.is_email_valid():
                msg += "Email is not valid"

            if not self.is_password_valid():
                msg += "Length of the pass`word should be between 8 and 16"

            if not self.is_details_exists():
                msg += "User already exists"

            return msg
        except Exception as e:
            raise e

    def is_email_valid(self) -> bool:
        """_summary_: This validates the email id
        Returns:
            bool: True if the email id is valid else False
        """
        if re.fullmatch(self.regex, self.user.email_id):
            return True
        else:
            return False

    def is_password_valid(self) -> bool:
        if len(self.user.password) >= 8 and len(self.user.password) <= 16:
            return True
        else:
            return False

    def is_details_exists(self) -> bool:
        username_val = self.userdata.get_user({"username": self.user.username})
        emailid_val = self.userdata.get_user({"email_id": self.user.email_id})
        uuid_val = self.userdata.get_user({"UUID": self.uuid})
        if username_val == None and emailid_val == None and uuid_val == None:
            return True
        return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        return bcrypt_context.hash(password)

    def validate_registration(self) -> bool:

        """This checks all the validation conditions for the user registration
        """
        if len(self.validate()) != 0:
            return {"status": False, "msg": self.validate()}
        return {"status": True}

    def authenticate_user_registration(self) -> bool:
        """_summary_: This saves the user details in the database
        only after validating the user details
        Returns:
            bool: _description_
        """
        try:
            logging.info("Validating the user details while Registration.....")
            if self.validate_registration()["status"]:
                logging.info("Generating the password hash.....")
                hashed_password: str = self.get_password_hash(self.user.password)
                user_data_dict: dict = {
                    "name": self.user.name,
                    "username": self.user.username,
                    "password": hashed_password,
                    "email_id": self.user.email_id,
                    "phone_no": self.user.phone_no,
                    "uuid": self.uuid,
                }
                logging.info("Saving the user details in the database.....")
                self.userdata.save_user(user_data_dict)
                logging.info("Saving the user details in the database completed.....")
                return {"status": True, "msg": "User registered successfully"}
            logging.info("Validation failed while Registration.....")
            return {"status": False, "msg": self.validate()}
        except Exception as e:
            raise 