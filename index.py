from flask import Flask, render_template, send_file, jsonify, request
import json

app = Flask(__name__)

@app.route("/pages/<page_name>/css/<style>")
def get_css(page_name, style):
    return send_file("pages/" + page_name + "/css/" + style, "text/css")

@app.route("/pages/<page_name>/js/<script>")
def get_js(page_name, script):
    return send_file("pages/" + page_name + "/js/" + script, "text/javascript")

@app.route("/pages/<page_name>/images/<image>")
def get_image(page_name, image):
    return send_file("pages/" + page_name + "/images/" + image, "text/javascript")

@app.route("/favicon.ico")
def get_favicon():
    return jsonify(success=True)

@app.route("/<name>")
def hello_world(name):
    with open("pages/xss/data/data.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())["data"]

    page = """
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
    <title>XSS Demo</title>
    <link rel="stylesheet" type="text/css" href="/pages/xss/css/style.css">
    <link rel="stylesheet" type="text/css" href="/pages/xss/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="/pages/xss/css/font-awesome.min.css">
<!--    <script src="/pages/xss/js/jquery.min.js" type="text/javascript"></script>
    <script src="/pages/xss/js/bootstrap.bundle.min.js" type="text/javascript"></script> -->

</head>
<body>
<div class="container mt-5 mb-5">
    <div class="d-flex justify-content-center row">
        <div class="d-flex flex-column col-md-8">
            <div class="d-flex flex-row align-items-center text-left comment-top p-2 bg-white border-bottom px-4">
                <div class="profile-image"><img class="rounded-circle" src="/pages/xss/images/t9toMAQ.jpg" width="70"></div>
                <div class="d-flex flex-column ml-3">
                    <div class="d-flex flex-row post-title">
                        <h5>Как вам уроки в OTUS?</h5><span class="ml-2">(Виктор, преподаватель)</span>
                    </div>
                    <div class="d-flex flex-row align-items-center align-content-center post-title">
                        <span class="bdge mr-1">Вопрос</span>
                        <span class="mr-2 comments">""" +  str(len(data)) + """ комментариев</span>
                        <span class="mr-2 dot"></span><span>17 часов назад</span>
                    </div>
                </div>
            </div>
            <div class="coment-bottom bg-white p-2 px-4">
                <div class="d-flex flex-row add-comment-section mt-4 mb-4">
                    <img class="img-fluid img-responsive rounded-circle mr-2" src="/pages/xss/images/qdiP4DB.jpg" width="38">
                    <input id="comment-text" type="text" class="form-control mr-3" placeholder="Add comment">
                    <button id="comment-button" class="btn btn-primary" type="button">Comment</button>
                </div>"""

    for item in data:
        new_elem = """
        <div class="commented-section mt-2">
            <div class="d-flex flex-row align-items-center commented-user">
                <h5 class="mr-2">""" + item['name'] + """</h5>
                <span class="dot mb-1"></span>
                <span class="mb-1 ml-2">""" + item['hours_ago'] + """ </span>
            </div>
            <div class="comment-text-sm">
                <span>""" + item['comment'] + """</span>
            </div>
        </div>"""
        page += new_elem

    page += """
                   </div>
            </div>
        </div>
    </div>
</div>
<script src="/pages/xss/js/script.js" type="text/javascript"></script>
</body>
</html>
"""

    return page


@app.route("/post_comment", methods=["POST"])
def post_comment():
    body = request.get_json()
    with open("pages/xss/data/data.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    data["data"].insert(0, {
        "name": body["name"],
        "hours_ago": body["hours_ago"],
        "comment": body["comment"]
    })
    with open("pages/xss/data/data.json", "w", encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
    return jsonify(success=True)