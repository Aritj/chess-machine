from flask import Flask, render_template, request
from motorcontroller import StepperMotorController
from json import loads

app: Flask = Flask(__name__)

@app.route('/move', methods=['POST'])
def move() -> str:
    with StepperMotorController() as controller:
        controller.move(loads(request.data))
    return "", 204

@app.route('/', methods=['GET'])
def index() -> str:
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
