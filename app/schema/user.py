from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, SecretStr, validator


# Required fields for a user
class UserBase(BaseModel):
	"""Shared fields for a user"""

	name: str = Field(..., example="Jane Doe")
	email: EmailStr = Field(..., example="jane@example.com")


class UserCreate(UserBase):
	"""Fields required when creating a user"""
	# Use SecretStr to avoid accidentally printing passwords; in production
	# you should hash passwords before storing them.
	name:str = Field(min_length=2, max_length=50, examples=["John Doe"],)#pattern=r"^[a-z0-9_]{3,20}$"
	email:EmailStr
	password:str = Field(min_length=8, max_length=16, examples=["strong-password"])
	# @validator("password")
	# def validate_password(cls, v):
	# 	if " " in v:
	# 		raise ValueError("Password must not contain spaces")
	# 	return v
	
	#password: SecretStr = Field(..., example="strong-password")


class UserRead(UserBase):
	"""Fields returned to clients (no password)"""
	id: int
	name:str
	email:str
	created_at: datetime = Field(default_factory=datetime.utcnow)
	model_config = {"from_attributes": True}

class UserLogin(UserBase):
	"""Fields returned to clients with token (no password)"""
	id: int
	email:str
	name:str
	access_token:str = None
	model_config = {"from_attributes": True}


# Note: This file contains Pydantic models for validation/serialization. If you
# need an ORM model (e.g., SQLAlchemy), add it to `app/models/` and map
# attributes to the DB layer; always store hashed passwords, never plaintext.
