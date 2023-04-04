from face_authentication.utilities.utilities import CommonUtils

SECRET_KEY = CommonUtils().get_environment_variable("SECRET_KEY")
ALGORITHM = CommonUtils().get_environment_variable("HASH_ALGORITHM")