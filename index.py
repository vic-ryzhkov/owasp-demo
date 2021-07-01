from flask import Flask, make_response, send_file, jsonify, request
import json

app = Flask(__name__)

@app.route("/pages/<page_name>/css/<style>")
def get_css(page_name, style):
    return send_file("pages/" + page_name + "/css/" + style, "text/css")


@app.route("/pages/<page_name>/fonts/<font>")
def get_font(page_name, font):
    return send_file("pages/" + page_name + "/fonts/" + font, "font/woff2")


@app.route("/pages/<page_name>/js/<script>")
def get_js(page_name, script):
    return send_file("pages/" + page_name + "/js/" + script, "text/javascript")

@app.route("/pages/<page_name>/images/<image>")
def get_image(page_name, image):
    return send_file("pages/" + page_name + "/images/" + image, "text/javascript")

@app.route("/favicon.ico")
def get_favicon():
    return jsonify(success=True)

@app.route("/comments")
def get_xss_page():
    with open("pages/xss/data/comments.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())["data"]
    lang = request.args.get("lang")
    if not lang:
        lang = "RU"

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
    <body class="d-flex flex-column h-100">
    <header>
    <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
        <a class="navbar-brand" href="/comments">OTUS</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
              <a class="nav-link" href="#">Курсы<span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">События</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">О нас</a>
            </li>
          </ul>
          <div class="d-flex flex-row-reverse">
            <button id="search-button" class="btn btn-outline-success my-2 my-sm-0">Найти</button>
            <input id="search-text" class="form-control mr-sm-2" type="text" placeholder="Поиск по сайту" aria-label="Search">
            
          </div>
        </div>
  </nav>
  </header>
  <br>
  <br>
  <br>
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
                    <p class="font-italic"><small id="current-lang">Ваш текущий язык: """ + """</small></p>
                </div>
            </div>
            <div class="coment-bottom bg-white p-2 px-4">
                <div class="d-flex flex-row add-comment-section mt-4 mb-4">
                    <img class="img-fluid img-responsive rounded-circle mr-2" src="/pages/xss/images/qdiP4DB.jpg" width="38">
                    <input id="comment-text" type="text" class="form-control mr-3" placeholder="Добавьте комментарий">
                    <button id="comment-button" class="btn btn-primary" type="button">Ответить</button>
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
    resp = make_response(page)
    resp.set_cookie('userID', 'cyimH0C9gX8MguUs9MEqcy6g4o5imhgiSSj5tqm9WNuehH5FiB')
    resp.set_cookie('sessionID', 'DWZmCXyR2lWxaspif6HJjkf37O7mrDlDLxGAKynvvRDOL291rVa9Oe73hLDtZyAjGZ6vXRo5yRfnXjo5')
    return resp


@app.route("/post_comment", methods=["POST"])
def post_comment():
    body = request.get_json()
    with open("pages/xss/data/comments.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    data["data"].insert(0, {
        "name": body["name"],
        "hours_ago": body["hours_ago"],
        "comment": body["comment"]
    })
    with open("pages/xss/data/comments.json", "w", encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
    return jsonify(success=True)


@app.route("/search", methods=["GET"])
def get_search_results():
    with open("pages/xss/data/contents.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())["contents"]

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
        <body class="d-flex flex-column h-100">
        <header>
        <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
            <a class="navbar-brand" href="/comments">OTUS</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarCollapse">
              <ul class="navbar-nav mr-auto">
                <li class="nav-item active">
                  <a class="nav-link" href="#">Курсы<span class="sr-only">(current)</span></a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#">События</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#">О нас</a>
                </li>
              </ul>
            <div class="d-flex flex-row-reverse">
                <button id="search-button" class="btn btn-outline-success my-2 my-sm-0">Найти</button>
                <input id="search-text" class="form-control mr-sm-2" type="text" placeholder="Поиск по сайту" aria-label="Search">
            
            </div>
            </div>
      </nav>
      </header>
      <br>
      <br>
      <br>
    <div class="alert alert-success" role="alert">
        Результаты поиска по запросу:"""

    q = str(request.args.get("q"))
    page += q

    page += """
    </div>
    """
    for item in data:
        if q.lower() in item["name"].lower():
            page += """<div class="card w-75">
  <div class="card-body">
    <h5 class="card-title">""" + item["name"] + """</h5>
    <p class="card-text">""" + item["description"] + """</p>
    <a href="#" class="btn btn-primary">Подробнее</a>
  </div>
</div>"""


    page += """
    <script src="/pages/xss/js/script.js" type="text/javascript"></script>
    </body>
    </html>
    """
    resp = make_response(page)
    resp.set_cookie('userID', 'cyimH0C9gX8MguUs9MEqcy6g4o5imhgiSSj5tqm9WNuehH5FiB')
    resp.set_cookie('sessionID', 'DWZmCXyR2lWxaspif6HJjkf37O7mrDlDLxGAKynvvRDOL291rVa9Oe73hLDtZyAjGZ6vXRo5yRfnXjo5')
    return resp


