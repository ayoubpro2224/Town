from flask import Flask
import os

app = Flask(__name__)

print("FILES_IN_PROJECT =", os.listdir("/opt/render/project/src"))

@app.route("/")
def home():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
