from pydantic import BaseModel, EmailStr, Field

class UserSignUp(BaseModel):
    username: str = Field(
        title="Username",
        min_length=3,
        max_length=20,
        description="The username must be from 3 to 20 characters long and can contain letters, numbers and underscores."
    )
    email: EmailStr = Field(
        title="Email",
        description="Must be a valid email address."
    )
    password: str = Field(
        title="Password",
        min_length=8,
        description="The password must have at least 8 characters, include one uppercase letter, one number, and one special character."
    )
    confirm_password: str = Field(
        title="Confirm Password",
        min_length=8,
        description="It must match the password."
    )


class UserLogin(BaseModel):
    email: EmailStr = Field(
        title="Email",
        description="Must be a valid email address."
    )
    password: str = Field(
        title="Password",
        description="Your account's password."
    )
