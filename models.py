from datetime import date
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Student(Base):
    __tablename__ = "students"

    student_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    email: Mapped[str]
    birth_date: Mapped[date | None] = mapped_column("born_on")
    enrollment_date: Mapped[date] = mapped_column(
        "joined_on", server_default=func.current_date()
    )


class Course(Base):
    __tablename__ = "courses"

    course_id: Mapped[int] = mapped_column(primary_key=True)
    course_name: Mapped[str]
    instructor_name: Mapped[str] = mapped_column("professor_name")
    credits: Mapped[int]


class Grade(Base):
    __tablename__ = "grades"

    grade_id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.student_id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.course_id"))
    grade: Mapped[Decimal] = mapped_column(Numeric(5, 2))