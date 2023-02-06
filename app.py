from flask import Flask, render_template, request, redirect, url_for
import os
from ColorScripts.color_check import return_imgs_with_most_color
from database import select_from_id_list
from DownloadDataAndAlbums import download_album_covers
from ColorScripts.colors import ColorPalette

app = Flask(__name__)

IMG_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER
images = [i for i in os.listdir("static/images")]

clr = ColorPalette()


def clear_img_results():
    for f in os.listdir('static/images'):
        os.remove(os.path.join('static/images',f))


@app.route("/", methods=["GET", "POST"])
def hello_world():

    if request.method == "POST":
        name = request.form["user_name"]
        print(name)


    return render_template("main.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    clear_img_results()

    if request.method == "POST":
        lenght = (request.form["matrix_size"])
        color_name = request.form["mosaic_color"]
        print(color_name,'huj')

        color = clr.access_by_name(color_name)
        print(color,'huj')

        imgs = return_imgs_with_most_color(int(lenght)*int(lenght), 'AlbumCovers', color)
        imgs = select_from_id_list(imgs)
        download_album_covers(imgs, 'static/images')

        return redirect(url_for("image", lng=lenght))


    return render_template("login.html")


@app.route("/<lng>", methods=["GET", "POST"])
def image(lng):
    data = [os.path.join('static/images', i) for i in os.listdir('static/images')][:int(lng)*int(lng)]
    print(data)

    return render_template("index.html", image_file=data)


@app.route("/<usr>", methods=["GET", "POST"])
def user(usr):
    return f"<h1>{usr}</h1>"
