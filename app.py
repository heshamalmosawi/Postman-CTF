from flask import Flask, jsonify, make_response, render_template, request

app = Flask(__name__)
app.json.sort_keys = False

@app.route("/")
def index():
    return "<h1>Postman CTF</h1><p> Welcome to the &lt;challenge_name&gt;! In this &lt;challenge_name&gt we will explore how the web works, focusing in on HTTPS. As a first step, we will learn about the HTML Language. Please visit '<a href='/html'>/html</a>' to learn more!</p>"

@app.route("/challengeinfo", methods=["GET", "POST"])
def challengeinfo():
    if request.method == "GET":
        response = make_response(render_template('challengeinfo_get.html'), 405)
        return response
    elif request.method == "POST":
        return jsonify({
            "Greetings": "Welcome to the challenge!",
            "Goal": "To collect all flags and submit them through <github pages url>",
            "Example": "As example, you would send an HTTP request through the Postman application and get a flag that will be written in the format 'FLAG1_ABCDE'",
            "Next-step": "Navigate to the '/getrequest' path to continue with the challenge."
        })


@app.route("/html", methods=["GET"])
def html():
    return render_template('htmlpage.html')

@app.route("/http", methods=["GET"])
def http():
    return render_template('httppage.html')

@app.route("/formexample", methods=["GET"])
def form_example():
     return render_template('formexample.html')

@app.route("/getrequest", methods=["GET"])
def getreq():
    # if not 'Postman' in request.headers.get('User-Agent'):
    #     return make_response(render_template('gobacktopostman.html'), 403) 
    match request.args.get('name'):
        case None:
            #TODO: MAYBE ADD AN ACTUAL ERROR PAGE
            return make_response(jsonify({"error":"Missing GET parameter. Please guess a number 1-10 through a GET request."}), 400) 
        case "1" | "2" | "3" | "4" | "5" | "6" | "7" | "9":
            return make_response(jsonify({"Wrong guess": f"{request.args.get('name')} is not the correct number! please try again."}))
        case "8":
            return render_template('successwithflag.html', flag='FLAG2_NMBDV', next='postform')
        case _:
            return make_response(jsonify({"error":"Invalid GET parameter. Please send an HTTP request with a valid Parameter."}), 400)



@app.route('/postform', methods=["GET", "POST"])
def form():
    if not 'Postman' in request.headers.get('User-Agent'):
        return make_response(render_template('gobacktopostman.html'), 403)
    
    if request.method == 'GET':
        return render_template('formexercise.html')
    elif request.method == 'POST':
        #
        number = request.form.get('number') 
        if number == '400':
            return jsonify({
                "response": "Good job! Here is the third flag {FLAG3_RBOOT}",
                "info": "GET parameters are typically used to identify resources for the response and are visible in the URL, whilst POST values are usually used to submit data without exposing it in the URL, such as login details etc.",
                "next-step": "Visit the /challenge path for your fourth flag."
            })
        else:
            return make_response( jsonify({
                "error": "HTTP POST request with invalid or empty form data! GET the page to view the form."
            }), 400)

@app.route('/freeflag', methods=["GET", "POST"])
def freeflag():
    if not 'Postman' in request.headers.get('User-Agent'):
        return render_template('freeflag.html')
    elif request.method == 'POST':
        return jsonify({'flag':'FLAG7_VOERJ'})
    else:
        return '''<p>This is not a POST request!</p>'''

@app.route('/challenge', methods=["GET"])
def challenge():
    if not 'Postman' in request.headers.get('User-Agent'):
        return make_response(render_template('gobacktopostman.html'), 403)
    
    sha_cookie = request.cookies.get('SHA256_ENCRYPTED')

    if request.method == 'GET':
        if sha_cookie:
            return render_template('successwithflag.html', flag='FLAG5_EF2NJ', message='Try playing with your cookies for the next flag. On a browser, visit the <a href=/freeflag>/freeflag</a> for your next flag.')
        else:
            return make_response(render_template('challenger.html'), 401)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('loginer.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        if name == 'YWRtaW4K':
            return jsonify({'flag': '{flag4_HNIVW}', 
                            'Message': 'Send a GET request to /challenge with the cookies with the value below to get your next flag.',
                            'first-cookie': 'SHA256_ENCRYPTED=33674db2d4e3b45263374658a165544f44af510a6fd304d100d1aed81971ccd1; Path=/; Expires=Tue, 05 Aug 2025 18:20:00 GMT;',
                            'second-cookie': 'getflag = false; Path=/; Expires=Tue, 05 Aug 2025 18:20:00 GMT;'
                            })
        else:
            return "<h1>Try Again</h1>"

@app.before_request
def before_request_func():
    flag = request.cookies.get('getflag')
    if flag == 'true':
        return jsonify({'flag6': 'getflag cookie is set to true! heres you\'re next flag {FLAG6_GRWNO}',
                        'message': 'Now remove this cookie or set it back to false to continue the challenge.'})

if __name__ == '__main__':
    app.run(debug=True)
