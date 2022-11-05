from flask import Flask, render_template, redirect, url_for, request

from validation import is_valid_move

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index() -> str:
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        if not is_valid_move(request.form):
            return redirect(url_for('index'))

        # Move according to the requested (and validated) move!

        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
