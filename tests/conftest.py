import os

import pytest

from app import create_app
from app.models import Role, User
from app.services import db


@pytest.fixture
def app():
    """Create and configure a new app instance for each test and create test database."""
    app = create_app(config='config.TestConfig')
    with app.app_context():
        db.create_all()
    yield app


@pytest.fixture
def admin(app) -> User:
    """Creates an admin user for testing."""
    with app.app_context():
        admin_role = Role.create(name='admin')
        admin = User.create(role=admin_role, email='creatixdevelopers@gmail.com', password='password')
        yield admin


@pytest.fixture
def user(app) -> User:
    """Creates a user for testing."""
    with app.app_context():
        user_role = Role.create(name='user')
        user = User.create(role=user_role, email='user@creatix.com', password='password')
        yield user


@pytest.fixture
def utils():
    """Defines utility methods that can be used in any test."""

    class Utils:
        @staticmethod
        def getCookies(client) -> dict:
            """Returns a dictionary of cookie names and values for the given client."""
            return {cookie.name: cookie.value for cookie in client.cookie_jar}

        @staticmethod
        def add_mock_data():
            """Adds mock data to the test database."""
            admin_role = Role.create(name='admin')
            user_role = Role.create(name='user')
            User.create(role=admin_role, email='creatixdevelopers@gmail.com', password='password')
            User.create(role=user_role, email='test@test.com', password='password')
            User.create(role=user_role, email='test2@test.com', password='password')
            return True

    return Utils()


@pytest.fixture(autouse=True)
def clear_database(app):
    """Clears database after each test case."""
    yield
    with app.app_context():
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()


def pytest_sessionfinish(session, exitstatus):
    """Removes the test database after all tests have finished executing."""
    test_database = os.path.join(os.path.dirname(__file__), 'test.db')
    if os.path.exists(test_database):
        os.remove(test_database)
