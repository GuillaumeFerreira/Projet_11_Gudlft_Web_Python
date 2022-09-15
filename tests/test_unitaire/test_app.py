from server import loadClubs, loadCompetitions


def test_loadClubs(load_clubs_fixture):
    assert loadClubs() == load_clubs_fixture["clubs"]


def test_loadCompetitions(load_competitions_fixture):
    assert loadCompetitions() == load_competitions_fixture["competitions"]
