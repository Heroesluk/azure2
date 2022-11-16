from flask import Flask, render_template, request, redirect, url_for
import os, sys
from Main import generate_mosaic
from DownloadDataAndAlbums import get_albums

app = Flask(__name__)

IMG_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER
images = [i for i in os.listdir("static/images")]


# learn how to upload files


@app.route("/")
def hello_world():
    get_albums('heroesluk')

    return render_template('main.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = int(request.form["matrix_size"])
        return redirect(url_for("index", size=user))

    else:
        return render_template("login.html")


@app.route("/<size>", methods=["GET", "POST"])
def index(size):
    size = int(size)
    mosaic_images = generate_mosaic(size)
    data = [os.path.join('static/images', i) for i in mosaic_images][:size*size]

    return render_template("index.html", image_file=data)


@app.route("/<usr>", methods=["GET", "POST"])
def user(usr):
    return f"<h1>{usr}</h1>"
