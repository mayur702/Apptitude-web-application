# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import FastAPI, Depends, HTTPException, status
# from sqlalchemy import Column, Integer, String, Enum, create_engine, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session, relationship
# from pydantic import BaseModel, EmailStr, constr
# from passlib.context import CryptContext
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# from typing import Optional
# import enum

# # Database Setup
# DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # Password Hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # JWT Configuration
# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # Role Enum
# class Role(str, enum.Enum):
#     admin = "admin"
#     student = "student"

# # User Model
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     mobile_no = Column(String, unique=True, nullable=False)
#     email = Column(String, unique=True, index=True, nullable=False)
#     role = Column(Enum(Role), nullable=False)
#     hashed_password = Column(String, nullable=False)

# # Question Model
# class Question(Base):
#     __tablename__ = "questions"
#     id = Column(Integer, primary_key=True, index=True)
#     question_text = Column(String, nullable=False)
#     option_a = Column(String, nullable=False)
#     option_b = Column(String, nullable=False)
#     option_c = Column(String, nullable=False)
#     option_d = Column(String, nullable=False)
#     correct_option = Column(String, nullable=False)
#     created_by = Column(Integer, ForeignKey("users.id"))
#     creator = relationship("User")

# Base.metadata.create_all(bind=engine)

# # Pydantic Schemas
# class UserCreate(BaseModel):
#     name: str
#     mobile_no: constr(min_length=10, max_length=10)
#     email: EmailStr
#     role: Role
#     password: str
#     confirm_password: str

# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class QuestionCreate(BaseModel):
#     question_text: str
#     option_a: str
#     option_b: str
#     option_c: str
#     option_d: str
#     correct_option: str

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Create FastAPI app




# app = FastAPI()

# # CORS Middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins (Change this in production)
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # Helper Functions
# def get_password_hash(password: str):
#     return pwd_context.hash(password)

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# from fastapi.security import OAuth2PasswordBearer

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = db.query(User).filter(User.email == email).first()
#     if user is None:
#         raise credentials_exception
#     return user


# # User Registration Endpoint
# @app.post("/register/")
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     if user.password != user.confirm_password:
#         raise HTTPException(status_code=400, detail="Passwords do not match")
    
#     hashed_password = get_password_hash(user.password)
#     db_user = User(name=user.name, mobile_no=user.mobile_no, email=user.email, role=user.role, hashed_password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
    
#     return {"message": "User registered successfully"}

# # User Login Endpoint
# @app.post("/login/", response_model=Token)
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.email == user.email).first()
#     if not db_user or not verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
#     access_token = create_access_token(data={"sub": db_user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# # Admin-only Question Upload Endpoint
# @app.post("/questions/")
# def create_question(question: QuestionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     if current_user.role != Role.admin:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can upload questions")
    
#     db_question = Question(
#         question_text=question.question_text,
#         option_a=question.option_a,
#         option_b=question.option_b,
#         option_c=question.option_c,
#         option_d=question.option_d,
#         correct_option=question.correct_option,
#         created_by=current_user.id
#     )
#     db.add(db_question)
#     db.commit()
#     db.refresh(db_question)
    
#     return {"message": "Question uploaded successfully"}

# # Run the app with:
# # uvicorn filename:app --reload




from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import Column, Integer, String, Enum, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, EmailStr, constr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List
import enum
import random

# Database Setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 59

# Role Enum
class Role(str, enum.Enum):
    admin = "admin"
    student = "student"

# User Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    mobile_no = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(Enum(Role), nullable=False)
    hashed_password = Column(String, nullable=False)

# Question Model
class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_option = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User")

# Exam Response Model
class ExamResponse(Base):
    __tablename__ = "exam_responses"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer = Column(String, nullable=False)
    
    student = relationship("User")
    question = relationship("Question")

Base.metadata.create_all(bind=engine)

# Pydantic Schemas
class UserCreate(BaseModel):
    name: str
    mobile_no: constr(min_length=10, max_length=10)
    email: EmailStr
    role: Role
    password: str
    confirm_password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class QuestionCreate(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str

class ExamAnswer(BaseModel):
    question_id: int
    answer: str

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create FastAPI app
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Change this in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper Functions
def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# User Registration Endpoint
@app.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(name=user.name, mobile_no=user.mobile_no, email=user.email, role=user.role, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "User registered successfully"}

# User Login Endpoint
@app.post("/login/", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Admin-only Question Upload Endpoint
@app.post("/questions/")
def create_question(question: QuestionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != Role.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can upload questions")
    
    db_question = Question(
        question_text=question.question_text,
        option_a=question.option_a,
        option_b=question.option_b,
        option_c=question.option_c,
        option_d=question.option_d,
        correct_option=question.correct_option,
        created_by=current_user.id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    return {"message": "Question uploaded successfully"}

# Endpoint to get 20 random questions for the exam
@app.get("/exam/questions/")
def get_exam_questions(db: Session = Depends(get_db)):
    # Fetch all questions
    questions = db.query(Question).all()
    
    # Randomly pick 20 questions (or fewer if there are less than 20)
    selected_questions = random.sample(questions, min(20, len(questions)))
    
    return selected_questions

# Endpoint to submit answers for the exam
@app.post("/exam/submit/")
def submit_exam_answers(answers: List[ExamAnswer], current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    for answer in answers:
        # Create and save the exam response for each question
        exam_response = ExamResponse(
            student_id=current_user.id,
            question_id=answer.question_id,
            answer=answer.answer
        )
        db.add(exam_response)
    
    db.commit()
    return {"message": "Your exam responses have been submitted successfully!"}

# Endpoint to grade the exam
@app.get("/exam/grade/")
def grade_exam(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get all exam responses for the current student
    exam_responses = db.query(ExamResponse).filter(ExamResponse.student_id == current_user.id).all()
    
    score = 0
    total_questions = len(exam_responses)
    
    for response in exam_responses:
        # Get the correct answer from the question
        question = db.query(Question).filter(Question.id == response.question_id).first()
        
        if question.correct_option == response.answer:
            score += 1
    
    
    return {"score": score, "total_questions": total_questions}

# Run the app with:
# uvicorn filename:app --reload
