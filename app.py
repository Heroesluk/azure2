from flask import Flask, render_template, request, redirect, url_for
import os, sys
from color_check import return_imgs_with_most_color
from database import select_from_id_list
from DownloadDataAndAlbums import download_album_covers
from colors import ColorPalette

app = Flask(__name__)

IMG_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER
images = [i for i in os.listdir("static/images")]

clr = ColorPalette()

# learn how to upload files


@app.route("/")
def hello_world():
    imgs = return_imgs_with_most_color(3, 'AlbumCovers', clr.GREEN)
    imgs = select_from_id_list(imgs)

    download_album_covers(imgs, 'static/images')

    print('ready')

    return render_template('main.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["matrix_size"]
        return redirect(url_for("user", usr=user))

    else:
        return render_template("login.html")


@app.route("/image", methods=["GET", "POST"])
def image():
    data = [os.path.join('static/images', i) for i in os.listdir('static/images')]

    return render_template("index.html", image_file=data)


@app.route("/<usr>", methods=["GET", "POST"])
def user(usr):
    return f"<h1>{usr}</h1>"
