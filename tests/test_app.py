from server import loadClubs, loadCompetitions


def test_loadClubs(load_clubs_fixture):
    assert loadClubs() == load_clubs_fixture["clubs"]


def test_loadCompetitions(load_competitions_fixture):
    assert loadCompetitions() == load_competitions_fixture["competitions"]


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


#ERROR 01: Entering a unknown email crashes the app
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