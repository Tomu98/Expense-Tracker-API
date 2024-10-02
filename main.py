from fastapi import FastAPI
from routers import auth, expenses

app = FastAPI(
    title="Expense Tracker API",
    version="0.13.1"
)

app.include_router(auth.router)
app.include_router(expenses.router)
