import pytest
from sqlalchemy.orm import Session

from ...scrapers.course import Course
from ...scrapers.course_class import CourseClass

from .. import crud, models
from ..sql import SessionLocal, engine


class University:
    def __init__(self, name):
        self.name = name


university = University("test1")
term_id = "2020-FALL-1"

course = Course()
course.course_id = "test 101"
course.title = "intro to course"
course.department = "test"
course.units = 4
course.school = "School of Test"
course.department_title = "Test ing"

a_class = CourseClass(course)
a_class.class_id = "123456"
a_class.instructor = "Dr. Test"
a_class.time = "time is an illusion"
a_class.location = "Testing Hall 200"
a_class.building = "Testing Hall"
a_class.room = "200"
a_class.status = "OPEN"
a_class.units = 4
a_class.final = "never"
a_class.enrolled = 100


@pytest.fixture(scope="module")
def db():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    models.Base.metadata.drop_all(bind=engine)


def test_add_university(db):
    crud.add_university(db, **university.__dict__)
    universityRow = crud.get_university(db, university.name)
    assert universityRow != None


def test_add_course(db):
    crud.add_course(db, university.name, term_id, course)
    # print(crud.CourseQuery(db, university.name, dict()).search()[0])
    # courseRow = crud.get_university(db, university.name.upper()).courses.filter(models.Course.__table__.c["id"].in_([course.id])).all()
    assert (
        len(
            crud.CourseQuery(
                db,
                university.name,
                {
                    "course_id[equals]": course.course_id,
                    "course_id[not]": course.course_id + "a",
                    "title[like]": course.title.upper(),
                    "school[notlike]": "exam",
                },
            ).search()
        )
        > 0
    )


def test_add_class(db):
    crud.add_class(db, university.name, term_id, a_class)
    # print(crud.ClassQuery(db, university.name, dict()).search()[0])
    assert (
        len(
            crud.ClassQuery(
                db,
                university.name,
                {
                    "class_id[equals]": a_class.class_id,
                    "class_id[not]": a_class.class_id + "a",
                    "instructor[like]": a_class.instructor.upper(),
                    "building[notlike]": "exam",
                },
            ).search()
        )
        > 0
    )


def test_add_many_course_and_class(db):
    """
    Load testing for adding a course
    """
    temp_course_id = course.course_id
    temp_class_id = a_class.class_id
    limit = 90
    classes_per_course = 10
    courses = list()
    new_classes = list()
    new_term_id = "2021-WINTER-1"

    # create courses and classes and insert courses
    for i in range(limit):
        new_course = Course(course.__dict__)
        new_course.course_id = temp_course_id + str(i)

        for j in range(classes_per_course):
            new_class = CourseClass(course, a_class.__dict__)
            new_class.class_id = temp_class_id + str(i) + str(j)
            new_course.classes.append(new_class)
        courses.append(new_course)

        crud.add_course(db, university.name, new_term_id, new_course, commit=False)

    db.commit()

    # extract classes from courses for bulk db insertion
    for a_course in courses:
        new_classes.extend(a_course.classes)

    # insert classes
    for a_course_class in new_classes:
        crud.add_class(db, university.name, new_term_id, a_course_class, commit=False)
    db.commit()

    added_courses = crud.CourseQuery(
        db, university.name, term_id=new_term_id, limit=limit
    ).search()
    assert len(added_courses) == limit

    added_classes = crud.ClassQuery(
        db, university.name, term_id=new_term_id, limit=limit * classes_per_course
    ).search()
    assert len(added_classes) == limit * classes_per_course


def test_bulk_add_courses(db):
    """
    tests crud.bulk_add_course(db: Session)
    """
    temp_id = course.course_id
    limit = 900
    course_list = list()
    new_term_id = "2021-SPRING-1"

    for i in range(limit):
        new_course = Course(course.__dict__)
        new_course.course_id = str(i) + temp_id
        course_list.append(new_course)

    crud.bulk_add_courses(db, university.name, new_term_id, course_list)
    courses = crud.CourseQuery(
        db, university.name, term_id="2021-SPRING", limit=limit
    ).search()

    assert len(courses) == limit


def test_bulk_merge_courses_and_classes(db):
    """
    Load testing for adding a course
    """
    temp_course_id = course.course_id
    temp_class_id = a_class.class_id
    limit = 500
    classes_per_course = 5
    course_list = list()
    class_list = list()
    new_term_id = "2021-SUMMER-2"

    # create courses and classes and insert courses
    for i in range(limit):
        new_course = Course(course.__dict__)
        new_course.course_id = temp_course_id + str(i)

        for j in range(classes_per_course):
            new_class = CourseClass(course, a_class.__dict__)
            new_class.class_id = temp_class_id + str(i) + str(j)
            new_course.classes.append(new_class)
        course_list.append(new_course)

    # extract classes from courses for bulk db insertion
    for a_course in course_list:
        class_list.extend(a_course.classes)

    crud.bulk_merge_courses(db, university.name, new_term_id, course_list)
    courses = crud.CourseQuery(
        db, university.name, term_id=new_term_id, limit=limit
    ).search()
    crud.bulk_merge_classes(db, university.name, new_term_id, class_list)
    assert len(courses) == limit

    added_classes = crud.ClassQuery(
        db, university.name, term_id=new_term_id, limit=limit * classes_per_course
    ).search()
    assert len(added_classes) == limit * classes_per_course
