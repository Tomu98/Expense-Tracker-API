from fastapi import FastAPI
from routers import auth, expenses, users


app = FastAPI(
    title="Expense Tracker API",
    version="1.0.1",
    description="""A comprehensive API designed for managing personal expenses,
                enabling users to register and log in securely using JWT-based authentication,
                as well as add, update, and delete expenses with ease.
                The API also allows users to filter and retrieve their expenses based on various criteria, 
                and manage their profiles for a personalized experience.""",
    contact={
        "name": "Abel Tomás",
        "url": "https://github.com/Tomu98",
        "email": "abeltomasr98@gmail.com"
    }
)


app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(users.router)
