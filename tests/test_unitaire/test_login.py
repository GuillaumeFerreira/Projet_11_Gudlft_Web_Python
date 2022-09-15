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