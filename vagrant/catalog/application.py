from flask import Flask
app = Flask(__name__)


@app.route('/')
def home():
    return 'This is the first step!!'



if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)