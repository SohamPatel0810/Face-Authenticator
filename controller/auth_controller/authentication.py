from datetime import datetime, timedelta
import string
import random
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, Response, status
from jose import JWTError, jwt
from pydantic import BaseModel
from starlette.responses import JSONResponse, RedirectResponse

from face_authentication.validation.user import LoginValidation, RegisterValidation
from face_authentication.constants.auth import ALGORITHM, SECRET_KEY
from face_authentication.entity.user import User
from face_authentication.data_access.user_data import UserData


class Login(BaseModel):
    """Base model for login
    """

    email_id: str
    password: str


class Register(BaseModel):
    """
    Base model for register
    """

    name: str
    username: str
    email_id: str
    phone_no: int
    password: str


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={"401": {"description": "Not Authorized!!!"}},
)


# Calling the logger for Database read and insert operations


async def get_current_user(request: Request):
    """This function is used to get the current user
    Args:
        request (Request): Request from the route
    Returns:
        dict: Returns the username and uuid of the user
    """
    try:
        # secret_key = SECRET_KEY
        # algorithm = ALGORITHM

        email = request.cookies.get("email_id")
        if email is None:
            return None

        userdata = UserData()
        payload = userdata.get_user({"email_id": email})

        user = {"username":payload["username"], "user_id":payload["uuid"]}

        if user is None:
            return logout(request)
        return {"user": user}
    except JWTError:
        raise HTTPException(status_code=404, detail="Detail Not Found")
    except Exception as e:
        msg = "Error while getting current user"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": msg}
        )
        return response


def create_access_token() -> str:
    """This function is used to create the access token"""
    try:
        res = ''.join(random.choices(string.ascii_letters, k=16))
        return str(res)
    except Exception as e:
        raise e


@router.post("/token")
async def login_for_access_token(response: Response, login) -> dict:
    """Set the access token
    Returns:
        dict: response
    """

    try:
        user_validation = LoginValidation(login.email_id, login.password)
        user: Optional[str] = user_validation.authenticate_user_login()
        if not user:
            return {"status": False, "uuid": None, "response": response}
        token = create_access_token()
        response.set_cookie(key="access_token", value=token, httponly=True)
        response.set_cookie(key="email_id", value=login.email_id, httponly=True)
        return {"status": True, "uuid": user["uuid"], "response": response}
    except Exception as e:
        msg = "Failed to set access token"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": msg}
        )
        return {"status": False, "uuid": None, "response": response}


@router.get("/", response_class=JSONResponse)
async def authentication_page(request: Request):
    """Login GET route
    Returns:
        _type_: JSONResponse
    """
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Authentication Page"}
        )
    except Exception as e:
        raise e


@router.post("/", response_class=JSONResponse)
async def login(request: Request, login: Login):
    """Route for User Login
    Returns:
        _type_: Login Response
    """
    try:
        msg = "Login Successful"
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": msg}
        )
        token_response = await login_for_access_token(response=response, login=login)
        if not token_response["status"]:
            msg = "Incorrect Username and password"
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": msg},
            )
           
        response.headers["uuid"] = token_response["uuid"]

        return response

    except HTTPException:
        msg = "UnKnown Error"
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"status": False, "message": msg},
        )
        
    except Exception as e:
        msg = "User not found"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": False, "message": msg},
        )
        return response


@router.get("/register", response_class=JSONResponse)
async def authentication_page(request: Request):
    """Route for User Registration
    Returns:
        _type_: Register Response
    """
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Registration Page"}
        )
    except Exception as e:
        raise e


@router.post("/register", response_class=JSONResponse)
async def register_user(request: Request, register: Register):

    """Post request to register a user
    Args:
        request (Request): Request Object
        register (Register):    name: str
                                username: str
                                email_id: str
                                phone_no: int
                                password: str
    Raises:
        e: If the user registration fails
    Returns:
        _type_: Will redirect to the embedding generation route and return the UUID of user
    """
    try:
        name = register.name
        username = register.username
        password = register.password
        email_id = register.email_id
        phone_no = register.phone_no

        # Add uuid to the session
        user = User(name, username, email_id, phone_no, password)
        request.session["uuid"] = user.uuid_

        # Validation of the user input data to check the format of the data
        user_registration = RegisterValidation(user)

        validate_regitration = user_registration.validate_registration()
        if not validate_regitration["status"]:
            msg = validate_regitration["msg"]
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": msg},
            )
            return response

        # Save user if the validation is successful
        validation_status = user_registration.authenticate_user_registration()

        msg = "Registration Successful...Please Login to continue"
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": True, "message": validation_status["msg"]},
            headers={"uuid": user.uuid_},
        )
        return response
    except Exception as e:
        raise e


@router.get("/logout")
async def logout(request: Request):
    """Route for User Logout
    Returns:
        _type_: Logout Response
    """
    try:
        msg = "You have been logged out"
        response =  RedirectResponse(url="/auth/", status_code=status.HTTP_302_FOUND, headers={"msg": msg})
        response.delete_cookie(key="access_token")
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"status": True, "message": msg}
        )
        return response
    except Exception as e:
        raise e