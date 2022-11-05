from flask import Flask, render_template

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
	return 'Hello, World!'

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html', name="testing")

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
