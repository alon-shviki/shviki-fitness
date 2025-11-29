# ShvikiFitness 💪

ShvikiFitness is a comprehensive fitness application designed to help users discover exercises, manage their saved workouts, and track their progress. It provides a user-friendly dashboard, robust authentication, and seamless integration with the ExerciseDB API to offer a wide range of exercises. The application is built with Flask, SQLAlchemy, and Docker, ensuring portability and scalability.

## 🚀 Key Features

- **User Authentication**: Secure user registration and login functionality using password hashing.
- **Dashboard**: A personalized dashboard displaying user information and saved exercises.
- **Exercise Search**: Integration with the ExerciseDB API to search for exercises based on various criteria.
- **Saved Exercises Management**: Ability to save, view, and manage personalized exercise lists.
- **Health Check Endpoint**: A dedicated endpoint for monitoring the application's health status.
- **Dockerized Deployment**: Easy deployment using Docker and Docker Compose.
- **Kubernetes Support**: Helm chart provided for Kubernetes deployment.
- **Database Persistence**: MySQL database for persistent storage of user data and saved exercises.

## 🛠️ Tech Stack

- **Frontend**: (Basic, as this is primarily a backend application) HTML/CSS (rendered by Flask)
- **Backend**: Python, Flask
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **API Integration**: requests (for ExerciseDB API)
- **Containerization**: Docker
- **Orchestration**: Kubernetes (via Helm)
- **Web Server**: Gunicorn
- **Configuration**: `.env` files, `values.yaml` (Helm)
- **Testing**: pytest, pytest-flask
- **Build Tool**: Docker
- **Other**: Werkzeug (for security), python-dotenv (for environment variables)

## 📦 Getting Started / Setup Instructions

### Prerequisites

- Python 3.11+
- Docker
- Docker Compose
- Helm (for Kubernetes deployment)
- MySQL (if not using Docker Compose)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd shvikifitness
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    *   Create a `.env` file in the root directory.
    *   Add the following variables (replace with your actual values):

        ```
        FLASK_ENV=development
        FLASK_SECRET_KEY=<your_secret_key>
        EXERCISE_DB_API_KEY=<your_exercise_db_api_key>
        DATABASE_URI=mysql+pymysql://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>
        ```

        Alternatively, if using Docker Compose, these variables can be set in the `docker-compose.yml` file or a separate `.env` file referenced by it.

### Running Locally

1.  **Using Flask development server:**

    ```bash
    python run.py
    ```

    The application will be accessible at `http://0.0.0.0:5000`.

2.  **Using Docker Compose:**

    ```bash
    docker-compose up --build
    ```

    This will build the Docker image and start the application along with the MySQL database.  The application will be accessible at `http://localhost:5000`.

3.  **Deploying with Helm (Kubernetes):**

    *   Customize the `helm/helm-chart/values.yaml` file with your desired configuration.
    *   Install the chart:

        ```bash
        helm install shviki-fitness helm/helm-chart/
        ```

    *   Access the application through the Kubernetes service.

## 💻 Usage

1.  **Access the application in your browser.**
2.  **Register a new user account or log in with existing credentials.**
3.  **Explore the dashboard to view saved exercises.**
4.  **Use the exercise search functionality to find new exercises.**
5.  **Save exercises to your personal list.**
6.  **Manage your saved exercises by deleting or updating them.**

## 📂 Project Structure

```
shvikifitness/
├── app                              # Main Flask application package
│   ├── __init__.py                  # Initializes the Flask app, DB connection, Blueprints, etc.
│   ├── models.py                    # SQLAlchemy ORM models defining DB tables/entities
│   ├── __pycache__                  # Python's compiled bytecode cache (auto-generated)
│   └── templates                    # HTML templates rendered by Flask routes
│       ├── base.html                # Base layout template (header/nav/footer)
│       ├── create_user.html         # Admin page to create new users
│       ├── dashboard.html           # Admin dashboard with metrics and user management
│       ├── edit_user.html           # Edit user details page
│       ├── exercises.html           # Exercise search and display page (API-based results)
│       ├── index.html               # Landing page for the Shviki Fitness website
│       ├── login.html               # User login form (phone + password)
│       ├── my_exercises.html        # User's saved exercises and workout list page
│       ├── register.html            # Registration form page for new customers
│       └── user_home.html           # Logged-in customer's personal dashboard/home page

├── docker-compose.yml               # Runs Flask + MySQL containers locally with networking
├── Dockerfile                       # Builds the Flask app container image

├── helm                             # Kubernetes deployment configuration using Helm
│   └── helm-chart                   # Custom Helm chart for the Shviki Fitness app
│       ├── Chart.yaml               # Chart metadata and version info
│       ├── templates                # Kubernetes manifests generated by Helm
│       │   ├── app-configmap.yaml   # App environment variables/config for Flask
│       │   ├── external-secrets.yaml# Secrets fetched from AWS/GCP secret managers
│       │   ├── flask-deployment.yaml# Deployment manifest for Flask application Pods
│       │   ├── flask-hpa.yaml       # Horizontal Pod Autoscaler configuration
│       │   ├── flask-service.yaml   # Service exposing Flask app to the cluster
│       │   ├── hpa-rbac.yaml        # RBAC roles for HPA or monitoring permissions
│       │   ├── irsa-configmap.yaml  # IAM Role for Service Account (EKS IRSA integration)
│       │   ├── mysql-service.yaml   # Service exposing MySQL inside the cluster
│       │   ├── mysql-statefulset.yaml # StatefulSet configuration for MySQL persistence
│       │   └── secret-store.yaml    # Secret provider class for external secrets
│       └── values.yaml              # Default configuration values for Helm templating

├── README.md                        # Project documentation and setup instructions
├── requirements.txt                 # Python dependencies for Flask and supporting libraries
├── run.py                           # App entry point for running Flask in development mode

├── tests                            # Automated unit and integration tests
│   ├── conftest.py                  # Pytest fixtures for app and DB setup
│   ├── __init__.py                  # Marks this directory as a package
│   ├── test_exercises.py            # Tests for exercise search and save functionality
│   ├── test_integration.py          # End-to-end integration tests
│   ├── test_login.py                # Authentication tests for login flow
│   ├── test_logout.py               # Tests logout behavior/session clearing
│   └── test_register.py             # Registration form + DB creation functionality tests



