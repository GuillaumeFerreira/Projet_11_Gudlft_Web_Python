def test_logout(client):
    response = client.post(
        "/showSummary",
        data={"email": "admin@irontemple.com"}, follow_redirects=True
    )
    assert response.status_code == 200
    response = client.get('/logout', follow_redirects=True)
    data = response.data.decode()
    assert "Logout" not in data