from robyn import Robyn
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy import (
    Column, String, Integer, Boolean, BigInteger, ForeignKey, Text, UniqueConstraint, Enum, JSON, create_engine, Integer, String, DateTime, Float, Column
)
from datetime import datetime

# DB_URL = "postgresql://djgoDBmain_owner:0YvOjC7yEeHi@ep-lingering-term-a5gpgv2e.us-east-2.aws.neon.tech/djgoDBmain"
DB_URL = "postgresql+psycopg2://shubham:9504@localhost:5432/robyn_db?sslmode=require"

engine = create_engine(
    DB_URL,
    pool_size=20, max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

app = Robyn(__name__)


class Survey(Base):
    __tablename__ = 'surveys'
    
    survey_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    created_by = Column(JSON, nullable=True)  # Users who created or manage the survey
    tenant = Column(String, nullable=False)
    channel_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    responses = relationship("SurveyResponse", back_populates="survey")


class SurveyResponse(Base):
    __tablename__ = 'survey_responses'
    
    response_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    survey_id = Column(String, ForeignKey('surveys.survey_id'), nullable=False)
    survey_title = Column(String)  # Optional, for caching the title at response time
    description = Column(String)  # Optional, for caching the description at response time
    status = Column(String)
    timetaken = Column(Integer)
    total_questions = Column(Integer)
    questions_asked = Column(Integer)
    questions_answered = Column(Integer)
    response_timestamp = Column(DateTime, default=datetime.utcnow)
    timestamp = Column(DateTime, default=datetime.utcnow)
    tenant = Column(String)
    channel_id = Column(String)
    created_by = Column(JSON, nullable=True)  
    survey = relationship("Survey", back_populates="responses")
    responses = relationship("SurveyQuestionResponse", back_populates="survey_response")

class SurveyQuestionResponse(Base):
    __tablename__ = 'survey_question_responses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    response_id = Column(String, ForeignKey('survey_responses.response_id'), nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(String)  # e.g., 'mcq', 'text_field'
    text = Column(String, nullable=False)
    value = Column(String)
    sentiment = Column(Enum('positive', 'negative', 'neutral', 'no_sentiment', name="sentiment_types"), default="no_sentiment")
    next = Column(JSON, nullable=True)  
    is_required = Column(Boolean, default=True)
    
    survey_response = relationship("SurveyResponse", back_populates="responses")

Base.metadata.create_all(bind=engine)






def insert_data(data):
    # Open a new session
    session = SessionLocal()

    try:
        for survey_data in data["surveys"]:
            # Create Survey instance
            survey = Survey(
                survey_id=survey_data["survey_id"],
                title=survey_data["title"],
                description=survey_data["description"],
                created_by=survey_data["created_by"],
                tenant=survey_data["tenant"],
                channel_id=survey_data["channel_id"],
                created_at=datetime.fromisoformat(survey_data["created_at"].replace("Z", "+00:00"))
            )

            # Add Survey instance to session
            session.add(survey)

            for response_data in survey_data["responses"]:
                # Create SurveyResponse instance
                survey_response = SurveyResponse(
                    response_id=response_data["response_id"],
                    user_id=response_data["user_id"],
                    survey_id=response_data["survey_id"],
                    survey_title=response_data["survey_title"],
                    description=response_data["description"],
                    status=response_data["status"],
                    timetaken=response_data["timetaken"],
                    total_questions=response_data["total_questions"],
                    questions_asked=response_data["questions_asked"],
                    questions_answered=response_data["questions_answered"],
                    response_timestamp=datetime.fromisoformat(response_data["response_timestamp"].replace("Z", "+00:00")),
                    timestamp=datetime.fromisoformat(response_data["timestamp"].replace("Z", "+00:00")),
                    tenant=response_data["tenant"],
                    channel_id=response_data["channel_id"],
                    created_by=response_data["created_by"]
                )

                # Add SurveyResponse instance to session
                session.add(survey_response)

                for question_response_data in response_data["responses"]:
                    # Create SurveyQuestionResponse instance
                    question_response = SurveyQuestionResponse(
                        response_id=response_data["response_id"],
                        question_id=question_response_data["question_id"],
                        type=question_response_data["type"],
                        text=question_response_data["text"],
                        value=question_response_data["value"],
                        sentiment=question_response_data["sentiment"],
                        next=question_response_data["next"],
                        is_required=question_response_data["is_required"]
                    )

                    # Add SurveyQuestionResponse instance to session
                    session.add(question_response)

        # Commit all records to the database
        session.commit()
        print("Data inserted successfully.")
    except Exception as e:
        session.rollback()
        print("An error occurred:", e)
    finally:
        session.close()