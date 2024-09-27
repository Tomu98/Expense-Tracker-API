from pydantic import BaseModel, Field, EmailStr

class UserSignUp(BaseModel):
    username: str = Field(
        title="Username",
        description="The username must be from 3 to 20 characters long and can contain letters, numbers and underscores.",
        min_length=3,
        max_length=20
    )
    email: EmailStr = Field(
        title="Email",
        description="Must be a valid email address.",
        max_length=75
    )
    password: str = Field(
        title="Password",
        description="The password must have at least 8 characters, include one uppercase letter, one number, and one special character.",
        min_length=8
    )
    confirm_password: str = Field(
        title="Confirm Password",
        description="It must match the password.",
        min_length=8
    )



class UserLogin(BaseModel):
    email: EmailStr = Field(
        title="Email",
        description="Must be a valid email address.",
        max_length=75
    )
    password: str = Field(
        title="Password",
        description="Your account's password.",
        min_length=8
    )

# Falta agregar para validar que password coincida con confirm_password
