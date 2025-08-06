from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)