import os
import uuid
from datetime import datetime
from random import randrange, choice
import flask
import requests
from PIL.Image import Image
from flask import Flask, render_template, request, redirect, url_for
from lastfmtools.gif_creator import gif_creator
from lastfmtools.bubble import bubble_chart

app = Flask(__name__)


def clean_up():
    files = os.listdir("static/results")

    for file in files:
        os.remove("static/results/" + file)


usernames = (
    "heroesluk", "Ryryk", "Zajii", "kaasi06", "PixelSun", "SniperWolf92", "aroquis", "calikasan", "skvce", "Ididealism")


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("main.html")


@app.route("/bubbles", methods=["GET", "POST"])
def bubbles():
    if request.method == "POST":
        file_name = uuid.uuid4()

        if len(request.form.keys()) == 0:
            bubble_type = "album"
            number_of_bubbles = randrange(30, 100)
            nickname = choice(usernames)
        else:
            bubble_type = request.form['record_type']
            number_of_bubbles = request.form['records_number']
            nickname = request.form['nickname']

        bubble = bubble_chart(bubble_type, int(number_of_bubbles), nickname, "static/" + str(file_name))
        if bubble:
            bubble.save("static/{}.png".format(file_name))
            return redirect(url_for("display_bubble", file_name=str(file_name)))

    return render_template("select_bubble.html")


@app.route("/display_bubble", methods=["GET", "POST"])
def display_bubble():
    if request.method == "POST":
        if 'color' in request.form.keys():
            print(request.form['color'])

    filename = request.args.get("file_name")
    return render_template("display_bubble.html", file_name=filename)


############################################
##########GIF CREATOR#######################
############################################


@app.route("/mosaic", methods=["GET", "POST"])
def mosaic():
    if request.method == "POST":
        if len(request.form.keys()) == 0:
            date_str = "2022-01-01"
            matrix_size = randrange(3, 6)
            time_delta = "3month"
            nickname = choice(usernames)
        else:
            date_str = request.form["start_date"]
            matrix_size = request.form["matrix_size"]
            time_delta = request.form["time_delta"]
            nickname = request.form["nickname"]

        start_date = datetime.strptime(date_str, "%Y-%m-%d")

        file_name = uuid.uuid4()

        mosaic = gif_creator(start_date, time_delta, int(matrix_size), nickname)
        if mosaic:
            mosaic.save("static/{}.gif".format(file_name),save_all=True)

            return redirect(url_for("display_mosaic", file_name=file_name))

    return render_template("select_mosaic.html")


@app.route("/display_mosaic", methods=["GET"])
def display_mosaic():
    file_name = request.args.get("file_name")

    return render_template("display_mosaic.html", file_name=file_name)


# dynamically showing user the maximum size of mosaic gif
@app.route("/about", methods=["GET"])
def about():
    return render_template("about me.html")


@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact_me.html")


@app.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy_note.html")
