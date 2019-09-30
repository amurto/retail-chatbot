import numpy as np
from vc import results
from flask import Flask, render_template, request, jsonify
# Initialize the Flask application
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/_add_numbers')
def predict():
    print("Start talking with the bot (type quit to stop)!")
    inp = request.args.get('a')
    print(inp)
    if inp.lower() == "quit":
        return render_template('quit.html')
    res = results(inp)
    print(res)
    return jsonify(result=inp, op=res)


if __name__ == '__main__':
    app.run()
