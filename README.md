# Personalized Workout Plan API

This is a RESTful API for a Personalized Workout Plan system, built with Django and Django Rest Framework. It allows users to register, create and manage customized workout plans, and track their fitness goals.

---

### Core Features

* **User Authentication**: Secure user registration, login, and logout using JSON Web Tokens (JWT).
* **Exercise Library**: A predefined, read-only library of exercises with details like descriptions and target muscles.
* **Personalized Workout Plans**: Users can create, view, update, and delete their own workout plans, adding exercises from the library and specifying sets, reps, and order.
* **Fitness Goals & Tracking**: Functionality for users to set and manage personal fitness goals and track metrics like weight over time.
* **API Documentation**: Automatic, interactive API documentation powered by Swagger (drf-yasg).

---

### Tech Stack

* **Backend**: Python, Django, Django Rest Framework
* **Database**: SQLite (for development)
* **Authentication**: djangorestframework-simplejwt (JWT)
* **API Documentation**: drf-yasg (Swagger)
* **Deployment**: Docker, Docker Compose, Gunicorn

---

### Setup and Installation

There are two ways to run this project: locally using a Python virtual environment, or using Docker (recommended).

#### Option 1: Using Docker & Docker Compose (Recommended)

This is the easiest way to get the entire application running with a single command.

1.  **Prerequisites**:
    * Docker

2. **Clone the repository**:
    ```bash
    git clone https://github.com/guraspy/personalized-workout-api
    cd personalized-workout-api
    ```

3.  **Run the application**:
    From the project's root directory, run the following command:
    ```bash
    docker-compose up --build
    ```
    This command will:
    * Build the Docker image for the Django application.
    * Start the container.
    * Automatically run database migrations and the seeding script.
    * Start the Gunicorn server.

    The API will now be running at `http://localhost:8000/`. To stop the application, press `Ctrl+C`.

#### Option 2: Local Development (Without Docker)

1.  **Prerequisites**:
    * Python 3.8+
    * `pip` and `venv`

2.  **Clone the repository**:
    ```bash
    git clone https://github.com/guraspy/personalized-workout-api
    cd personalized-workout-api
    ```

3.  **Create and activate a virtual environment**:
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run database migrations**:
    ```bash
    python manage.py migrate
    ```

6.  **Seed the database with exercises**:
    ```bash
    python manage.py seed_exercises
    ```

7.  **Run the development server**:
    ```bash
    python manage.py runserver
    ```
    The API will now be running at `http://localhost:8000/`.

---

### API Documentation & Endpoints

Once the application is running, you can access the interactive Swagger API documentation in your browser:

* **Swagger UI**: `http://localhost:8000/swagger/`
* **ReDoc UI**: `http://localhost:8000/redoc/`

#### Key Endpoints:

* **Authentication**:
    * `POST /api/auth/register/`: Register a new user.
    * `POST /api/auth/login/`: Obtain JWT access and refresh tokens.
    * `POST /api/auth/token/refresh/`: Refresh an access token.
    * `POST /api/auth/logout/`: Logout by blacklisting the refresh token.
* **Main API**:
    * `/api/exercises/`: List of all available exercises.
    * `/api/workout-plans/`: List and create of user's workout plans.
    * `/api/workout-plans/id/`: CRUD operations for the user's workout plans by id.
    * `/api/goals/`: List and create of user's goals.
    * `/api/goals/id/`: CRUD operations for the user's goals by id.
    * `/api/tracking/`: List and create of user's weight tracking data.
    * `/api/tracking/id/`: CRUD operations for the user's weight tracking data by id.
* **Admin**:
    * `/admin/`: Administrative interface.
