from connect_db import session
from models import Student, Group, Teacher, Subject, Student_subject, Grade

# from datetime import datetime
# from random import randint, choice

# from sqlalchemy import Column, Integer, String, Boolean
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql.schema import ForeignKey, Table
# from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy import func, desc, select, column

class requests:

    def select_1():
        # -- Find the 5 students with the highest average score in all subjects.
        # SELECT s.student_name, sb.subjects_name, round(AVG(g.grade), 3) AS grade 
        # FROM students_subjects sts
        # LEFT JOIN grades g ON g.student_subject_id = sts.id 
        # LEFT JOIN students s ON s.id = sts.student_id 
        # LEFT JOIN subjects sb ON sb.id = sts.subject_id  
        # GROUP BY sts.subject_id, sts.student_id, s.student_name, sb.subjects_name
        # ORDER BY grade DESC 
        # LIMIT 5
        
        res = session.query(Student.student_name, Subject.subjects_name, func.round(func.avg(Grade.grade), 3).label('grade'))\
            .select_from(Student_subject).join(Grade).join(Student).join(Subject)\
                .group_by(Student_subject.subject_id, Student_subject.student_id, Student.student_name, Subject.subjects_name)\
                    .order_by(desc('grade')).limit(5).all()
        
        return res

    def select_2():
        # SELECT s.student_name, sb.subjects_name, AVG(g.grade) AS grade
        # FROM students_subjects sts 
        # LEFT JOIN grades g ON g.student_subject_id = sts.id 
        # LEFT JOIN students s ON s.id = sts.student_id 
        # LEFT JOIN subjects sb ON sb.id = sts.subject_id  
        # WHERE sts.subject_id  = 7
        # GROUP BY sts.student_id , s.student_name, sb.subjects_name
        # ORDER BY grade DESC 
        # LIMIT 1

        res = session.query(Student.student_name, Subject.subjects_name, func.round(func.avg(Grade.grade), 2).label('grade'))\
            .select_from(Student_subject).join(Grade).join(Student).join(Subject)\
            .filter(Student_subject.subject_id == 7)\
            .group_by(Student_subject.student_id, Student.student_name, Subject.subjects_name)\
            .order_by(desc('grade')).limit(1).all()
        
        return res
    
    def select_3():
        # SELECT gr.group_name, round(AVG(g.grade), 2) AS grade 
        # FROM grades g
        # LEFT JOIN students_subjects sts ON sts.id = g.student_subject_id 
        # LEFT JOIN students st ON st.id = sts.student_id 
        # RIGHT JOIN groups gr ON gr.id = st.group_id 
        # LEFT JOIN subjects s ON s.id = sts.subject_id 
        # WHERE s.id = 7
        # GROUP BY gr.id 

        res = session.query(Group.group_name, func.round(func.avg(Grade.grade), 2).label('grade'))\
            .select_from(Grade).join(Student_subject).join(Student).join(Group).join(Subject)\
            .filter(Subject.id == 7)\
            .group_by(Group.id).all()

        return res
    
    def select_4():
        # SELECT AVG(g.grade) AS grade 
        # FROM grades g
        # LEFT JOIN students_subjects sts ON sts.id = g.student_subject_id 
        # LEFT JOIN subjects s ON s.id = sts.subject_id 

        res = session.query(func.round(func.avg(Grade.grade), 5).label('grade'))\
            .select_from(Grade).join(Student_subject).join(Subject).all()

        return res

    def select_5():
        # SELECT s.subjects_name, t.teacher_name 
        # FROM subjects s  
        # LEFT JOIN teachers t ON t.id = s.teacher_id 
        # WHERE t.id = 4

        res = session.query(Subject.subjects_name, Teacher.teacher_name)\
            .select_from(Subject).join(Teacher).filter(Teacher.id == 4).all()
        
        return res
    
    def select_6():
        # SELECT s.student_name, g.group_name  
        # FROM students s
        # LEFT JOIN groups g ON g.id = s.group_id 
        # WHERE g.id = 3

        res = session.query(Student.student_name, Group.group_name)\
            .select_from(Student).join(Group).filter(Group.id == 3).all()
        
        return res    

    def select_7():
        # SELECT s.student_name, gr.group_name, sb.subjects_name, g.grade 
        # FROM grades g 
        # LEFT JOIN students_subjects sts ON sts.id = g.student_subject_id 
        # LEFT JOIN students s ON s.id = sts.student_id 
        # RIGHT JOIN groups gr ON gr.id = s.group_id 
        # right JOIN subjects sb ON sb.id = sts.subject_id 
        # WHERE sb.id = 5 AND gr.id = 3

        res = session.query(Student.student_name, Group.group_name, Subject.subjects_name, Grade.grade)\
            .select_from(Grade).join(Student_subject).join(Student).join(Group).join(Subject)\
            .filter(Subject.id == 5, Group.id == 3).all()

        return res

    def select_8():
        # SELECT t.teacher_name, s.subjects_name, round(AVG(g.grade), 3) AS grade
        # FROM grades g 
        # LEFT JOIN students_subjects sts ON sts.id = g.student_subject_id 
        # RIGHT JOIN subjects s ON s.id = sts.subject_id 
        # LEFT JOIN teachers t ON t.id = s.teacher_id 
        # WHERE t.id = 3
        # GROUP BY s.id, t.teacher_name

        res = session.query(Teacher.teacher_name, Subject.subjects_name, func.round(func.avg(Grade.grade), 3).label('grade'))\
            .select_from(Grade).join(Student_subject).join(Subject).join(Teacher)\
            .filter(Teacher.id == 3)\
            .group_by(Subject.id, Teacher.id).all()

        return res
    
    def select_9():
        # SELECT s.student_name, sb.subjects_name 
        # FROM students s 
        # LEFT JOIN students_subjects sts ON sts.student_id  = s.id 
        # LEFT JOIN subjects sb ON sb.id = sts.subject_id 
        # WHERE s.id = 7

        res = session.query(Student.student_name, Subject.subjects_name)\
            .select_from(Student).join(Student_subject).join(Subject)\
            .filter(Student.id == 7).all()

        return res    

    def select_10():
        # SELECT s.subjects_name, st.student_name, t.teacher_name 
        # FROM subjects s 
        # LEFT JOIN teachers t ON t.id = s.teacher_id 
        # LEFT JOIN students_subjects sts ON sts.subject_id = s.id 
        # LEFT JOIN students st on st.id = sts.student_id 
        # WHERE st.id = 7 AND t.id = 3

        res = session.query(Subject.subjects_name, Student.student_name, Teacher.teacher_name)\
            .select_from(Subject).join(Teacher).join(Student_subject).join(Student)\
            .filter(Student.id == 7, Teacher.id == 3).all()

        return res

    def select_11():
        # SELECT t.teacher_name, s.student_name, round(AVG(g.grade), 3) AS grade 
        # FROM grades g 
        # LEFT JOIN students_subjects sts ON sts.id = g.student_subject_id 
        # RIGHT JOIN subjects sb ON sb.id = sts.subject_id 
        # LEFT JOIN teachers t ON t.id = sb.teacher_id 
        # RIGHT JOIN students s ON s.id = sts.student_id 
        # WHERE t.id = 3 AND s.id = 7
        # GROUP BY s.id, t.id 

        res = session.query(Teacher.teacher_name, Student.student_name, func.round(func.avg(Grade.grade), 3).label('grade'))\
            .select_from(Grade).join(Student_subject).join(Subject).join(Teacher).join(Student)\
            .filter(Teacher.id == 3, Student.id == 7)\
            .group_by(Student.id, Teacher.id).all()

        return res
    
    def select_12():
        # SELECT s.student_name, sb.subjects_name, gr.group_name, g.grade, g.date_of
        # FROM grades g
        # LEFT JOIN students_subjects sts ON sts.id = g.student_subject_id  
        # RIGHT JOIN students s ON s.id = sts.student_id 
        # LEFT JOIN groups gr ON gr.id = s.group_id 
        # RIGHT JOIN subjects sb ON sb.id = sts.subject_id 
        # WHERE gr.id = 3 AND sb.id = 3 AND g.date_of = (SELECT MAX(date_of) FROM grades)

        scalar_subquery = (session.query(func.max(Grade.date_of).label('date'))).select_from(Grade).scalar_subquery()

        res = session.query(Student.student_name, Subject.subjects_name, Group.group_name, Grade.grade, Grade.date_of)\
            .select_from(Grade).join(Student_subject).join(Student).join(Group).join(Subject)\
            .filter(Group.id == 3, Subject.id == 3, Grade.date_of == scalar_subquery).all()

        return res    


    def view_res(res):
        print("-"*30)
        print(f"\n + {res}")
    

if __name__ == '__main__':
    request = requests
    res = request.select_12()
    request.view_res(res)