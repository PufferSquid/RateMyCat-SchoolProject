from flask import Blueprint, request
from statsig import statsig, StatsigUser
from flask import Flask

statsig.initialize('secret-RAhLG2aub8QdUaBrzzGLzLqIJt9aJGyg3ioIbAldyqU')
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"


@app.route('/experiment/', methods=['GET'])
def experimentRoute():
    userID = request.args.get('userID') 
    user = StatsigUser(user_id=userID)
    statsig.check_gate(user, "first_gate")
    background_color = statsig.get_experiment(user, "test_experiment").get("background_color", "green") # green is default (if we can't get the color from statsig)
    return f"{userID} <body style='background-color: {background_color}'>"




app.run(debug=True)



