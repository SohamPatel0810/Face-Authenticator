import os
from dotenv import dotenv_values

class CommonUtils:

    def get_environment_variable(self, variable_name: str):
        """
        :param variable_name:
        :return environment variable:
        """
        if os.environ.get(variable_name) is None:
            enironment_variable = dotenv_values(".env")
            return enironment_variable[variable_name]
        else:
            return os.environ.get(variable_name)