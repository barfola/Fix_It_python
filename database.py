from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

fix_it_db_path = r"D:\Cyber\project\db\fixitdb.db"
DATABASE_URL = f"sqlite:///{fix_it_db_path}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
