from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class StudentCreate(BaseModel):
    full_name: str
    email: EmailStr
    birth_date: date | None = None

class StudentUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    birth_date: date | None = None

class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    student_id: int
    full_name: str
    email: EmailStr
    birth_date: date | None
    enrollment_date: date

class CourseCreate(BaseModel):
    course_name: str
    instructor_name: str
    credits: int = Field(gt=0)

class CourseUpdate(BaseModel):
    course_name: str | None = None
    instructor_name: str | None = None
    credits: int | None = Field(default=None,gt=0)

class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    course_id: int
    course_name: str
    instructor_name: str
    credits: int

class GradeCreate(BaseModel):
    student_id: int
    course_id: int
    grade: float = Field(ge=0, le=100)

class GradeUpdate(BaseModel):
    grade: float | None = Field(ge=0, le=100)

class GradeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    grade_id: int
    student_id: int
    course_id: int
    grade: float

class StudentAverage(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    student_id: int
    full_name: str
    average_grade: float 
    courses_taken: int

class CourseAverage(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    course_id: int
    course_name: str
    average_grade: float 
    students_graded: int

   