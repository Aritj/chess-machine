from flask import Flask, render_template, redirect, url_for, request

from validation import is_valid_move

from controllers import ServoController

app: Flask = Flask(__name__)

@app.route('/chess', methods=['GET'])
def chess() -> str:
    return render_template('chess.html')

@app.route('/move', methods=['POST'])
def move():
    source = request.args.get('Source')
    target = request.args.get('Target')
    piece = request.args.get('Piece')

    form: dict[str, str] = {
        "fileFrom": source[0],
        "rankFrom": source[1],
        "fileTo": target[0],
        "rankTo": target[1],        
    }

    if is_valid_move(form):
        with ServoController() as controller:
            controller.move(
                source[0],
                source[1],
                target[0],
                target[1]
            )
    
    return ""

@app.route('/', methods=['POST', 'GET'])
def index() -> str:
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        if not is_valid_move(request.form):
            return redirect(url_for('index'))

        with ServoController() as controller:
            controller.move(
                request.form.get("fileFrom"),
                request.form.get("rankFrom"),
                request.form.get("fileTo"),
                request.form.get("rankTo")
            )

        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
