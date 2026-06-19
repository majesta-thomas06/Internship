from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.templating import Jinja2Templates

from .database import SessionLocal
from .models import Employee, AuditLog
from .schemas import EmployeeCreate,EmployeeUpdate,EmployeeResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Employee + Audit Log
@router.post("/employees", response_model=EmployeeResponse)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    # Create Employee
    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        salary=employee.salary
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    # Create Audit Log
    audit_log = AuditLog(
        event_type="CREATE",
        table_name="employees",
        record_id=new_employee.id,
        old_value=None,
        new_value=str({
            "name": new_employee.name,
            "email": new_employee.email,
            "salary": new_employee.salary
        }),
        action_by="admin"
    )

    db.add(audit_log)
    db.commit()

    return new_employee


# Get All Employees
@router.get("/employees")
def get_all_employees(
    db: Session = Depends(get_db)
):
    employees = db.query(Employee).all()
    return employees


# Get Employee By ID
@router.get("/employees/{employee_id}")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee

@router.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    existing_employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not existing_employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Store old values for audit
    old_data = {
        "name": existing_employee.name,
        "email": existing_employee.email,
        "salary": existing_employee.salary
    }

    # Update employee
    existing_employee.name = employee.name
    existing_employee.email = employee.email
    existing_employee.salary = employee.salary

    db.commit()
    db.refresh(existing_employee)
    last_log = (
        db.query(AuditLog)
        .filter(AuditLog.record_id == employee_id)
        .order_by(AuditLog.version.desc())
        .first()
    )

    next_version = 1

    if last_log:
       next_version = last_log.version + 1

    audit_log = AuditLog(
        event_type="UPDATE",
        table_name="employees",
        record_id=existing_employee.id,  
        version=next_version,      
        old_value=str(old_data),
        new_value=str(employee.model_dump()),
        action_by="admin"
    )

    db.add(audit_log)
    db.commit()

    return {
        "message": "Employee updated successfully"
    }

@router.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    old_data = {
        "name": employee.name,
        "email": employee.email,
        "salary": employee.salary
    }

    # Get latest version
    last_log = (
        db.query(AuditLog)
        .filter(AuditLog.record_id == employee_id)
        .order_by(AuditLog.version.desc())
        .first()
    )

    next_version = 1

    if last_log:
       next_version = last_log.version + 1

    audit_log = AuditLog(
        event_type="DELETE",
        table_name="employees",
        record_id=employee.id,
        version=next_version,
        old_value=str(old_data),
        new_value=None,
        action_by="admin"
    )

    db.add(audit_log)

    db.delete(employee)

    db.commit()

    return {
        "message": "Employee deleted successfully"
    }

@router.get("/audit-logs")
def get_audit_logs(
    db: Session = Depends(get_db)
):
    return (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .all()
    )

@router.get("/audit-logs/{employee_id}")
def get_employee_history(
    employee_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(AuditLog)
        .filter(AuditLog.record_id == employee_id)
        .order_by(AuditLog.created_at.desc())
        .all()
    )

@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    employee_count = db.query(Employee).count()

    audit_count = db.query(AuditLog).count()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "employee_count": employee_count,
            "audit_count": audit_count
        }
    )

@router.get("/employees-ui")
def employees_ui(
    request: Request,
    db: Session = Depends(get_db)
):
    employees = db.query(Employee).all()

    return templates.TemplateResponse(
        request=request,
        name="employees.html",
        context={
            "request": request,
            "employees": employees
        }
    )

@router.get("/audit-ui")
def audit_ui(
    request: Request,
    employee_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog)

    if employee_id:
        query = query.filter(
            AuditLog.record_id == employee_id
        )

    logs = (
        query
        .order_by(AuditLog.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="audit_logs.html",
        context={
            "request": request,
            "logs": logs
        }
    )

@router.get("/history/{employee_id}")
def employee_history(
    employee_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    logs = (
        db.query(AuditLog)
        .filter(AuditLog.record_id == employee_id)
        .order_by(AuditLog.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "request": request,
            "logs": logs,
            "employee_id": employee_id
        }
    )