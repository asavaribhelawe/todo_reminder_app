# To-Do Reminder App

A simple To-Do Reminder App built using Flask, Python, and PostgreSQL. This app allows users to add, view, update, and delete tasks. It supports RESTful API endpoints for managing tasks.

## Features
- Add a new task
- View all tasks
- Update an existing task
- Delete a specific task
- Delete all tasks

## Technologies Used
- **Flask** - Web framework for Python
- **PostgreSQL** - Database to store tasks
- **Render** - Platform to deploy the app

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Flask
- Flask-SQLAlchemy
- psycopg2 (PostgreSQL adapter)
- Requests (for API interaction)

### Install dependencies
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/todo-reminder-app.git
    cd todo-reminder-app
    ```
2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up your PostgreSQL database and update your database URI in config.py.
5. Run the app locally:
   ```bash
    python app.py
    ```
   The app will be running at http://127.0.0.1:5000.
   
### API Endpoints
- **POST /tasks** - Add a new task.
- **GET /tasks** - Get all tasks.
- **GET /tasks/{id}** - Get a task by ID.
- **PUT /tasks/{id}** - Update a task by ID.
- **DELETE /tasks/{id}** - Delete a task by ID.
- **DELETE /tasks** - Delete all tasks.

### Deployment
This app is deployed on Render, and the live URL is:
https://todo-reminder-app-6343.onrender.com

### Running Tests
To run tests, save the test_app.py file in your pc. Make sure your have 'pytest' dependency installed. 
In cmd, navigate to the location of the file, and then use follwoing command:
 ```bash
    pytest test_app.py
 ```
