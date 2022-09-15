#FEATURE: Implement Points Display Board #7
def test_showClub_showSummary(client, load_clubs_fixture):
    response = client.post(
        "/showSummary",
        data={"email": "admin@irontemple.com"},
    )
    data = response.data.decode()
    for club in load_clubs_fixture["clubs"]:
        assert club["points"] in data and club["name"] in data and "Logout" in data