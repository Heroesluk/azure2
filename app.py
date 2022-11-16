from flask import Flask, render_template, request, redirect, url_for
import os, sys
from Main import main
app = Flask(__name__)



IMG_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER
images = [i for i in os.listdir("static/images")]


#learn how to upload files



@app.route("/")
def hello_world():
    data = main()
    return render_template('main.html')


