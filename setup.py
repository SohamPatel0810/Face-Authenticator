from setuptools import setup, find_packages
from typing import List

# Declaring variables for setup functions
PROJECT_NAME = "Face Authenticator"
VERSION = "1.0.0"
AUTHOR = "Soham Patel"
DESRCIPTION = "Face Authentication using the concept of Image Embeddings"


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESRCIPTION,
    packages=find_packages(),
)