from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship

class School(Base):
    __tablename__ = 'school'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    school_name = Column('school_name', String(100), nullable=True)
    faculties = relationship('Faculty')

    def __init__(self, school_name):
        self.school_name = school_name


class Faculty(Base):
    __tablename__ = 'faculty'
    id = Column('id', Integer, primary_key=True)
    faculty = Column('faculty', String(100), nullable=True)
    school_id = Column('school_id', Integer, ForeignKey('school.id'))
    departments = relationship('Department')

    def __init__(self, faculty, school_id):
        self.faculty = faculty
        self.school_id = school_id


class Department(Base):
    __tablename__ = 'department'
    id = Column('id', Integer, primary_key=True)
    department = Column('department', String(100), nullable=True)
    faculty_id = Column('faculty_id', Integer, ForeignKey('faculty.id'))
    programs = relationship('Program')
    # lecturers = relationship('Lecturer')

    def __init__(self, department, faculty_id):
        self.department = department
        self.faculty_id = faculty_id


class Program(Base):
    __tablename__ = 'program'
    id = Column('id', Integer, primary_key=True)
    program = Column('program', String(100), nullable=True)
    department_id = Column('department_id', Integer,
                           ForeignKey('department.id'))
    # students = relationship('Student')

    def __init__(self, program, department_id):
        self.program = program
        self.department_id = department_id

class Level(Base):
    __tablename__ = 'level'
    id = Column('id', Integer, primary_key=True)
    level = Column('level', Integer, nullable=True)

    def __init__(self,level):
        self.level = level
