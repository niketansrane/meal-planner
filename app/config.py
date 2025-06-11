"""
Load env cars from .env and also keep some constant vsettings and exposed them as a config object.
"""


import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class to hold environment variables and constants.
    """

    # Load environment variables from .env file
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
    AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT")
    AZURE_SUBSCRIPTION_KEY = os.getenv("AZURE_SUBSCRIPTION_KEY")
    AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
    MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
