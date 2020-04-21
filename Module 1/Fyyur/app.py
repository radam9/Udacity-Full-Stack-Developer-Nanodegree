# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = "Venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column("genres", db.ARRAY(db.String()), nullable=False)
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship(
        "Show", cascade="save-update, merge, delete", backref="venue", lazy=True
    )

    def __repr__(self):
        return f"<Venue {self.id} - {self.name}>"


class Artist(db.Model):
    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column("genres", db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", backref="artist", lazy=True)

    def __repr__(self):
        return f"<Artist {self.id} - {self.name}>"


class Show(db.Model):
    __tablename__ = "Show"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Show {self.id} - Artist {self.artist_id} - Venue {self.venue_id}>"


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():
    # create the data list
    data = list()
    # get all venues
    venues = Venue.query.all()
    # get unique city and states combination for each available venue
    venue_locations = set()
    for v in venues:
        venue_locations.add((v.city, v.state))
    # add cities and states to data
    for loc in venue_locations:
        data.append({"city": loc[0], "state": loc[1], "venues": []})
    # add the rest of the info to the data
    for v in venues:
        num_upcoming_shows = 0
        # get all shows in venue
        shows = Show.query.filter_by(venue_id=v.id).all()
        # increment upcoming shows
        for s in shows:
            if s.start_time > datetime.now():
                num_upcoming_shows += 1
        # add venues to data
        for d in data:
            if v.city == d["city"] and v.state == d["state"]:
                d["venues"].append(
                    {
                        "id": v.id,
                        "name": v.name,
                        "num_upcoming_shows": num_upcoming_shows,
                    }
                )

    return render_template("pages/venues.html", areas=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    # user search term
    search_term = request.form.get("search_term", "")
    # find all venues matching search term (partial and case insensitivity included)
    venues = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()
    response = {"count": len(venues), "data": []}

    for v in venues:
        num_upcoming_shows = 0
        # get all shows in venue
        shows = Show.query.filter_by(venue_id=v.id).all()
        # increment upcoming shows
        for s in shows:
            if s.start_time > datetime.now():
                num_upcoming_shows += 1
        # add venues to response
        response["data"].append(
            {"id": v.id, "name": v.name, "num_upcoming_shows": num_upcoming_shows,}
        )
    # return response with search results
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    # get venue info using venue_id
    venue = Venue.query.get(venue_id)
    # get all shows for the given venue
    shows = Show.query.filter_by(venue_id=venue_id).all()
    # get past and upcoming show info and count
    upcoming = list()
    past = list()
    for s in shows:
        artist = Artist.query.get(s.artist_id)
        artist_name = artist.name
        artist_image_link = artist.image_link
        if s.start_time > datetime.now():
            upcoming.append(
                {
                    "artist_id": s.artist_id,
                    "artist_name": artist_name,
                    "artist_image_link": artist_image_link,
                    "start_time": format_datetime(str(s.start_time)),
                }
            )
        else:
            past.append(
                {
                    "artist_id": s.artist_id,
                    "artist_name": artist_name,
                    "artist_image_link": artist_image_link,
                    "start_time": format_datetime(str(s.start_time)),
                }
            )
    # add show data to venue
    venue.past_shows = past
    venue.upcoming_shows = upcoming
    venue.past_shows_count = len(past)
    venue.upcoming_shows_count = len(upcoming)

    return render_template("pages/show_venue.html", venue=venue)


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    try:
        # get form submitted data
        form = VenueForm()
        # create object
        seeking_talent = True if form.seeking_talent.data == "Yes" else False
        venue = Venue(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            genres=form.genres.data,
            facebook_link=form.facebook_link.data,
            website=form.website.data,
            image_link=form.image_link.data,
            seeking_talent=seeking_talent,
            seeking_description=form.seeking_description.data,
        )
        # add venue to session and commit to database
        db.session.add(venue)
        db.session.commit()
        # flash success message if there are no errors
        flash("The Venue " + request.form["name"] + " was submitted successfully!")
    except:
        db.session.rollback()
        flash(
            "The Venue " + request.form["name"] + " was not submitted due to an error."
        )
    finally:
        # close session
        db.session.close()
    return render_template("pages/home.html")


@app.route("/venues/<int:venue_id>/delete")
def delete_venue(venue_id):
    try:
        # get venue using venue_id
        venue = Venue.query.get(venue_id)
        # delete venue
        db.session.delete(venue)
        db.session.commit()
        # flash message if deletion was successful
        flash("The Venue " + venue.name + " was deleted successfully!")
    except:
        db.session.rollback()
        flash(
            "The Venue with id [" + venue_id + "] was not be deleted due to an error."
        )
    finally:
        db.session.close()

    return redirect(url_for("index"))


#  Artists
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():
    data = list()
    # get all the artists from db
    artists = Artist.query.all()
    # add artists to data
    for a in artists:
        data.append({"id": a.id, "name": a.name})
    return render_template("pages/artists.html", artists=data)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    # user search term
    search_term = request.form.get("search_term", "")
    # find all artists matching search term (partial and case insensitivity included)
    artists = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()
    response = {"count": len(artists), "data": []}

    for a in artists:
        num_upcoming_shows = 0
        # get all shows by the artist
        shows = Show.query.filter_by(artist_id=a.id).all()
        # increment upcoming shows
        for s in shows:
            if s.start_time > datetime.now():
                num_upcoming_shows += 1
        # add artists to the response
        response["data"].append(
            {"id": a.id, "name": a.name, "num_upcoming_shows": num_upcoming_shows,}
        )
    # return response with search results
    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    # get artist info using artist_id
    artist = Artist.query.get(artist_id)
    # get all shows by the given artist
    shows = Show.query.filter_by(artist_id=artist_id).all()
    # get past and upcoming show info and count
    upcoming = list()
    past = list()
    for s in shows:
        venue = Venue.query.get(s.venue_id)
        venue_name = venue.name
        venue_image_link = venue.image_link
        if s.start_time > datetime.now():
            upcoming.append(
                {
                    "venue_id": s.venue_id,
                    "venue_name": venue_name,
                    "venue_image_link": venue_image_link,
                    "start_time": format_datetime(str(s.start_time)),
                }
            )
        else:
            past.append(
                {
                    "venue_id": s.venue_id,
                    "venue_name": venue_name,
                    "venue_image_link": venue_image_link,
                    "start_time": format_datetime(str(s.start_time)),
                }
            )
    # add show data to artist
    artist.past_shows = past
    artist.upcoming_shows = upcoming
    artist.past_shows_count = len(past)
    artist.upcoming_shows_count = len(upcoming)

    return render_template("pages/show_artist.html", artist=artist)


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    form = ArtistForm()
    # get artist info using artist_id
    artist = Artist.query.get(artist_id)
    # artist data
    theartist = {"id": artist.id, "name": artist.name}
    # Populate the edit form
    form.process(obj=artist)

    return render_template("forms/edit_artist.html", form=form, artist=theartist)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    try:
        form = ArtistForm()
        # get artist info using artist_id
        artist = Artist.query.get(artist_id)
        # update artist using form data
        artist.name = form.name.data
        artist.genres = form.genres.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.facebook_link = form.facebook_link.data
        artist.image_link = form.image_link.data
        artist.website = form.website.data
        artist.seeking_venue = True if form.seeking_venue.data == "Yes" else False
        artist.seeking_description = form.seeking_description.data
        # commit changes
        db.session.commit()
        flash("The Artist " + request.form["name"] + " was updated successfully!")
    except:
        db.session.rollback()
        flash(
            "The Artist "
            + request.form["name"]
            + " was not be updated due to an error."
        )
    finally:
        db.session.close()

    return redirect(url_for("show_artist", artist_id=artist_id))


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    form = VenueForm()
    # get venue info using venue_id
    venue = Venue.query.get(venue_id)
    # venue data
    thevenue = {"id": venue.id, "name": venue.name}
    # Populate the edit form
    form.process(obj=venue)

    return render_template("forms/edit_venue.html", form=form, venue=thevenue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    try:
        form = VenueForm()
        # get venue info using venue_id
        venue = Venue.query.get(venue_id)
        # update venue using form data
        venue.name = form.name.data
        venue.genres = form.genres.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.facebook_link = form.facebook_link.data
        venue.website = form.website.data
        venue.image_link = form.image_link.data
        venue.seeking_talent = True if form.seeking_talent.data == "Yes" else False
        venue.seeking_description = form.seeking_description.data
        # commit changes
        db.session.commit()
        flash("The Venue " + request.form["name"] + " was updated successfully!")
    except:
        db.session.rollback()
        flash("The Venue " + request.form["name"] + " was not updated due to an error.")
    finally:
        db.session.close()

    return redirect(url_for("show_venue", venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    try:
        # get form submitted data
        form = ArtistForm()
        # create object
        seeking_venue = True if form.seeking_venue.data == "Yes" else False
        artist = Artist(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            genres=form.genres.data,
            facebook_link=form.facebook_link.data,
            website=form.website.data,
            image_link=form.image_link.data,
            seeking_venue=seeking_venue,
            seeking_description=form.seeking_description.data,
        )
        # add artist to session and commit to database
        db.session.add(artist)
        db.session.commit()
        # flash success message if there are no errors
        flash("The Artist " + request.form["name"] + " was submitted successfully!")
    except:
        db.session.rollback()
        flash(
            "The Artist " + request.form["name"] + " was not submitted due to an error."
        )
    finally:
        db.session.close()

    return render_template("pages/home.html")


# ----------------------------------------------------------------------------#
#  Shows
# ----------------------------------------------------------------------------#


@app.route("/shows")
def shows():
    # get all shows
    shows = Show.query.all()
    data = list()
    # get the venue and artist info for each show
    for s in shows:
        artist = Artist.query.get(s.artist_id)
        artist_name = artist.name
        artist_image_link = artist.image_link
        data.append(
            {
                "venue_id": s.venue_id,
                "venue_name": Venue.query.get(s.venue_id).name,
                "artist_id": s.artist_id,
                "artist_name": artist_name,
                "artist_image_link": artist_image_link,
                "start_time": format_datetime(str(s.start_time)),
            }
        )

    return render_template("pages/shows.html", shows=data)


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    try:
        # get form submitted data
        form = ShowForm()
        # create object
        show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data,
        )
        # add show to session and commit to database
        db.session.add(show)
        db.session.commit()
        # flash success message if there are no errors
        flash("The show was submitted successfully!")
    except:
        db.session.rollback()
        flash("The Show was not submitted due to an error.")
    finally:
        db.session.close()

    return render_template("pages/home.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
