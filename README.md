# Expense Tracker API

Expense Tracker API is a backend application designed to allow users to manage their personal expenses.
Users can register, log in, update their username or delete their account, and perform CRUD operations on their expenses.
The API also features a filtering system to search for expenses by dates and categories.


This project is inspired by an idea from [roadmap.sh](https://roadmap.sh), a platform that offers community-created roadmaps, 
best practices, projects, articles, resources and guides to help people grow in their technology careers.


Specific inspiration for this project comes from the following link: [Expense Tracker API en roadmap.sh](https://roadmap.sh/projects/expense-tracker-api)

<br>

## Contributions

I want to clarify that this is my first API project (of the many I want to do). So if I made any mistake either small or big, improvements, help and advice are welcome. If you want to help, please open an “Issue” or create a “Pull Request”.


In advance, thanks for reading and visiting the project.

<br>

## Features

- **Account management**: Users can register, login, update their username or delete their account.
- **Authentication with JWT**: The API is protected by JSON Web Tokens (JWT), only authenticated users can access their data and perform operations on the API.
- **Expense administration**: Users can create, read, update and delete their expenses. Expenses can be filtered by dates and categories.
- **Secure and Scalable Database**: The database used is PostgreSQL. Sensitive settings, such as the database connection URL, are managed through an `.env` file, so users can easily switch databases if they prefer, by adjusting only the `DATABASE_URL` variable.
- **Cascading deletion**: When a user account is deleted, all charges associated with it are automatically deleted.
- **Database Migrations**: Database schema is kept up to date through migrations managed with Alembic.

<br>

## Requirements

- Python 3.9+
- FastAPI
- PostgreSQL (you can use any SQL database, but PostgreSQL is the one used in this project)
- Pydantic v2
- Other requirements mentioned in `requirements.txt`

<br>

## Installation

1. Clone this repository on your local machine:

   ```bash
   git clone https://github.com/Tomu98/Expense-Tracker-API.git
   ```

2. Go to the project directory:

   ```bash
   cd Expense-Tracker-API
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv .expvenv
   source .expvenv/bin/activate  # Linux/MacOS
   .expvenv\Scripts\activate  # Windows
   ```

4. Install the necessary dependencies for the project using the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

5. Set environment variables
   This project uses environment variables to configure the connection to the database and a secret key for JWT authentication.
   - You must create a file named `.env` in the root directory of the project with the following variables:
     ```python
     DATABASE_URL=postgresql://<your_user>:<your_password>@localhost/<your_database>
     SECRET_KEY=<generated_unique_key>
     ```

   - To generate a secure secret key in bash, you can use the following command:
     ```bash
     openssl rand -hex 32
     ```
     Copy the generated value and place it in the `SECRET_KEY` variable inside the `.env` file.

   - If you prefer to use a different database (such as SQLite, MySQL, etc.), change the `DATABASE_URL` value to the connection URL corresponding to your database.

   > [!NOTE]
   > Be sure not to include the `.env` file in Git, as it contains sensitive information. This project already has a `.gitignore` that automatically omits this file.
11. Start the API development server with the following command:

    ```bash
    uvicorn main:app --reload
    ```


<br>

## How to use it

Once the application is running, you can access Swagger's interactive documentation at 
`http://localhost:8000/docs` where you can visualize and test the different API endpoints.

### Main Endpoints:

**Authentication**
- **POST** `/signup` - User registration.
- **POST** `/auth/login/` - User login.

**Expenses**
- **GET** `/expenses` - Read expenses.
- **POST** `/expenses` - Add expense.
- **PUT** `/expenses/{id}` - Update expense.
- **DELETE** `/expenses/{id}` - Delete expense.

**User Account**
- **PUT** `/update` - Update the username.
- **DELETE** `/delete` - Delete user account.

<br>

By following these steps, you will be able to install and run the Expense Tracker API in your local environment.
If you decide to change the database or authentication settings, 
be sure to adjust the environment variables in the `.env` file.


