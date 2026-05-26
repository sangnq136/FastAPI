from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URI = 'sqlite:///./todoapps.db'
# SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456a%40@localhost:5432/TodoApplicationDatabase"
# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/todoapplicationdatabase"
# engine = create_engine(SQLALCHEMY_DATABASE_URI)

# engine = create_engine(SQLALCHEMY_DATABASE_URI,connect_args={"check_same_thread":False})

SQLALCHEMY_DATABASE_URI = 'postgresql://fastapi_idra_user:NiVrt3QTjzsIN43OoiY64WNJptJj5PCy@dpg-d8ags54m0tmc73a336j0-a.ohio-postgres.render.com/fastapi_idra'
engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()