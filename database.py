from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./ortho.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Rep(Base):
    __tablename__ = "reps"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hospital = Column(String)
    specialty = Column(String)

class Procedure(Base):
    __tablename__ = "procedures"
    id = Column(Integer, primary_key=True)
    type = Column(String)

class Case(Base):
    __tablename__ = "cases"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    revenue = Column(Float)

    rep_id = Column(Integer, ForeignKey("reps.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    procedure_id = Column(Integer, ForeignKey("procedures.id"))

    rep = relationship("Rep")
    doctor = relationship("Doctor")
    procedure = relationship("Procedure")

class Visit(Base):
    __tablename__ = "visits"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    notes = Column(String)

    rep_id = Column(Integer, ForeignKey("reps.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    rep = relationship("Rep")
    doctor = relationship("Doctor")

def init_db():
    Base.metadata.create_all(bind=engine)
