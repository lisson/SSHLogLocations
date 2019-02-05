import re
import sys
import io
from flask import Flask
import SSHLogParser


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()