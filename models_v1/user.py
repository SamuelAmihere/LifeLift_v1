#!/usr/bin/python3
"""This is the user class"""
import os
import hashlib
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from models import storage_type


class User(BaseModel, Base):
    """This is the class for User
    """
    fields_errMSG = {
        'user_name': 'Missing user name',
        'password': 'Missing password',
        'user_type': 'Missing user type',
    }
    if storage_type == "db":
        __tablename__ = "users"
        user_name = Column(String(128), nullable=False)
        hashed_password = Column(String(128), nullable=False)
        user_type = Column(Enum('admin', 'company', 'nurse', 'driver'),
                           nullable=False)
        staff_id = Column(String(60), ForeignKey('staff.id'), nullable=True)
        salt = Column(String(128), nullable=False)
    else:
        user_name = ""
        hashed_password = ""
        user_type = ""
        salt = ""

    @staticmethod
    def generate_salt():
        return os.urandom(16).hex()  # Generate a random salt
    
    def set_password(self, password):
        """Set password for the user"""
        self.salt = User.generate_salt()  # Generate a salt
        password_with_salt = password + self.salt  # Combine password with salt
        # Hash the combined string
        self.hashed_password = hashlib.sha256(password_with_salt.encode()).hexdigest()

    def is_valid_password(self, password):
        """Check if the provided password is valid"""
        # Combine input password with stored salt
        password_with_salt = password + self.salt
         # Hash the combined string
        hashed_input_password = hashlib.sha256(password_with_salt.encode()).hexdigest()
        # Compare with stored hashed password
        return hashed_input_password == self.hashed_password