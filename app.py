from flask import Flask, jsonify, make_response, render_template, request

app = Flask(__name__)
app.json.sort_keys = False

@app.route("/")
def index():
    if request.args.get('gethint') == 'flag10':
        return '''<p> Ever wonder how the secrets of the universe are hidden? Sometimes, you might need to dig through the image to uncover the truth. Maybe a hexadecimal explorer could help you find what you're looking for! </p> <br/> <p> Is there an explorer in the terminal? </p>'''

    return "<h1>Postman CTF</h1><p> Welcome to the Postman challenge! In this capture-the-flag activity we will explore how the web works, focusing in on HTTPS. As a first step, we will learn about the HTML Language. Please visit '<a href='/html'>/html</a>' to learn more!</p>"

@app.route("/html", methods=["GET"])
def html():
    return render_template('htmlpage.html')

@app.route("/formexample", methods=["GET"])
def form_example():
     return render_template('formexample.html')

@app.route("/http", methods=["GET"])
def http():
    return render_template('httppage.html')

@app.route("/challengeinfo", methods=["GET", "POST"])
def challengeinfo():
    if request.method == "GET":
        response = make_response(render_template('challengeinfo_get.html'), 405)
        return response
    elif request.method == "POST":
        return jsonify({
            "Greetings": "Welcome to the challenge!",
            "Goal": "To collect all flags and submit them through the '/submitflags' path.",
            "Example": "As example, you would send an HTTP request through the Postman application and get a flag that will be written in the format 'FLAG1_ABCDE'",
            "Next-step": "Navigate to the '/flag2' path to continue with the challenge." #TODO update url
        })

@app.route("/flag2", methods=["GET"])
def flag2():
    if not 'Postman' in request.headers.get('User-Agent'):
        return make_response(render_template('gobacktopostman.html'), 403)

    if request.args.get('get') == 'hint':
        return render_template('flag2q.html', message="Instead of 'get'-ing the hint, try 'take'-ing the flag.", message2="hint: the query param is 'take'. ")
    elif request.args.get('take') == 'flag':
        return render_template('successwithflag.html', flag='FLAG2_NMBDV' , next="getrequest", message="Try to guess a number 1-10 through the GET request.")
    else:
        slashmessage="After the main route is over, you can ask for more specific data using a GET request with a query"
        slashhint="Try asking for how to get the flag using adding '?get=hint' to the URL."
        return render_template("flag2q.html", message=slashmessage, message2=slashhint)
    
@app.route("/getrequest", methods=["GET"])
def getreq():
    if not 'Postman' in request.headers.get('User-Agent'):
        return make_response(render_template('gobacktopostman.html'), 403) 
    
    match request.args.get('number'):
        case None:
            #TODO: MAYBE ADD AN ACTUAL ERROR PAGE
            return make_response(jsonify({"error":"Missing GET parameter. Please guess a number 1-10 through a GET request."}), 400) 
        case "1" | "2" | "3" | "4" | "5" | "6" | "7" | "9":
            return make_response(jsonify({"Wrong guess": f"{request.args.get('number')} is not the correct number! please try again."}))
        case "8":
            return render_template('successwithflag.html', flag='FLAG3_RBOOT', next='postform') 
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
        number = request.form.get('code') 
        if number == '400':
            return jsonify({
                "response": "Good job! Here is the fourth flag {FLAG4_HNIVW}",
                "info": "POST values are usually used to submit data without exposing it in the URL, such as login details etc.",
                "info2": "POST requests are generally more secure than GET requests for sending sensitive data, as POST sends the data in the request body rather than in the URL.",
                "next-step": "Visit the /challenge path for your fifth flag."
            })
        else:
            return make_response( jsonify({
                "error": "HTTP POST request with invalid or empty form data! GET the page to view the form."
            }), 400)
        
    return make_response(jsonify({"error": "Invalid request, please send form data through Postman"}), 405)

