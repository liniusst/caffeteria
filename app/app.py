# pylint: disable= missing-docstring
from flask import Flask, render_template, redirect, url_for, flash
import utilities.forms as forms
from utilities.database import db_session
from backend import Reservation

database = db_session()
app = Flask(__name__)
app.config["SECRET_KEY"] = "4654f5dfadsrfasdr54e6rae"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/check-reservation", methods=["GET", "POST"])
def check_reservation():
    form = forms.UserInformation()
    if form.validate_on_submit():
        reservation = Reservation()
        user_reservations = reservation.filter_client_reservations(form.firstname.data)
        if user_reservations:
            return render_template(
                "reservations-list.html",
                title="Check reservations",
                user_reservations=user_reservations,
                user_name=form.firstname.data,
            )
        else:
            flash("We can't find any reservations", "danger")
    return render_template(
        "check-reservation.html", title="Check reservations", form=form
    )


@app.route("/create-reservation", methods=["GET", "POST"])
def create_reservation():
    form = forms.NewReservation()
    if form.validate_on_submit():
        reservation = Reservation()
        reservation.enable_validation_scheme()
        new_reservations = reservation.create_reservation(
            form.firstname.data, form.seats.data, form.time.data
        )
        if new_reservations:
            flash("Reservation added successfully", "success")
            return redirect(url_for("index"))
        else:
            flash("We can't add new reservations", "danger")
    return render_template(
        "create-reservation.html", title="Create reservations", form=form
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
