import unittest
import time
import sys
from models import init_db
from db_operations import insert_test_result

class DatabaseTestResult(unittest.TextTestResult):
    def startTest(self, test):
        super().startTest(test)
        self.start_time = time.time()

    def addSuccess(self, test):
        super().addSuccess(test)
        duration = time.time() - self.start_time
        insert_test_result(test.id(), 'pass', duration)
        print(f"PASS: {test.id()} ({duration:.4f}s)")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        duration = time.time() - self.start_time
        insert_test_result(test.id(), 'fail', duration)
        print(f"FAIL: {test.id()} ({duration:.4f}s)")

    def addError(self, test, err):
        super().addError(test, err)
        duration = time.time() - self.start_time
        # Errors are also considered failures in test outcomes
        insert_test_result(test.id(), 'fail', duration)
        print(f"ERROR: {test.id()} ({duration:.4f}s)")

class DatabaseTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, resultclass=DatabaseTestResult, **kwargs)

def run_tests():
    """
    Discovers and runs all tests, recording results to the database.
    """
    # Initialize the database and create tables if they don't exist
    print("Initializing database...")
    init_db()
    print("Database initialized.")

    # Discover and run tests
    print("Discovering tests...")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='.', pattern='test_*.py')
    
    if suite.countTestCases() == 0:
        print("No tests found.")
        return True

    print(f"Found {suite.countTestCases()} tests.")
    
    runner = DatabaseTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return True if the test run was successful, False otherwise
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    # Exit with a status code that reflects the test outcome
    # This is important for CI/CD systems like Jenkins
    sys.exit(0 if success else 1)
