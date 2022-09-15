

def test_login_route(client,load_clubs_fixture,load_competitions_fixture):

    # On connecter un utilisateur
    response = client.post(
        "/showSummary",
        data={"email": load_clubs_fixture["clubs"][2]["email"]}, follow_redirects=True
    )
    assert response.status_code == 200

    #On reserve 2 places
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

    # On se déconnecte
    response = client.get('/logout', follow_redirects=True)
    data = response.data.decode()
    assert "Logout" not in data

    #On visualise l index avec les clubs et leurs points
    response = client.get("/")
    assert response.status_code == 200
    for club in load_clubs_fixture["clubs"]:
        if club["name"] == load_clubs_fixture["clubs"][2]["name"]:
           points = str(int(club["points"]) - 2*3)
           assert points in data and club["name"] in data and "Logout" not in data
        else:
            assert  club["points"] in data and club["name"] in data and "Logout" not in data