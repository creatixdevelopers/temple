import pytest
from sqlalchemy.exc import IntegrityError

from app.services import db
from app.models import Role, User


def test_role_model(app, client):
    with app.app_context():
        # test columns were created properly
        columns = ['id', 'uid', 'name']
        assert len(Role.columns()) == len(columns) and sorted(Role.columns()) == sorted(columns)

        # test adding role
        role = Role.create(name='Role 1')
        assert len(Role.all()) == 1
        assert role.id is not None
        assert role.name == 'Role 1'

        # test adding role with existing name
        with pytest.raises(IntegrityError) as e:
            Role.create(name='Role 1')
        db.session.rollback()
        assert "UNIQUE constraint failed" in str(e)
        assert len(Role.all()) == 1

        # test users relationship
        user_1 = User.create(role=role, email='test@test.com', password='password')
        user_2 = User.create(role=role, email='test2@test.com', password='password2')
        assert role.users == [user_1, user_2]


def test_user_model(app, client):
    with app.app_context():
        # test columns were created properly
        columns = ['id', 'uid', 'role_id', 'created', 'email', 'password_hash', 'deleted']
        assert len(User.columns()) == len(columns) and sorted(User.columns()) == sorted(columns)

        test_role = Role.create(name='Test Role')

        # test adding user
        user = User.create(role=test_role, email='test@test.com', password='password')
        assert len(User.all()) == 1
        assert user.id is not None
        assert user.role_id == test_role.id
        assert user.role.name == 'Test Role'
        assert user.email == 'test@test.com'
        assert user.password_hash is not None
        with pytest.raises(AttributeError) as e:
            _ = user.password
        db.session.rollback()
        assert ("Password is not a readable attribute." in str(e))

        # test adding user with existing email
        with pytest.raises(IntegrityError) as e:
            User.create(role=test_role, email='test@test.com', password='password2')
        db.session.rollback()
        assert ("UNIQUE constraint failed" in str(e))
        assert (len(User.all()) == 1)
