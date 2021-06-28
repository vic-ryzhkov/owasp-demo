from flask import Flask, render_template

app = Flask(__name__)

@app.route("/<name>")
def hello_world(name):
    return render_template('index.html', name=name)