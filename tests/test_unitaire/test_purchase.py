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
            "places": 3,
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
            "club": load_clubs_fixture["clubs"][2]["name"],
            "places": 2,
        },
    )
    data = response.data.decode()

    assert "Points available: 6" in data

#BUG: Clubs shouldn't be able to book more than 12 places per competition #4
def test_purchasePlacesTwelve(client, load_clubs_fixture, load_competitions_fixture):
    response = client.post(
        "/showSummary",
        data={"email": "admin@irontemple.com"}, follow_redirects=True
    )
    assert response.status_code == 200
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": load_competitions_fixture["competitions"][0]["name"],
            "club": load_clubs_fixture["clubs"][0]["name"],
            "places": 13,
        },
    )
    data = response.data.decode()

    assert "You cannot buy more than twelve places" in data

def test_purchasePlacesCompetition(client, load_clubs_fixture, load_competitions_fixture):
    response = client.post(
        "/showSummary",
        data={"email": "admin@irontemple.com"}, follow_redirects=True
    )
    assert response.status_code == 200
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": load_competitions_fixture["competitions"][0]["name"],
            "club": load_clubs_fixture["clubs"][0]["name"],
            "places": 4,
        },
    )
    data = response.data.decode()

    assert "Number of Places: 21" in data

#BUG: Booking places in past competitions #5
def test_purchaseDate_valid(client, load_clubs_fixture, load_competitions_fixture):
    response = client.post(
        "/showSummary",
        data={"email": "admin@irontemple.com"}, follow_redirects=True
    )
    assert response.status_code == 200
    response = client.get(
        "/book/"
        + load_competitions_fixture["competitions"][1]["name"]
        + "/"
        + load_clubs_fixture["clubs"][1]["name"]
    )
    data = response.data.decode()
    assert "Valid competition" in data

def test_purchaseDate_not_valid(client, load_clubs_fixture, load_competitions_fixture):
    response = client.post(
        "/showSummary",
        data={"email": "admin@irontemple.com"}, follow_redirects=True
    )
    assert response.status_code == 200
    response = client.get(
        "/book/"
        + load_competitions_fixture["competitions"][0]["name"]
        + "/"
        + load_clubs_fixture["clubs"][1]["name"]
    )
    data = response.data.decode()
    assert "This competition is closed." in data

#BUG: Point updates are not reflected #6
def test_updates_purchasePlaces(client, load_clubs_fixture, load_competitions_fixture):
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
            "places": 1,
        },
    )
    data = response.data.decode()

    assert "Points available: 1" in data