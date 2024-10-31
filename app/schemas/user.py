import re
from pydantic import BaseModel, Field, field_validator, EmailStr, ValidationInfo


class UserSignUp(BaseModel):
    username: str = Field(
        title="Username",
        description="The username must be from 3 to 30 characters long and can contain letters, numbers and underscores.",
        min_length=3,
        max_length=30
    )
    email: EmailStr = Field(
        title="Email",
        description="Must be a valid email address.",
        max_length=75
    )
    password: str = Field(
        title="Password",
        description="The password must have at least 8 characters.",
        min_length=8
    )
    confirm_password: str = Field(
        title="Confirm Password",
        description="It must match the password."
    )

    # Username format validator
    @field_validator("username")
    def validate_username(cls, value):
        if not re.match(r'^\w+$', value):
            raise ValueError('Username can only contain letters, numbers, and underscores.')
        return value

    # Matching password validator
    @field_validator("confirm_password")
    def passwords_match(cls, value, info: ValidationInfo):
        password = info.data.get("password")
        if password and value != password:
            raise ValueError("Passwords do not match")
        return value



class UserLogin(BaseModel):
    username: str = Field(
        title="Username",
        description="Your account's username.",
        min_length=3,
        max_length=30
    )
    password: str = Field(
        title="Password",
        description="Your account's password.",
        min_length=8
    )



class UpdateAccount(BaseModel):
    username: str = Field(
        title="Username",
        description="The username must be from 3 to 30 characters long and can contain letters, numbers and underscores.",
        min_length=3,
        max_length=30
    )

    # Username format validator
    @field_validator("username")
    def validate_username(cls, value):
        if not re.match(r'^\w+$', value):
            raise ValueError('Username can only contain letters, numbers, and underscores.')
        return value



class Token(BaseModel):
    access_token: str
    token_type: str
