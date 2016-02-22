from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String(100))
    maximum_capacity = Column(Integer)
    current_occupancy = Column(Integer)


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    picture = Column(String)
    description = Column(String(250))


association_table = Table('association', Base.metadata,
    Column('adopter_id', Integer, ForeignKey('adopter.id')),
    Column('puppy_id', Integer, ForeignKey('puppy.id'))
)

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    profile_id = Column(Integer, ForeignKey('profile.id'))
    shelter = relationship(Shelter)
    profile = relationship(Profile)
    adopter = relationship(
        "Adopter",
        secondary=association_table,
        back_populates="adopted_puppies")
    weight = Column(String(20))


class Adopter(Base):
    __tablename__ = 'adopter'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    adopted_puppies = relationship(
        "Puppy",
        secondary=association_table,
        back_populates="adopter")


engine = create_engine('sqlite:///puppyshelter.db')
 

Base.metadata.create_all(engine)
