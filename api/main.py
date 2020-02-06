from flask import Flask

# start flask instance
app = Flask(__name__)

# default index route
@app.route('/')
@app.route('/index')
def index():
    return {'OK': '200'}

if __name__ == '__main__':
    app.run(host='localhost', port=3000)
