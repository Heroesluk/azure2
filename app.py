import os
import uuid
from datetime import datetime

import flask
from flask import Flask, render_template, request, redirect, url_for

from gif_creator import gif_creator
app = Flask(__name__)
from bubble import main


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route("/", methods=["GET", "POST"])
def home():

    return render_template("main.html")


@app.route("/bubbles", methods=["GET", "POST"])
def bubbles():
    if request.method == "POST":
        file_name = uuid.uuid1()
        bubble_type = request.form['record_type']
        number_of_bubbles = request.form['records_number']
        nickname = request.form['nickname']
        main(bubble_type, int(number_of_bubbles), nickname, str(file_name))

        return redirect(url_for("display_bubble", file_name=file_name))

    return render_template("bubble_select.html")


@app.route("/display_bubble", methods=["GET", "POST"])
def display_bubble():

    if request.method=="POST":
        if 'color' in request.form.keys():
            print(request.form['color'])

    filename = request.args.get("file_name")
    return render_template("display_results.html", file_name=filename)



############################################
##########GIF CREATOR#######################
############################################

@app.route("/mosaic", methods=["GET", "POST"])
def mosaic():
    if request.method=="POST":
        print("tak")
        date_str = request.form["start_date"]
        matrix_size = request.form["matrix_size"]
        time_delta = request.form["time_delta"]

        start_date = datetime.strptime(date_str,"%Y-%m-%d")
        gif_creator(start_date, time_delta, int(matrix_size))

        return redirect(url_for("display_mosaic"))



    else:

        return render_template("mosaic.html")

@app.route("/display_mosaic", methods=["GET"])
def display_mosaic():
    return render_template("display_mosaic.html")

