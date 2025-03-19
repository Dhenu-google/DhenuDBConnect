from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CowBreed(Base):
    __tablename__ = 'cow_breeds'

    id = Column(Integer, primary_key=True)
    breed = Column(String(255), nullable=False)
    state = Column(String(255))
    places = Column(String(255))
    longitude = Column(Float)
    latitude = Column(Float)
    population = Column(Integer)
    synonyms = Column(String(255))
    origin = Column(String(255))
    major_utility = Column(String(255))
    comments_on_utility = Column(String(255))
    comments_on_breeding_tract = Column(String(255))
    adaptability_to_environment = Column(String(255))
    management_system = Column(String(255))
    mobility = Column(String(255))
    feeding_of_adults = Column(String(255))
    comments_on_management = Column(String(255))
    colour = Column(String(255))
    horn_shape_and_size = Column(String(255))
    visible_characteristics = Column(String(255))
    height_avg_cm = Column(Float)
    body_length_avg_cm = Column(Float)
    heart_girth_avg_cm = Column(Float)
    body_weight_avg_kg = Column(Float)
    birth_weight_avg_kg = Column(Float)
    litter_size_born = Column(Integer)
    age_at_first_parturition_months = Column(Integer)
    parturition_interval_months = Column(Integer)
    milk_yield_per_lactation_kg = Column(Float)
    milk_fat_percent = Column(Float)
    peculiarity_of_breed = Column(String(255))

class CowDisease(Base):
    __tablename__ = 'cow_diseases'

    id = Column(Integer, primary_key=True)
    cow_id = Column(Integer, ForeignKey('cows.id'), nullable=False)
    disease_id = Column(Integer, ForeignKey('diseases.id'), nullable=False)
    outcome = Column(String(255))  # Outcome of the disease (e.g., "Recovered", "Fatal")
    diagnosis_date = Column(Date)  # Date of diagnosis
    cost = Column(Float)  # Cost of treatment
    treatment_date = Column(Date)  # Date of treatment

    # Relationships to Cow and Disease
    cow = relationship('Cow', back_populates='cow_diseases')
    disease = relationship('Disease', back_populates='cow_diseases')

class Cow(Base):
    __tablename__ = 'cows'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(255))
    breed_id = Column(Integer, ForeignKey('cow_breeds.id'))
    dob = Column(Date)
    health_status = Column(String(255))
    milk_production = Column(Float)
    work = Column(String(255))
    breed = relationship('CowBreed', back_populates='cows')
    cow_diseases = relationship('CowDisease', back_populates='cow')  # Link to CowDisease

CowBreed.cows = relationship('Cow', back_populates='breed')

class Disease(Base):
    __tablename__ = 'diseases'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    date_diagnosed = Column(Date)
    treatment = Column(String(255))
    cow_id = Column(Integer, ForeignKey('cows.id'))
    cow_diseases = relationship('CowDisease', back_populates='disease')  # Link to CowDisease

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255))
    phone = Column(String(10))
    email = Column(String(255), unique=True)
    cows = relationship('Cow', back_populates='owner')
    role = Column(String(255), default='farmer', nullable=False)
    role_options = ['farmer', 'NGO', 'gaushala', 'normal']
    capacity = Column(Integer, default=1)
    oauthID = Column(String(255), unique=True)

Cow.owner = relationship('User', back_populates='cows')