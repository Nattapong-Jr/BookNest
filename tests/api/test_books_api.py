from decimal import Decimal
from models import db
from models.book import Book
from models.user import User

def test_get_books_require_login(client):
    ressponse = client.get("/api/get_books")

    assert ressponse.status_code == 401
    assert ressponse.get_json() == {
        "error": "Please login first"
    }

def test_get_books_when_logged_in_and_database_empty(client):
    with client.session_transaction() as session:
        session["user_id"] = 1

    response = client.get("/api/get_books")

    assert response.status_code == 200
    assert response.get_json() == []

def test_get_books_returns_books(app, client):
    with app.app_context():
        book = Book(
            title="Test Book",
            author="Test Author",
            price=Decimal("199.00"),
            stock_quantity=5,
            image_path=None,
        )
        db.session.add(book)
        db.session.commit()

    with client.session_transaction() as session:
        session["user_id"] = 1

    response = client.get("/api/get_books")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Test Book"
    assert data[0]["author"] == "Test Author"
    assert data[0]["price"] == "199.00"
    assert data[0]["stock_quantity"] == 5
    assert data[0]["image_path"] == "assets/if_book_error.png"

def test_login_then_get_books(app, client):
    with app.app_context():
        user = User(
            name="Tester",
            email="tester@example.com",
            password_hash="1234",
            role="user",
        )
        db.session.add(user)
        db.session.commit()

    login_response = client.post(
        "/login",
        data={
            "email": "tester@example.com",
            "password": "1234",
        },
    )

    assert login_response.status_code == 302

    books_response = client.get("/api/get_books")

    assert books_response.status_code == 200