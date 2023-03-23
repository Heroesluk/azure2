from flask import Flask, render_template, request, redirect, url_for
import os
from ColorScripts.color_check import return_imgs_with_most_color
from ColorScripts.colors import ColorPalette

app = Flask(__name__)
from datetime import datetime
from bubble import main


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        name = request.form["user_name"]
        print(name)

    return render_template("main.html")


@app.route("/bubbles", methods=["GET", "POST"])
def bubbles():
    if request.method == "POST":
        bubble_type = request.form['record_type']
        number_of_bubbles = request.form['records_number']
        nickname = request.form['nickname']
        main(bubble_type, int(number_of_bubbles), nickname)

        return redirect(url_for("display_bubble"))

    return render_template("bubble_select.html")


@app.route("/display_bubble", methods=["GET", "POST"])
def display_bubble():
    return render_template("display_results.html")
