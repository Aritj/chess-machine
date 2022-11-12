from flask import Flask, render_template, request

from validation import is_valid_move

from motorcontroller import StepperMotorController

app: Flask = Flask(__name__)


@app.route('/move', methods=['POST'])
def move() -> str:
    if is_valid_move(request.args):
        with StepperMotorController() as controller:
            controller.move(
                request.args.get('fileFrom'),
                request.args.get('rankFrom'),
                request.args.get('fileTo'),
                request.args.get('rankTo')
            )
        return "Valid move", 200

    return "Invalid move", 400


@app.route('/', methods=['GET'])
def index() -> str:
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
