from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = 'sqlite:///./todoapps.db'
# SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456a%40@localhost:5432/TodoApplicationDatabase"
# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/todoapplicationdatabase"
# engine = create_engine(SQLALCHEMY_DATABASE_URI)

engine = create_engine(SQLALCHEMY_DATABASE_URI,connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()