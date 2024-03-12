#!/usr/bin/python3
"""Module base_model

This module contains the definition for User Class
"""

from models.base_model import BaseModel


class User(BaseModel):
    """A class that represents a user.

    Attributes:
        email (str): user email
        password (str): user password
        first_name (str): first name of the user
        last_name (str): last name of the user
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
