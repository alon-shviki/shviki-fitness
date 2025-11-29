# ShvikiFitness 💪

ShvikiFitness is a comprehensive fitness application designed to help users discover exercises, manage their saved workouts, and track their progress. It provides a **user-friendly dashboard**, **robust authentication**, and seamless integration with the **ExerciseDB API** to offer a wide range of exercises. The application is built with **Flask**, **SQLAlchemy**, and **Docker**, ensuring **portability**, **scalability**, and **Kubernetes readiness**.  

This app is part of the **ShvikiFitness ecosystem**, where the **GitOps repo** manages deployment via ArgoCD, and the **infrastructure repo** provisions the underlying EKS cluster, VPC, and IAM roles.

---

## 🚀 Key Features

- **User Authentication:** Secure registration and login with hashed passwords.
- **Dashboard:** Personalized user dashboard showing saved exercises and stats.
- **Exercise Search:** Integration with ExerciseDB API to search exercises by name, type, or muscle group.
- **Saved Exercises Management:** Save, update, and delete exercises from your personal list.
- **Health Check Endpoint:** For monitoring app health and uptime.
- **Dockerized Deployment:** Runs locally with Docker Compose.
- **Kubernetes Support:** Helm chart provided for Kubernetes deployment.
- **Database Persistence:** Uses MySQL for storing user data and saved exercises.
- **Testing Ready:** Unit and integration tests using pytest and pytest-flask.

---

## 🛠️ Tech Stack

| Component             | Technology                     | Description                                                             |
|-----------------------|--------------------------------|-------------------------------------------------------------------------|
| **Backend**           | Python, Flask                  | Web server and API handling.                                            |
| **Frontend**          | HTML/CSS (Flask templates)     | Simple web interface for dashboards and user interactions.             |
| **Database**          | MySQL                          | Persistent storage of users, exercises, and dashboards.                |
| **ORM**               | SQLAlchemy                     | Object-relational mapping between Python models and MySQL tables.      |
| **API Integration**   | requests                       | Consuming ExerciseDB API for exercise search.                           |
| **Containerization**  | Docker                         | Package and run the app locally or in the cloud.                        |
| **Orchestration**     | Kubernetes (via Helm)          | Deployment and scaling of the application in a cluster.                 |
| **Web Server**        | Gunicorn                       | Production-grade WSGI HTTP server for Flask.                             |
| **Secrets Management**| .env files / Helm values.yaml  | Securely store API keys and DB credentials.                             |
| **Testing**           | pytest, pytest-flask           | Unit and integration tests for app features.                             |

---

## 📈 Architecture Diagrams

### 1️⃣ User Interaction Flow

```text
         ┌──────────────┐
         │    Users     │
         └─────┬────────┘
               │
               ▼
        ┌──────────────┐
        │   Flask App  │
        │ (Web Server) │
        └─────┬────────┘
   ┌───────────┼─────────────┐
   │                           │
   ▼                           ▼
┌──────────────┐          ┌──────────────┐
│ MySQL DB     │          │ ExerciseDB API│
│ (User +      │<---------│ Search & Info │
│ Saved Workouts)│         └──────────────┘
└──────────────┘
```

### 2️⃣ Connection to GitOps & Infra

```text
┌──────────────┐
│    Users     │
└─────┬────────┘
      │
      ▼
 ┌──────────────┐
 │  ShvikiFitness│
 │   App        │
 └─────┬────────┘
       │
       ▼
 ┌──────────────┐        ┌─────────────────┐
 │ GitOps Repo  │<------>│ Infra Repo (EKS)│
 │ (ArgoCD App) │        │ VPC, IAM, Nodes │
 └──────────────┘        └─────────────────┘
       │
       ▼
 ┌──────────────┐
 │ Kubernetes   │
 │ Cluster      │
 └──────────────┘
```

**Explanation:**  
- The **user interacts** with the Flask app via browser.  
- The **Flask app** communicates with **MySQL** and **ExerciseDB API**.  
- **Helm chart** in the app repo defines how the application is deployed in **Kubernetes**.  
- **GitOps repo** uses ArgoCD to synchronize the Helm chart with the cluster.  
- **Infra repo** provisions the EKS cluster, networking, node groups, and IAM roles.  

---

## 📦 Getting Started / Setup Instructions

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Helm (for Kubernetes deployment)
- Access to a Kubernetes cluster (optional)
- MySQL (optional if using Docker Compose)

---

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/alon-shviki/shviki-fitness.git
cd shvikifitness
```

2. **Create a Python virtual environment (recommended):**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**

Create a `.env` file:

```
FLASK_ENV=development
FLASK_SECRET_KEY=<your_secret_key>
EXERCISE_DB_API_KEY=<your_api_key>
DATABASE_URI=mysql+pymysql://<user>:<password>@<host>:<port>/<db>
```

---

### Running Locally

**Flask Development Server:**

```bash
python run.py
```

**Docker Compose:**

```bash
docker-compose up --build
```

**Kubernetes Deployment via Helm:**

1. Customize `helm/helm-chart/values.yaml` (DB creds, API key, replicas).  
2. Install Helm chart:

```bash
helm install shviki-fitness helm/helm-chart/
```

- The chart includes:
  - **Flask Deployment** with `replicas` for scaling.
  - **Service** exposing the app.
  - **Horizontal Pod Autoscaler (HPA)** for auto-scaling.
  - **External Secrets** integration.
  - **IAM Role for Service Account (IRSA)** support on EKS.
  - **MySQL StatefulSet & Service** for persistent storage.

---

## 💻 Usage

1. Open the app in a browser.  
2. Register or log in.  
3. Search exercises via ExerciseDB API.  
4. Save, update, or delete exercises.  
5. Monitor dashboards and progress.  
6. Use `/health` endpoint for monitoring.

---

## 📂 Project Structure

```
shvikifitness/
├── app                              # Main Flask application package
│   ├── __init__.py                  # Initializes the Flask app, DB connection, Blueprints, etc.
│   ├── models.py                    # SQLAlchemy ORM models defining DB tables/entities
│   ├── __pycache__/                 # Python compiled bytecode cache (auto-generated)
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
│   └── helm-chart                   # Custom Helm chart for ShvikiFitness app
│       ├── Chart.yaml               # Chart metadata and version info
│       ├── templates                # Kubernetes manifests generated by Helm
│       │   ├── app-configmap.yaml   # App environment variables/config for Flask
│       │   ├── external-secrets.yaml # Secrets fetched from AWS/GCP secret managers
│       │   ├── flask-deployment.yaml # Deployment manifest for Flask Pods
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
└── tests                            # Automated unit and integration tests
    ├── conftest.py                  # Pytest fixtures for app and DB setup
    ├── __init__.py                  # Marks this directory as a package
    ├── test_exercises.py            # Tests for exercise search and save functionality
    ├── test_integration.py          # End-to-end integration tests
    ├── test_login.py                # Authentication tests for login flow
    ├── test_logout.py               # Tests logout behavior/session clearing
    └── test_register.py             # Registration form + DB creation functionality tests

```

---

## 🔑 Notes

- Helm chart defines the **deployment, scaling, secrets, and services** for Kubernetes.
- `.env` and `values.yaml` hold **sensitive information**; never commit secrets.
- Fully **testable** via pytest.  
- Works **locally** with Docker Compose or **production-ready** on Kubernetes with GitOps deployment.

