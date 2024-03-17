from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()

# alembic revision --autogenerate -m 'Init'
# alembic upgrade head

# Table: groups
class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    group_name = Column(String(40), nullable=False, unique=True)

# Table: students
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    student_name = Column(String(40), nullable=False, unique=True)
    group_id = Column(Integer, ForeignKey(Group.id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    relationship("Group", cascade="all, delete", backref="student")
    relationship("Subject", secondary="students_subjects", backref="students", passive_deletes=True, passive_updates=True)

# Table: teachers
class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    teacher_name = Column(String(40), nullable=False, unique=True)

# Table: subjects
class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    subjects_name = Column(String(40), nullable=False, unique=True)
    teacher_id = Column(Integer, ForeignKey(Teacher.id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    relationship("Teacher", cascade="all, delete", backref="subject")

# Table: students_subjects
class Student_subject(Base):
    __tablename__ = "students_subjects"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey(Student.id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)    
    subject_id = Column(Integer, ForeignKey(Subject.id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)    

# students_subjects = Table(
#     "students_subjects",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
#     Column("subject_id", Integer, ForeignKey("subjects.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
# )

# Table: grades
class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    # grade = Column(String(40), nullable=False)
    date_of = Column(DateTime, default=datetime.now())
    student_subject_id = Column(Integer, ForeignKey(Student_subject.id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    relationship("Student_subject", backref="grade", passive_deletes=True, passive_updates=True)
    # student_subject_id = Column(Integer, ForeignKey("students_subjects.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    # relationship("students_subjects", backref="grade", passive_deletes=True, passive_updates=True)