@app.route('/challenge', methods=["GET"])
def challenge():
    if not 'Postman' in request.headers.get('User-Agent'):
        return make_response(render_template('gobacktopostman.html'), 403)
    
    sha_cookie = request.cookies.get('BASE64_ENCRYPTED')

    if request.method == 'GET':
        if sha_cookie:
            return render_template('successwithflag.html', flag='FLAG6_GRWNO', message='\n Cookies are like a website storing a note about you, to remember information such as if you are logged in or not, or your favorite settings in the website etc. \n Try playing with your cookies for the next flag.')
        else:
            return make_response(render_template('challenger.html'), 401)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('loginer.html')
    elif request.method == 'POST':
        name = request.form.get('username')
        pwd = request.form.get('password')
        if name == 'admin' and pwd == 'admin':
            return jsonify({'flag': 'FLAG5_EF2NJ', 
                            'Message': 'Add the below cookies to Postman, then send a GET request to /challenge for your next flag.',
                            'first-cookie': 'BASE64_ENCRYPTED=Q2hhbmdlIHRoZSBzZWNvbmQgZmxhZyAnZmFsc2UnIHRvICd0cnVlJyBmb3IgeW91ciA3dGggZmxhZy4K; Path=/; Expires=Tue, 05 Aug 2025 18:20:00 GMT;',
                            'second-cookie': 'getflag = false; Path=/; Expires=Tue, 05 Aug 2025 18:20:00 GMT;'
                            })
        else:
            return "<h1>Try Again</h1>"

@app.before_request
def before_request_func():
    flag = request.cookies.get('getflag')
    if flag == 'true':
        return jsonify({'flag7': 'getflag cookie is set to true! heres you\'re next flag {FLAG7_VOERJ}',
                        'message': 'Now remove this cookie or set it back to false to continue the challenge.',
                        'next': "Lets get out of postman and go back to the real world! Visit the '/freeflag' path on Firefox or Chromium to get a free flag."
                        })

@app.route('/freeflag', methods=["GET", "POST"])
def freeflag():
    if not 'Postman' in request.headers.get('User-Agent'):
        return render_template('freeflag.html')
    elif request.method == 'POST':
        return jsonify({
                        'flag':'FLAG8_DJSND',
                        'next': 'Navigate to /flag9 for your next flag.',
                        })
    else:
        return '''<p>This is not a POST request!</p>'''


@app.route('/flag9', methods=["GET", "POST"])
def flag9():
    if 'Postman' in request.headers.get('User-Agent'):
        return render_template("justatemplate.html", message="To see what’s hidden, you must look beneath the surface. Try curling a more detailed view.")
    elif 'curl' in request.headers.get('User-Agent'):
        if request.method == 'POST':
            code = request.form.get('code')
            if not code:
                response =  make_response(render_template("justatemplate.html", message="Great Job! Now try sending a POST request through 'curl' with the HTTP 'code' of status 'Forbidden'."))
            elif code == '403':
                response = make_response(render_template("justatemplate.html", message="Great! You’re getting closer. The devil is in the details, pay attention to the verbose output!", hint="hint: VXNlIGN1cmwgd2l0aCBhIHNwZWNpYWwgcGFyYW1ldGVyOiAnY3VybCAtdicK"))
            else: 
                response = make_response(render_template("justatemplate.html", message="The code is incorrect. Please send a POST request with the correct HTTP code to proceed."))
            response.headers['FLAG'] = 'FLAG9_FGEWD'
            response.headers['NEXT_FLAG'] = "The next flag is hidden _INSIDE_ one of the images on this website. You can add '/static/IMAGENAME.jpg' at the end of the URL and visit it on a browser to download them."
            response.headers["FLAG10_HINT"] = "To get a hint, you can send a GET request to the original URL with '?gethint=flag10'"
            return response
        else: 
            return render_template("justatemplate.html", message="To proceed, send a POST request through 'curl' with the HTTP 'code' of status 'Forbidden'.")
    else:
        return make_response(render_template('gobacktopostman.html'), 403)


@app.route('/submitflags')
def submitflag():
    return render_template('submitflag.html')

if __name__ == '__main__':
    app.run(debug=True)
