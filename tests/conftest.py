import pytest
from server import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def load_clubs_fixture():
    clubs = {
        "clubs": [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
        ]
    }
    return clubs


@pytest.fixture
def load_competitions_fixture():
    competitions = {
        "competitions": [
            {
                "name": "Spring Festival",
                "date": "2022-03-27 10:00:00",
                "numberOfPlaces": "25",
            },
            {
                "name": "Fall Classic",
                "date": "2022-10-22 13:30:00",
                "numberOfPlaces": "13",
            },
        ]
    }
    return competitions