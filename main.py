from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Postman CTF</h1><p> Welcome to the &lt;challenge_name&gt;! In this &lt;challenge_name&gt we will explore how the web works, focusing in on https. As a first step, we will learn about the HTML Language. Please visit '<a href='/html'>/html</a>' to learn more!</p>"

@app.route("/challengeinfo", methods=["GET", "POST"])
def test():
    if request.method == "GET":
        return render_template('challengeinfo_get.html')
    elif request.method == "POST":
        return jsonify({
        "message": "Welcome to the challenge! We can start with... [TODO] "
        })


@app.route("/html", methods=["GET"])
def html():
    return render_template('htmlpage.html')

@app.route("/http", methods=["GET"])
def http():
    return render_template('httppage.html')

@app.route('/form', methods=["GET"])
def form():
    return render_template('formexample.html')

if __name__ == '__main__':
    app.run