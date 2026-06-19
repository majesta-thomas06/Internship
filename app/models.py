from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    salary = Column(Integer)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    event_type = Column(String(50), nullable=False)

    table_name = Column(String(100), nullable=False)

    record_id = Column(Integer, nullable=False)

    version = Column(Integer, default=1)

    old_value = Column(Text)

    new_value = Column(Text)

    action_by = Column(String(100))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )