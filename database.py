from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
metadata = MetaData()

engine = create_engine(
    f"postgresql+psycopg2://nocode_user:banana@localhost/nocode"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class Organization(Base):
    __table__ = Table("organization", metadata, autoload_with=engine)