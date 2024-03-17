from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

# docker run --name orm_migrations -p 5432:5432 -e POSTGRES_PASSWORD=post_pass -d postgres
# docker ps
# docker exec -it orm_migrations bash
# psql -h localhost -U postgres
# CREATE DATABASE university; 
# CREATE DATABASE fortest; 
# DROP DATABASE university
# \l    - list of databases

engine = create_engine("postgresql+psycopg2://postgres:post_pass@localhost/university", echo=True)

Session = sessionmaker(bind=engine)
session = Session()
