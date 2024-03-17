from connect_db import session
from models import Student, Group, Teacher, Subject, Student_subject, Grade
from datetime import datetime
from faker import Faker
from random import randint, choice

# ~30-50 студентов, 
# 3 группы, 
# 5-8 предметов, 
# 3-5 преподавателей, 
# до 20 оценок у каждого студента по всем предметам

NUMBER_STUDENT = 50     # (30 - 50)
NUMBER_GROUP = 3
NUMBER_STUDENTS_IN_GROUP = [15, 32, 18]
NUMBER_SUBJECT = 8      # (5 - 8)
NUMBER_TEACHER = 5      # (3 - 5)
NUMBER_GRADES = 20      # ( up to 20 grades for each students in all subjects )

fake = Faker()

def gen_fake_data(num_stud, num_subj, num_teachers):
    fake_students = []
    fake_group = ["Group_1", "Group_2", "Group_3"]
    fake_subject = ["Python", "SQL", "JavaScript", "HTML_CSS", "Datasigns", "Mathematics", "Databases", "OS"]
    fake_teacher = []
    fake_grades = [1,2,3,4,5]

    # fake = Faker()

    for _ in range(num_stud):
        fake_students.append(fake.name())

    # for _ in range(num_subj):
    #     fake_subject.append(fake.name())

    for _ in range(num_teachers):
        fake_teacher.append(fake.name())

    return fake_students, fake_group, fake_subject, fake_teacher, fake_grades


def prepare_data(studs, groups, subjects, teachers, grades):

    for_students = []
    id_stud = 1
    group = 1
    for student in studs:
        if id_stud > NUMBER_STUDENTS_IN_GROUP[0] and id_stud <= NUMBER_STUDENTS_IN_GROUP[1]:
            group = 2
        if id_stud > NUMBER_STUDENTS_IN_GROUP[1]:
            group = 3
        for_students.append((student, group))
        id_stud +=1

    for_groups = []
    for group in groups:
        for_groups.append((group, ))

    for_subjects = []
    for subject in subjects:
        for_subjects.append((subject, randint(1, NUMBER_TEACHER)))

    for_teachers = []
    for teacher in teachers:
        for_teachers.append((teacher, ))  

    for_students_subjects = []
    for subj_id in range(1, NUMBER_SUBJECT + 1):
        for stud_id in range(1, NUMBER_STUDENT + 1):
            for_students_subjects.append((stud_id, subj_id))

    # num variations of students - subjects
    num_var_stud_dub = NUMBER_STUDENT * NUMBER_SUBJECT
    for_grades = []
    for num_var in range(num_var_stud_dub):
        for _ in range(randint(15, NUMBER_GRADES)):
            for_grades.append((randint(1, 5), 
                               fake.date_between_dates(date_start=datetime(2022,9,1), date_end=datetime(2023,5,31))
                               , num_var+1))
            
    return for_students, for_groups, for_subjects, for_teachers, for_grades, for_students_subjects


if __name__ == '__main__':
    studs, groups, subjects, teachers, grades, studs_subjects = prepare_data(*gen_fake_data(NUMBER_STUDENT, NUMBER_SUBJECT, NUMBER_TEACHER))

    for gr in groups:
        group = Group(group_name = gr[0])
        session.add(group)
    session.commit()

    for stud in studs:
        student = Student(student_name = stud[0], group_id = stud[1])
        session.add(student)
    session.commit()

    for tch in teachers:
        teacher = Teacher(teacher_name = tch[0])
        session.add(teacher)
    session.commit()

    for sub in subjects:
        subject = Subject(subjects_name = sub[0], teacher_id = sub[1])
        session.add(subject)
    session.commit()

    for sts in studs_subjects:
        stud_sub = Student_subject(student_id = sts[0], subject_id = sts[1])
        session.add(stud_sub)
    session.commit()

    for gr in grades:
        grade = Grade(grade = gr[0], date_of = gr[1], student_subject_id = gr[2])
        session.add(grade)
    session.commit()

