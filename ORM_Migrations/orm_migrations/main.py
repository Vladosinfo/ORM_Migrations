from connect_db import session
from models import Student, Group, Teacher, Subject, Student_subject, Grade
import argparse

### --------------------------------------------
# docker run --name orm_migrations -p 5432:5432 -e POSTGRES_PASSWORD=post_pass -d postgres
# engine = create_engine("postgresql+psycopg2://postgres:post_pass@localhost/postgres")

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--action", type=str, choices=["create", "list", "update", "remove", "item"], 
                    help="CRUD action: create, list, update or remove")
parser.add_argument("-m", "--model", type=str, choices=["student", "teacher", "group", "subject"], 
                    help="for note with what model we are working")
parser.add_argument("-n", "--name", type=str, help="name of the instance we want to work with")
parser.add_argument("-rid", "--rel_id", type=int, default=1, help="id of related object")
parser.add_argument("-id", "--id", type=int, help="id of the instance we want to work with")
args = parser.parse_args()


OBJ_LIST = {
    "student": "student",
    "teacher": "teacher",
    "group": "group",
    "subject": "subject"
}

def models(model):
    if model == OBJ_LIST['student']:
        return Student
    elif model == OBJ_LIST['teacher']:
        return Teacher
    elif model == OBJ_LIST['group']:
        return Group
    elif model == OBJ_LIST['subject']:
        return Subject
    else:
        return None

def create(args, instance=None):
    if args.model == OBJ_LIST["teacher"]:
        if instance == None:
            teacher =  Teacher(teacher_name = args.name)
            session.add(teacher)
        elif instance != None:
            instance.teacher_name = args.name
            session.add(instance)
        session.commit()
    if args.model == OBJ_LIST["student"]:
        if instance == None:
            student = Student(student_name = args.name, group_id = args.rel_id)
            session.add(student)
        elif instance != None:
            instance.student_name = args.name             
            session.add(instance)
        session.commit()
    if args.model == OBJ_LIST["group"]:
        if instance == None:
            group = Group(group_name = args.name)
            session.add(group)
        elif instance != None:
            instance.group_name = args.name             
            session.add(instance)
        session.commit()        
    if args.model == OBJ_LIST["subject"]:
        if instance == None:
            subject = Subject(subjects_name = args.name, teacher_id = args.rel_id)
            session.add(subject)
        elif instance != None:
            instance.subjects_name = args.name             
            session.add(instance)
        session.commit()         
    return True

def show_res(res):
    for item in res:
        print(item)

def list(args):
    items = session.query(models(args.model)).all()
    res = []
    for item in items:
        if args.model == OBJ_LIST["teacher"]:
            res.append(f"Id: {item.id}, Name: {item.teacher_name}")
        if args.model == OBJ_LIST["student"]:
            res.append(f"Id: {item.id}, Name: {item.student_name}, GroupId: {item.group_id}")
        if args.model == OBJ_LIST["group"]:
            res.append(f"Id: {item.id}, Group name: {item.group_name}")
        if args.model == OBJ_LIST["subject"]:
            res.append(f"Id: {item.id}, Name: {item.subjects_name}, TeacherId: {item.teacher_id}")    

    show_res(res)

def item(args):
    model = models(args.model)
    if args.model == OBJ_LIST["teacher"]:
        item = session.query(model.id, model.teacher_name).select_from(model).filter(model.id == args.id).first()
    elif args.model == OBJ_LIST["student"]:
        item = session.query(model.id, model.student_name, model.group_id).select_from(model).filter(model.id == args.id).first()
    elif args.model == OBJ_LIST["group"]:
        item = session.query(model.id, model.group_name).select_from(model).filter(model.id == args.id).first()
    elif args.model == OBJ_LIST["subject"]:
        item = session.query(model.id, model.subjects_name, model.teacher_id).select_from(model).filter(model.id == args.id).first()
    # item = session.query(model).filter(model.id == args.id).first()
    print(item)

def update(args):
    model = session.query(models(args.model)).get(args.id)
    create(args, model)

def remove(args):
    if args.id != None:
        model = session.query(models(args.model)).get(args.id)
        session.delete(model)
        session.commit()


COMMAND_HANDLER = {
    "create": create,
    "list": list,
    "update": update,
    "remove": remove,
    "item": item
}

def command_handler(command):
    handler = COMMAND_HANDLER.get(command)
    return handler

def main():
    # print(f"args: {args}")
    # print(f"model: {args.model}")
    handler = command_handler(args.action)
    handler(args)


if __name__ == '__main__':
    main()
    