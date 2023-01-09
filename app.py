from flask import Flask, render_template, redirect, url_for, request
from controller import Controller
from json import loads

app: Flask = Flask(__name__)


@app.route('/move', methods=['POST'])
def move() -> str:
    with Controller() as controller:
        controller.move(loads(request.data))
    return '', 204

@app.route('/reset', methods=['GET'])
def reset() -> str:
    with Controller() as controller:
        controller.reset()
    return redirect(url_for('index'))

@app.route('/', methods=['GET'])
def index() -> str:
    return render_template('index.html')

@app.route('/test', methods=['GET'])
def test() -> str:
    return render_template('test.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
