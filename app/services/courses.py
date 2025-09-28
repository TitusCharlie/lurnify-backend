from sqlmodel import Session, select
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from typing import Optional, List
import slugify

def create_course(data: CourseCreate, author_id: str, db: Session) -> Course:
    course_dict = data.model_dump()
    
    # Generate slug from the title
    if "title" in course_dict:
        course_dict["slug"] = slugify.slugify(course_dict["title"])   
    
    course = Course(**course_dict, author_id=author_id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

def publish_course(course_id: str, current_user_id: str, db: Session) -> Optional[Course]:
    course = db.get(Course, course_id)
    if not course or course.author_id != current_user_id:
        return None
    course.is_published = True
    db.commit()
    db.refresh(course)
    return course

def get_course(course_id: str, db: Session) -> Optional[Course]:
    return db.get(Course, course_id)

def list_courses(db: Session, creator_id: str = None, only_published: bool = True) -> List[Course]:
    query = select(Course)
    
    if only_published:
        query = query.where(Course.is_published == True)
    
    if creator_id:
        # creator can see all (ignore published filter if they own it)
        query = select(Course).where(Course.creator_id == creator_id)
    
    return db.exec(query).all()

def update_course(course_id: str, data: CourseUpdate, current_user_id: str, db: Session) -> Optional[Course]:
    course = db.get(Course, course_id)
    if not course or course.author_id != current_user_id:
        return False


    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(course, key, value)

    db.add(course)
    db.commit()
    db.refresh(course)
    return course

def delete_course(course_id: str, current_user_id: str, db: Session) -> bool:
    course = db.get(Course, course_id)
    if not course or course.author_id != current_user_id:
        return False


    db.delete(course)
    db.commit()
    return True