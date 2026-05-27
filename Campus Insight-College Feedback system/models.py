from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from database import Base

class Feedback(Base):

    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    usn = Column(String)

    department = Column(String)

    year = Column(String)

    feedback_type = Column(String)

    teacher_name = Column(String)

    subject = Column(String)

    rating1 = Column(Float)

    rating2 = Column(Float)

    rating3 = Column(Float)

    rating4 = Column(Float)

    rating5 = Column(Float)

    overall_rating = Column(Float)

    feedback_text = Column(String)

    sentiment = Column(String)