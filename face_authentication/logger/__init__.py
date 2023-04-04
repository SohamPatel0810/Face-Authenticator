import logging
import os
from datetime import datetime

# Creating logs directory to store log in files
LOG_DIRECTORY = "logs"
LOG_DIRECTORY = os.path.join(os.getcwd(), LOG_DIRECTORY)

# Creating LOG_DIRECTORY if it does not exists.
os.makedirs(LOG_DIRECTORY, exist_ok=True)


# Creating file name for log file based on current timestamp
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
file_name = f"log_{CURRENT_TIME_STAMP}.log"

# Creating file path for projects.
log_file_path = os.path.join(LOG_DIRECTORY, file_name)


logging.basicConfig(
    filename=log_file_path,
    filemode="w",
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)