from fastapi import Depends, FastAPI, HTTPException, Query, Response
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import Course, Grade, Student
from schemas import (
    StudentCreate,StudentOut,StudentUpdate, StudentAverage,
    CourseCreate,CourseOut,CourseUpdate, CourseAverage,
    GradeCreate,GradeOut,GradeUpdate,
)

app = FastAPI(title="Grades API")


@app.post("/students", response_model=StudentOut, status_code=201)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    if db.query(Student).filter(Student.email == payload.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")
    student = Student(**payload.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@app.get("/students", response_model=list[StudentOut])
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Student)
    if name:
        query = query.filter(Student.full_name.ilike(f"%{name}%"))
    return query.order_by(Student.student_id).offset(skip).limit(limit).all()


@app.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.patch("/students/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)
):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    data = payload.model_dump(exclude_unset=True)

    if "email" in data:
        taken = (
            db.query(Student)
            .filter(Student.email == data["email"], Student.student_id != student_id)
            .first()
        )
        if taken:
            raise HTTPException(status_code=409, detail="Email already exists")
    for key, value in data.items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student


@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.query(Grade).filter(Grade.student_id == student_id).delete()
    db.delete(student)
    db.commit()
    return Response(status_code=204)


@app.post("/courses", response_model=CourseOut, status_code=201)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    course = Course(**payload.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@app.get("/courses/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.get("/courses", response_model=list[CourseOut])
def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return db.query(Course).order_by(Course.course_id).offset(skip).limit(limit).all()


@app.patch("/courses/{course_id}", response_model=CourseOut)
def update_course(course_id: int, payload: CourseUpdate, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course


@app.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    if db.query(Grade).filter(Grade.course_id == course_id).first():
        raise HTTPException(
            status_code=409, detail="Course has grades; delete them first"
        )
    db.delete(course)
    db.commit()
    return Response(status_code=204)

@app.post("/grades", response_model=GradeOut, status_code=201)
def create_grade(payload: GradeCreate, db: Session = Depends(get_db)):
    if db.get(Student, payload.student_id) is None:
        raise HTTPException(status_code=400, detail="Student does not exist")
    if db.get(Course, payload.course_id) is None:
         raise HTTPException(status_code=400, detail="Course does not exist")
    duplicate = (
        db.query(Grade)
        .filter(
            Grade.student_id == payload.student_id, Grade.course_id == payload.course_id
        ).first()
    )
    if duplicate:
         raise HTTPException(
               status_code=409, detail="Grade for this student and course already exists"
         )
    grade = Grade(**payload.model_dump())
    db.add(grade)
    db.commit()
    db.refresh(grade)
    return grade

@app.get("/students/{student_id}/grades", response_model=list[GradeOut])
def list_student_grades(student_id: int, db: Session = Depends(get_db)):
    if db.get(Student, student_id) is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return (
        db.query(Grade)
        .filter(Grade.student_id == student_id)
        .order_by(Grade.course_id)
        .all()
    )

@app.patch("/grades/{grade_id}", response_model=GradeOut)
def update_grade(grade_id: int, payload: GradeUpdate, db: Session = Depends(get_db)):
    row = db.get(Grade, grade_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Grade not found")
    row.grade = payload.grade
    db.commit()
    db.refresh(row)
    return row

@app.delete("/grades/{grade_id}", status_code=204)
def delete_grade(grade_id: int, db : Session = Depends(get_db)):
    row = db.get(Grade, grade_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Grade not found")
    db.delete(row)
    db.commit()
    return Response(status_code=204)

@app.get("/reports/student-averages", response_model=list[StudentAverage])
def student_averages(db: Session = Depends(get_db)):
    return (
        db.query(
            Student.student_id,
            Student.full_name,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
            func.count(Grade.grade_id).label("courses_taken"),
        )
        .join(Grade, Grade.student_id == Student.student_id)
        .group_by(Student.student_id, Student.full_name)
        .order_by(Student.student_id)
        .all()
    )

@app.get("/reports/course-averages", response_model=list[CourseAverage])
def course_averages(db: Session = Depends(get_db)):
    return (
        db.query(
            Course.course_id,
            Course.course_name,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
            func.count(Grade.grade_id).label("students_graded"),
        )
        .join(Grade, Grade.course_id == Course.course_id)
        .group_by(Course.course_id, Course.course_name)
        .order_by(Course.course_id)
        .all()
    )