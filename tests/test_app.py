from server import loadClubs, loadCompetitions


def test_loadClubs(load_clubs_fixture):
    assert loadClubs() == load_clubs_fixture["clubs"]


def test_loadCompetitions(load_competitions_fixture):
    assert loadCompetitions() == load_competitions_fixture["competitions"]


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


#ERROR: Entering a unknown email crashes the app #01
def test_login(client):

    response = client.post(
        "/showSummary",
        data={"email": "admin@irontemple.com"}, follow_redirects=True
    )
    assert response.status_code == 200
    data = response.data.decode()

    assert "Logout" in data

def test_not_login(client):

    response = client.post(
        "/showSummary",
        data={"email": "test@irontemple.com"}, follow_redirects=True
    )
    assert response.status_code == 200
    data = response.data.decode()

    assert "Email not found" in data

#BUG: Clubs should not be able to use more than their points allowed #02
def test_purchasePlacesMore(client, load_clubs_fixture, load_competitions_fixture):
    response = client.post(
        "/showSummary",
        data={"email": "admin@irontemple.com"}, follow_redirects=True
    )
    assert response.status_code == 200
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": load_competitions_fixture["competitions"][1]["name"],
            "club": load_clubs_fixture["clubs"][1]["name"],
            "places": 5,
        },
    )
    data = response.data.decode()
    assert "You don t have enough points" in data

def test_purchasePlaces(client, load_clubs_fixture, load_competitions_fixture):
    response = client.post(
        "/showSummary",
        data={"email": "admin@irontemple.com"}, follow_redirects=True
    )
    assert response.status_code == 200

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": load_competitions_fixture["competitions"][1]["name"],
            "club": load_clubs_fixture["clubs"][1]["name"],
            "places": 2,
        },
    )
    data = response.data.decode()

    assert "Points available: 2" in data