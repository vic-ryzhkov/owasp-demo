from flask import Flask, render_template

app = Flask(__name__)

@app.route("/xss")
def hello_world(name):
    return render_template('xss.html', name=name)

