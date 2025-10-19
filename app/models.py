from sqlalchemy import Column , Integer, String, ForeignKey, CheckConstraint, DateTime, func, Index
from app.database import Base
from sqlalchemy.orm import relationship

# create User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable= False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    membership = relationship("OrgMembership", back_populates="user", cascade="all, delete-orphan")
    tasks_assigned = relationship("Task", back_populates="assignee")

# create organization model
class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    memberships = relationship("OrgMembership", back_populates="organization", cascade= "all, delete-orphan")
    projects = relationship("Project", back_populates="organization", cascade="all, delete-orphan")


# Organization membership model
class OrgMembership(Base):
    __tablename__ = "org_memberships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="membership")
    organization = relationship("Organization", back_populates="memberships")

    __table_args__ = (
        CheckConstraint(
            # one membership per user
            "role IN ('OWNER', 'ADMIN', 'MEMBER', 'VIEWER')",
            name = "ck_role_appropriate"              
        ),
        Index("one_member_per_membership", "user_id", "organization_id", unique=True)

)

# Project model    
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organizations.id",ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    organization = relationship("Organization", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_project_org_name", "org_id", "name", unique=True),
    )

# Tasks model 
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, server_default="TODO")
    assignee_id= Column(Integer, ForeignKey("users.id"), nullable=True)
    priority = Column(String, nullable=False, server_default="normal")
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks_assigned")

    __table_args__ = (
        CheckConstraint(
            "status IN ('TODO', 'DOING', 'DONE')",
            name = "ck_task_status"
        ),
        CheckConstraint(
            "priority IN ('low', 'normal', 'high')",
            name = "ck_task_priority"
        ),
        Index("ix_task_project_status", "project_id", "status")
    )









    

