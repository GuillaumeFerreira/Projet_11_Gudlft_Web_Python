import json
import datetime
from flask import Flask, render_template, request, redirect, flash, url_for, session


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def create_app(config={}):
    app = Flask(__name__)
    app.config.from_object(config)

    app.config.update(config)
    app.secret_key = "something_special"

    competitions = loadCompetitions()
    clubs = loadClubs()

    @app.route("/")
    def index():
        return render_template("index.html", clubs=clubs)

    @app.route("/showSummary", methods=["POST"])
    def showSummary():
        if request.method == 'POST':
            session['email'] = request.form['email']
            # Issue 01 : ERROR entering a unknown email crashes the app
            try:
                club = [club for club in clubs if club["email"] == session['email']][0]
                return render_template(
                    "welcome.html", club=club, competitions=competitions, clubs=clubs
                )
            except:
                flash("Email not found")
                return render_template("index.html", clubs=clubs)

    @app.route("/book/<competition>/<club>")
    def book(competition, club):
        if 'email' in session:
            foundClub = [c for c in clubs if c["name"] == club][0]
            foundCompetition = [c for c in competitions if c["name"] == competition][0]
            competitionDate = datetime.datetime.strptime(foundCompetition['date'],
                                                         '%Y-%m-%d %H:%M:%S')

            if competitionDate > datetime.datetime.now():
                if (foundClub and foundCompetition):
                    flash("Valid competition")
                    return render_template(
                        "booking.html",
                        club=foundClub,
                        competition=foundCompetition,
                        clubs=clubs,
                    )
            else:
                flash("This competition is closed.")

                return render_template(
                    "welcome.html", club=foundClub, competitions=competitions, clubs=clubs
                )
        else:
            flash("Please log in")
            return render_template("index.html", clubs=clubs)

    @app.route("/purchasePlaces", methods=["POST"])
    def purchasePlaces():
        if 'email' in session:
            competition = [
                c for c in competitions if c["name"] == request.form["competition"]
            ][0]
            club = [c for c in clubs if c["name"] == request.form["club"]][0]
            placesRequired = int(request.form["places"])

            if (
                placesRequired <= 12
                and placesRequired >= 0
                and int(club["points"]) > placesRequired
            ):
                if int(club["points"]) < placesRequired*3:
                    flash("You don t have enough points")
                    return render_template(
                        "booking.html",
                        club=club,
                        competitions=competitions,
                        clubs=clubs,
                        competition=competition,
                    )
                else:
                    # Issue 6 : Point updates are not reflected
                    competition["numberOfPlaces"] = (
                        int(competition["numberOfPlaces"]) - placesRequired
                    )
                    club["points"] = int(club["points"]) - (placesRequired*3)
                    flash("Great-booking complete!")
                    return render_template(
                        "welcome.html", club=club, competitions=competitions, clubs=clubs,date=str(datetime.datetime.now())
                    )
            elif placesRequired > 12:

                flash("You cannot buy more than twelve places, try again")
                return render_template(
                    "booking.html",
                    club=club,
                    competitions=competitions,
                    clubs=clubs,
                    competition=competition,
                )
            else:

                flash("Something went wrong-please try again")
                return render_template(
                    "booking.html",
                    club=club,
                    competitions=competitions,
                    clubs=clubs,
                    competition=competition,
                )
        else:
            flash("Please log in")
            return render_template("index.html", clubs=clubs)
    # TODO: Add route for points display

    @app.route("/logout")
    def logout():
        session.pop('email', None)
        return redirect(url_for("index"))

    return app
