# pylint: disable= missing-docstring
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class UserInformation(FlaskForm):
    firstname = StringField("First name")
    email = StringField("Email")
    submit = SubmitField("Check reservation")


class NewReservation(FlaskForm):
    firstname = StringField("First name", [DataRequired()])
    email = StringField("Email", [DataRequired()])
    seats = IntegerField("Seats", [DataRequired()])
    time = StringField("Time (HH:MM)", [DataRequired()])
    submit = SubmitField("Create reservation")
