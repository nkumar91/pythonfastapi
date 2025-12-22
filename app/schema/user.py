from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, SecretStr


# Required fields for a user
class UserBase(BaseModel):
	"""Shared fields for a user"""

	name: str = Field(..., example="Jane Doe")
	email: str = Field(..., example="jane@example.com")


class UserCreate(UserBase):
	"""Fields required when creating a user"""
	# Use SecretStr to avoid accidentally printing passwords; in production
	# you should hash passwords before storing them.
	name:str
	email:str
	password:str
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
