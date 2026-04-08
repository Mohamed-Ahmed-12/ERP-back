# ERP Backend

[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/Mohamed-Ahmed-12/ERP-back)

A modular and scalable ERP backend built with Django and Django REST Framework. This system is designed with a plug-and-play architecture, allowing different business modules like Human Resources (HR) and Equipment Management to be enabled or disabled as needed.

## ✨ Features

*   **Modular Architecture**: Core modules like HR and Equipment can be included or excluded from the `INSTALLED_APPS` without breaking the system. The application gracefully handles optional dependencies.
*   **JWT Authentication**: Secure, token-based authentication using `djangorestframework-simplejwt`.
*   **Human Resources (HR) Module**:
    *   Employee and department management.
    *   Job positions, vacancies, and candidate tracking.
    *   Attendance logging (check-in/check-out).
    *   Workflow for job change requests (promotions, transfers).
*   **Equipment Management Module**:
    *   Track equipment, including type, brand, model, and status.
    *   Assign main and sub-drivers to equipment.
    *   Automatically syncs driver information from the HR module if installed, or allows local entry otherwise.
*   **Core System Features**:
    *   UUID-based primary keys for all models.
    *   Soft-delete functionality to prevent accidental data loss.
    *   Centralized dashboard for key statistics.
*   **Containerized Deployment**: Fully containerized with Docker and Docker Compose for easy setup in both development and production environments.

## 🛠️ Tech Stack

*   **Backend**: Django, Django REST Framework
*   **Database**: PostgreSQL
*   **Authentication**: djangorestframework-simplejwt
*   **Web Server**: Gunicorn
*   **Reverse Proxy**: Nginx
*   **Containerization**: Docker, Docker Compose

## 🚀 Getting Started

### Prerequisites

*   Docker
*   Docker Compose

### 1. Clone the Repository

```bash
git clone https://github.com/mohamed-ahmed-12/ERP-back.git
cd ERP-back
```

### 2. Configuration

Create a `.env` file by copying the example file. This file will hold your environment-specific configurations.

```bash
cp env.example .env
```

Open the `.env` file and generate a new `SECRET_KEY`. You can use an online generator or Django's command-line utility. All other variables can typically remain as their default values for local development.

```ini
# .env
SECRET_KEY=your-super-secret-key-goes-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=appdb
POSTGRES_USER=appuser
POSTGRES_PASSWORD=changeme

DATABASE_URL=postgres://appuser:changeme@db:5432/appdb
```

### 3. Running in Development Mode

This mode uses Django's development server with hot-reloading.

```bash
docker-compose -f docker-compose.dev.yml up --build
```

The API will be available at `http://localhost:8000`.

### 4. Running in Production Mode

This mode uses Gunicorn and Nginx for a production-ready setup. For production, set `DEBUG=False` in your `.env` file.

```bash
docker-compose -f docker-compose.yml up --build -d
```

The API will be available at `http://localhost:80`.

## Architectural Highlights

### Soft Deletion

All models inherit from a `BaseModel` which includes a `is_deleted` flag and a `deleted_at` timestamp. The default manager (`objects`) automatically filters out soft-deleted records. To include them, you can use `Model.objects.with_deleted()`.

### Modular Inter-App Communication

The system is designed to avoid hard dependencies between modules.

*   **Optional Foreign Keys**: The `core.mixins.OptionalFKMixin` is used to create relationships between models in different apps (e.g., an `Equipment` having a `main_driver` from the `hr.Employee` model) without raising `ImportError` if the related app is not installed. It stores the foreign key as a simple `UUIDField` and resolves the object at runtime.

*   **Signal-based Data Synchronization**: The `equipment` module listens for `post_save` and `post_delete` signals from the `hr.Employee` model. If the HR module is installed, it automatically creates or updates a local, lightweight `EquipmentEmployee` record. This keeps driver data in sync without creating a rigid dependency.

### Read/Write Serializer Pattern

The API uses separate serializers for read and write operations.
*   **Read Serializers** (`...ReadSerializer`) provide rich, nested representations of objects, making it easy for frontends to display related data.
*   **Write Serializers** (`...WriteSerializer`) accept flat primary keys (UUIDs) for creating and updating relationships, simplifying the payload for `POST` and `PUT` requests.

## API Endpoints

All endpoints are prefixed with `/api/`.

| Endpoint                                       | Method | Description                                    |
| ---------------------------------------------- | ------ | ---------------------------------------------- |
| `/accounts/login/`                             | `POST` | Obtain JWT access and refresh tokens.          |
| `/accounts/token/refresh/`                       | `POST` | Refresh an expired access token.               |
| `/accounts/me/`                                | `GET`  | Get the profile of the authenticated user.     |
| `/core/modules/installed`                      | `GET`  | Check which optional modules are installed.    |
| `/dashboard/stats/`                            | `GET`  | Get basic dashboard statistics.                |
| `/hr/departments/`                             | `CRUD` | Manage departments.                            |
| `/hr/positions/`                               | `CRUD` | Manage job positions.                          |
| `/hr/employees/`                               | `CRUD` | Manage employees.                              |
| `/hr/attendance/`                              | `CRUD` | Manage employee attendance records.            |
| `/hr/vacancies/`                               | `CRUD` | Manage job vacancies.                          |
| `/hr/candidates/`                              | `CRUD` | Manage candidates for vacancies.               |
| `/hr/job-change-requests/`                     | `CRUD` | Manage employee job change requests.           |
| `/equipments/equipments/`                      | `CRUD` | Manage equipment.                              |
| `/equipments/types/`                             | `CRUD` | Manage equipment types.                        |
| `/equipments/brands/`                            | `CRUD` | Manage equipment brands.                       |
| `/equipments/equipment-employee/`              | `CRUD` | Manage local driver records.                   |