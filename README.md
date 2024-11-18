# Expense Tracker API


Expense Tracker API is a backend application designed to help users manage their personal expenses.
Users can register, log in, update their username or delete their account, and perform CRUD operations on their expenses.
The API also features a filtering system to search for expenses by dates and categories.


This project is inspired by an idea from [roadmap.sh](https://roadmap.sh), a platform that offers community-created roadmaps, best practices, projects, and resources to help people grow in their technology careers.


Specific inspiration for this project comes from the following link: [Expense Tracker API in roadmap.sh](https://roadmap.sh/projects/expense-tracker-api)


<img alt="Static Badge" src="https://img.shields.io/badge/Version-1.2.15-seagreen?style=for-the-badge">


<br>

## Features

- **Account management:** Users can register, login, update their username or delete their account.
- **Authentication with JWT:** The API is protected by JSON Web Tokens (JWT), only authenticated users can access their data and perform operations on the API.
- **Expense administration:** Users can create, read, update and delete their expenses. Expenses can be filtered by dates and categories.
- **Secure and Scalable Database:** The database I used is PostgreSQL. Sensitive settings, such as the database connection URL, are managed through an `.env` file, so users can easily switch databases if they prefer, by adjusting only the `DATABASE_URL` variable.
- **Database Migrations:** Database schema is kept up to date through migrations managed with Alembic.
- **Automated testing:** This project uses pytest to perform unit tests and check that everything works correctly.

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
   python -m venv .venv          # Create a virtual environment
   .venv\Scripts\activate        # Activate the environment in Windows
   source .expvenv/bin/activate  # Activate the environment in Linux/MacOS
   ```

4. Install the necessary dependencies for the project using the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

5. This project uses environment variables to configure the connection to the database and a secret key for JWT authentication. You must create a file named `.env` in the root directory of the project with the following variables:

   ```python
   DATABASE_URL=postgresql://<your_user>:<your_password>@localhost/<your_database>
   SECRET_KEY=<generated_unique_key>
   ```

   For the `SECRET_KEY`, you can generate a secure key by running the following command in your terminal:
   
   ```bash
   openssl rand -hex 32
   ```

   Copy the generated value and assign it to the `SECRET_KEY` variable in your `.env` file. If you plan to use a different database, such as SQLite or MySQL, simply update the `DATABASE_URL` with the connection string relevant to your chosen database.

   > Note: Make sure not to include the .env file in version control, as it contains sensitive information. The project is already configured with a .gitignore file to automatically exclude this file.
7. Start the API development server with the following command:

    ```bash
    uvicorn main:app --reload
    ```

<br>

By following these steps, you'll be able to install and run the Expense Tracker API in your local environment.
Adjust the `.env` file if you need to change the database or authentication settings.

<br>

## Running Tests

This project uses pytest to perform automated tests to ensure the reliability and functionality of key features.
To run the tests, use the following command:
```bash
pytest
```

<br>

## How to use it

Once the application is running, you can access Swagger's interactive API documentation at 
`http://localhost:8000/docs`, where you can visualize and test the available API endpoints.

### Main Endpoints

**Authentication:**
- **POST** `/signup` - User registration.
- **POST** `/login` - User login.

**Expenses:**
- **GET** `/expenses` - Retrieve a list of expenses.
- **POST** `/expenses` - Create a new expense.
- **PUT** `/expenses/{id}` - Update an expense by ID.
- **DELETE** `/expenses/{id}` - Delete an expense by ID.

**User Account:**
- **PUT** `/user` - Update the username.
- **DELETE** `/user` - Delete the user account.

<br>

## Feedback & Contributions

I want to clarify that this is my first API project (of the many I want to do), and I welcome any feedback or contributions. If you find any bugs or have suggestions for improvements, feel free to open an issue or submit a pull request.

<br>

### **Thanks for checking out the project 🤍**



