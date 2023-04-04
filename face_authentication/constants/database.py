from face_authentication.utilities.utilities import CommonUtils

MONGODB_URL = CommonUtils().get_environment_variable("MONGODB_URL")
DATABASE_NAME = CommonUtils().get_environment_variable("DATABASE_NAME")
USER_COLLECTION_NAME = CommonUtils().get_environment_variable("USER_COLLECTION_NAME")
USER_EMBEDDING_COLLECTION_NAME = CommonUtils().get_environment_variable("USER_EMBEDDING_COLLECTION_NAME")