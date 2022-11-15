from flask import Flask, render_template, request, redirect, url_for
import os
app = Flask(__name__)



IMG_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER
images = [i for i in os.listdir("static/images")]



@app.route("/")
def hello_world():
    print(IMG_FOLDER)
    return render_template('main.html')


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = int(request.form["nm"])
        return redirect(url_for("index", size=user))

    else:
        return render_template("login.html")





@app.route("/<size>", methods=["GET","POST"])
def index(size):
    print(images)
    data = [os.path.join('static/images', i) for i in images][:int(size)]

    return render_template("index.html", image_file=data)


@app.route("/<usr>", methods=["GET","POST"])
def user(usr):
    return f"<h1>{usr}</h1>"
