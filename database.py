# Database 
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, Session,session,sessionmaker,relationship
from sqlalchemy import String,Integer, Boolean,create_engine,ForeignKey
from typing import List

class Base(DeclarativeBase):
    pass

try:
    engine=create_engine('postgresql://postgres:123456789@127.0.0.1:5432/postgres',echo=False)
    print("Connection Okey") 
    
except Exception as er:
    print(er)
    print("connction is not successful ")
    
with Session(engine) as session:
    Session = sessionmaker(bind=engine)
    session = Session()
    
class Academy(Base):
    __tablename__ = 'academy'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(nullable=False)
    course:Mapped[str] = mapped_column(nullable=False)
    fee:Mapped[float] = mapped_column(nullable=False)
    student:Mapped[List["Student"]]=relationship()
    
    def __init__(self,id,name,course,fee):
        self.id = id,
        self.name = name,
        self.course = course,
        self.fee = fee
        
        return self


    @staticmethod
    def get_academy(id):
        academy = session.query(Academy).filter_by(id=id).first()
        return academy
    
    
    @staticmethod
    def get_all_academy():
       academies= session.query(Academy).all()
       return academies
   
   
    @staticmethod
    def get_lastid():
        # sort before having last id
        academy = session.query(Academy).order_by(Academy.id.desc()).first()   #provide row here
        return academy.id
        
        
    @staticmethod
    def add_academy(name,course,fee):
        id = Academy.get_lastid()+1
        academy = Academy(id,name,course,fee)
        session.add(academy)
        session.commit()
        academy = Academy.get_academy(id)
        return academy
        
    def update_academy(self,name=None,course=None,fee=None):
        academy = Academy.get_academy(self.id)
        if name:
            academy.name = name
        
        if course:
            academy.course = course
            
        if fee:
            academy.fee = fee
        session.commit()
        
        updated_academy = Academy.get_academy(self.id)
        return updated_academy
        

class Student(Base):
    __tablename__='student'
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(nullable=True)
    # academy:Mapped[str] = mapped_column(nullable=False)
    fee_paid:Mapped[int] = mapped_column(nullable=False)
    is_dropout:Mapped[bool]=mapped_column(nullable=False)
    first_session_clear:Mapped[bool] = mapped_column(nullable=False)
    second_session_clear:Mapped[bool] = mapped_column(nullable=False)
    academy_id:Mapped[int]=mapped_column(ForeignKey("academy.id"))
    
    def __init__(self,id,name,academy_id,fee,is_dropout=False,first_session_clear=False,second_session_clear=False):
        self.id = id
        self.name = name
        self.academy_id=academy_id
        self.fee_paid = fee
        self.is_dropout=is_dropout
        self.first_session_clear = first_session_clear
        self.second_session_clear = second_session_clear
        
        return self
    
    @staticmethod
    def get_student(id):
        student = session.query(Student).filter_by(id=id).first()
        return student
        
    @staticmethod
    def get_student_last_id():
        student=session.query(Student).order_by(Student.id.desc()).first()
        return student.id
    
    @classmethod
    def add_student(cls,name,academy_id,fee_paid=0):
        id=cls.get_student_last_id()+1
        # student=Student(id, name,academy_id,fee)
        student=cls(id, name,academy_id,fee_paid)
        session.add(student)
        session.commit()
        
        student = cls.get_student(id)
        return student
        
    @staticmethod
    def check_enrollement_status(name,academy_id):
        check_enroll=session.query(Student).filter(Student.name==name,Student.academy_id==academy_id).first()
        
        if check_enroll ==None:
            return False
        # return True
        else:
            return True
        
        
        
    
    def pay_fee(self,fee):
        updated_fee=self.update_student(fee=fee)
        return updated_fee
    
    
    
    def update_student(self, name=None, academy_id=None,fee=None,first_session_clear = None,second_session_clear = None):
        student = Student.get_student(self.id)
        if name:
            student.name = name
        if academy_id:
            student.academy_id = academy_id
        if fee:
            student.fee_paid = fee
        if first_session_clear:
            student.first_session_clear = first_session_clear
            
        if second_session_clear:
            student.second_session_clear = second_session_clear  
            
        session.commit()
                
        updated_student = Student.get_student(student.id)
        return updated_student
        
    
    def clear_first_session(self):
        return self.update_student(first_session_clear=True)
        # updated=self.update_student(first_session_clear=True)
        # return updated
        
    
    def clear_second_session(self):
        return self.update_student(second_session_clear=True)
    
    def drop_out(self):
        updated_status=self.update_student(is_dropout=True)
        return updated_status
        
    
    
    