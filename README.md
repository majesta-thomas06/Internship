# Audit Tracking Framework

A backend-driven web application for **employee management, audit logging, version tracking, and record traceability**.

The framework automatically records important employee data changes as audit events, allowing users to inspect what changed, view previous and updated values, identify the action performed, and track the version history of an employee record.

## 🚀 Features

### 👤 Employee Management

* Create employee records through REST APIs
* Retrieve all employees
* Retrieve an employee by ID
* Update employee information
* Delete employee records
* Store employee name, email, and salary

### 📝 Automated Audit Logging

Employee operations automatically generate audit records.

The framework records:

* Event type — `CREATE`, `UPDATE`, or `DELETE`
* Table name
* Record ID
* Version number
* Previous value
* New value
* Action performed by
* Timestamp

### 🔢 Version Tracking

Each employee's audit history maintains a version number.

For example:

```text
Employee #1

CREATE  → Version 1
UPDATE  → Version 2
UPDATE  → Version 3
DELETE  → Version 4
```

This makes it possible to trace the sequence of changes made to a record.

### 🔍 Employee History

A dedicated history view allows users to inspect the audit trail associated with an employee.

The history displays:

* Event
* Old value
* New value
* Action by
* Created timestamp
* Version

### 📊 Dashboard

The dashboard provides a simple overview of:

* Total employees
* Total audit logs

It also provides navigation to the employee and audit-log interfaces.

### 🔎 Audit Log Filtering

Audit logs can be filtered using an employee ID to inspect the audit activity associated with a specific record.

---

## 🏗️ Architecture

```text
                  ┌──────────────────────┐
                  │       User           │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Bootstrap + Jinja2   │
                  │    Web Interface     │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │       FastAPI        │
                  │      REST APIs       │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     SQLAlchemy       │
                  │         ORM          │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     PostgreSQL       │
                  │       Database       │
                  └──────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology      | Purpose                      |
| --------------- | ---------------------------- |
| **Python**      | Application development      |
| **FastAPI**     | REST API development         |
| **SQLAlchemy**  | ORM and database interaction |
| **PostgreSQL**  | Persistent data storage      |
| **Pydantic**    | Request/response validation  |
| **Jinja2**      | Server-side HTML templating  |
| **Bootstrap 5** | Web interface styling        |
| **Uvicorn**     | ASGI application server      |
| **Git/GitHub**  | Version control              |

---

## 📁 Project Structure

```text
Internship-main/
│
├── app/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── schemas.py
│
├── templates/
│   ├── dashboard.html
│   ├── employees.html
│   ├── audit_logs.html
│   └── history.html
│
├── requirements.txt
└── README.md
```

### Core Files

**`app/main.py`**

Initializes the FastAPI application, database tables, routes, and application configuration.

**`app/database.py`**

Configures the SQLAlchemy database engine, session factory, and declarative base.

**`app/models.py`**

Defines the database models:

* `Employee`
* `AuditLog`

**`app/schemas.py`**

Defines Pydantic schemas used for employee creation, updates, and API responses.

**`app/routes.py`**

Contains the employee APIs, audit-log APIs, dashboard routes, and UI routes.

---

## 🗄️ Database Models

### Employee

```text
employees
├── id
├── name
├── email
└── salary
```

### AuditLog

```text
audit_logs
├── id
├── event_type
├── table_name
├── record_id
├── version
├── old_value
├── new_value
├── action_by
└── created_at
```

---

## 🔄 Audit Flow

When an employee record is created:

```text
Create Employee
      │
      ▼
Save Employee
      │
      ▼
Generate CREATE Audit Log
      │
      ▼
Store New Value
      │
      ▼
Version 1
```

When an employee is updated:

```text
Existing Employee
      │
      ▼
Capture Old Values
      │
      ▼
Update Employee
      │
      ▼
Find Latest Version
      │
      ▼
Increment Version
      │
      ▼
Create UPDATE Audit Log
      │
      ▼
Store Old + New Values
```

When an employee is deleted:

```text
Employee
   │
   ▼
Capture Existing Values
   │
   ▼
Calculate Next Version
   │
   ▼
Create DELETE Audit Log
   │
   ▼
Delete Employee
```

---

## 🔌 API Endpoints

### Employee APIs

| Method   | Endpoint                   | Description                             |
| -------- | -------------------------- | --------------------------------------- |
| `POST`   | `/employees`               | Create an employee and audit record     |
| `GET`    | `/employees`               | Retrieve all employees                  |
| `GET`    | `/employees/{employee_id}` | Retrieve an employee                    |
| `PUT`    | `/employees/{employee_id}` | Update employee and create audit record |
| `DELETE` | `/employees/{employee_id}` | Delete employee and create audit record |

### Audit APIs

| Method | Endpoint                    | Description                            |
| ------ | --------------------------- | -------------------------------------- |
| `GET`  | `/audit-logs`               | Retrieve audit logs                    |
| `GET`  | `/audit-logs/{employee_id}` | Retrieve audit history for an employee |

### Web Interface

| Method | Endpoint                 | Description         |
| ------ | ------------------------ | ------------------- |
| `GET`  | `/dashboard`             | Dashboard           |
| `GET`  | `/employees-ui`          | Employee interface  |
| `GET`  | `/audit-ui`              | Audit-log interface |
| `GET`  | `/history/{employee_id}` | Employee history    |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd Internship-main
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database named:

```text
audit_framework
```

Before publishing the repository, configure the database connection using environment variables rather than committing database credentials.

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

The application will be available locally through the Uvicorn server.

FastAPI's interactive API documentation is also available through:

```text
/docs
```

---

## 🖥️ Application Views

The application currently includes:

### Dashboard

Displays the total number of employees and total audit logs.

### Employees

Displays employee records and provides access to individual employee history.

### Audit Logs

Displays audit events with event type, record ID, action, timestamp, and version.

### Employee History

Displays the complete audit history for a selected employee, including old and new values.

> Add screenshots of these four views here once the GitHub repository is ready.

---

## 🎯 Project Objective

The objective of the Audit Tracking Framework is to provide a structured mechanism for monitoring changes to employee records and maintaining an accessible history of those changes.

Instead of only storing the latest state of an employee record, the system maintains an associated audit trail containing the sequence of operations performed on the record.

---

## 🔮 Future Enhancements

Potential extensions include:

* Authentication and authorization
* Role-based access control
* More granular action tracking
* Advanced audit-log search and filtering
* Side-by-side version comparison
* Audit report generation
* Export audit logs
* Improved dashboard analytics
* Cloud deployment
* Secure environment-based configuration

---

## 📌 Project Status

**Status: Active Development**

The current implementation provides employee CRUD operations, automated audit logging, version tracking, employee history, audit filtering, and a web-based dashboard.

---

## 👨‍💻 Author

**Majesta Thomas**

Pre-final Year Software Engineering Student
Interested in AI/ML, Agentic AI, Backend Development, and Cloud Technologies.
