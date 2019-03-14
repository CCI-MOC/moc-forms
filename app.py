import flask

app = flask.Flask(__name__)


@app.route('/signup')
def signup():
    return flask.render_template('signup.html')


if __name__ == '__main__':
    app.run(port=5001)
