from flask import Flask, render_template, redirect, url_for, request

from validation import is_valid_move

from controllers import ServoController

app: Flask = Flask(__name__)


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
