import pytest

from app import create_app
from models import db

@pytest.fixture
def app(tmp_path):
    database_file = tmp_path / "booknest-test.sq;ite"
    test_uri = f"sqlite:///{database_file.as_posix()}"

    assert "sqlite" in test_uri

    app = create_app(
        testing=True,
        test_db_uri=test_uri,
    )

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()