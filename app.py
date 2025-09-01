from flask import Flask, render_template, abort, redirect, url_for, 

app = Flask(__name__)


@app.route('/login')
def login():
    return render_template('login.html')
    


if __name__ == '__main__':
    app.run(debug=True)