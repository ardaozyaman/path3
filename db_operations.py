from sqlalchemy.orm import Session
from models import TestResult
from database import SessionLocal
from datetime import datetime

def insert_test_result(test_name: str, status: str, duration: float):
    """
    Inserts a test result into the database.

    Args:
        test_name (str): The name of the test method.
        status (str): The result of the test ('pass' or 'fail').
        duration (float): The execution time of the test in seconds.
    """
    db: Session = SessionLocal()
    try:
        test_result = TestResult(
            
            test_name=test_name,
            status=status,
            duration=duration,
            timestamp=datetime.utcnow()
        )
        db.add(test_result)
        db.commit()
    finally:
        db.close()
