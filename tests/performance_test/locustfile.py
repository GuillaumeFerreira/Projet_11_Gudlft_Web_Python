from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get("/")
    @task
    def login(self):
        self.client.post(
            "/showSummary",
            data={"email": "admin@irontemple.com"},
        )

    @task
    def logout(self):
        self.client.post(
                "/showSummary",
                data={"email": "admin@irontemple.com"}
            )

        self.client.get('/logout')

    @task
    def purchasePlaces(self):
        self.client.post(
            "/showSummary",
            data={"email": "admin@irontemple.com"}
        )
        self.client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": 2,
            },
        )

    @task
    def book(self):
        self.client.post(
            "/showSummary",
            data={"email": "admin@irontemple.com"}
        )
        self.client.get(
            "/book/"
            + "Spring Festival"
            + "/"
            + "Simply Lift"
        )
