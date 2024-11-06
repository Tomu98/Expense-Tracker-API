from fastapi import FastAPI
from app.db import engine
from app.models.user import User
from app.models.expense import Expense
from app.routers import health, auth, expenses, users


app = FastAPI(
    title="Expense Tracker API",
    version="1.2.13",
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


# Create tables for all models
User.metadata.create_all(bind=engine)
Expense.metadata.create_all(bind=engine)


# All routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(users.router)


# A ver:
# Comprobar que todo esté bien con los filtros de fechas en:
# - app/routers/expenses.py Posiblemente voy a mejorar el filtro y su rango dado por el usuario
# - app/schemas/expense.py
# - tests/utils.py

# Al probar desde swagger creando un nuevo usuario y un nuevo gasto me aparece:
# - id: 21 del gasto
# - user_id: 6 del usuario
# Comprobar si eso se puede arreglar para que no se acumulen ids de usuarios que ya no existen

# Habían tres expenses, al actualizar el segundo,
# este en pgadmin me apareció que se movió en el tercer lugar
# y el que estaba tercero quedó segundo, ASEGURAR si es normal o hay que arreglar
