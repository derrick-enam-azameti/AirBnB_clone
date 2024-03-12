#!/usr/bin/python3
"""Module base_model

This module contains the definition for Amenity Class
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """A class that represents a review

    Attributes:
        place_id (str): ID of the Place
        user_id (str): ID of the User
        text (str): review text content
    """

    place_id = ""
    user_id = ""
    text = ""
