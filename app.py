from flask import Flask, render_template, request
from motorcontroller import StepperMotorController
from json import loads
from validation import is_valid_chess_move

app: Flask = Flask(__name__)

@app.route('/move', methods=['POST'])
def move() -> str:
    chess_move = loads(request.data)
    
    if not is_valid_chess_move(chess_move):
        return "Invalid chess move", 400

    with StepperMotorController() as controller:
        controller.move(chess_move)

    return "Valid chess move", 200

@app.route('/', methods=['GET'])
def index() -> str:
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
