from connect_db import session
from models import Student, Group, Teacher, Subject, Student_subject, Grade

from datetime import datetime
from random import randint, choice

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy import func, desc, select, column

def select_1():
    return session.query(Student.student_name, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()

def select_2():
    pass
    

if __name__ == '__main__':
    select_1()