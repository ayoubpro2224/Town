from flask import Flask
import os
import ctypes

app = Flask(__name__)

BASE = os.path.dirname(os.path.abspath(__file__))
SO_FILE = os.path.join(BASE, "libdecodexmldyluc1.so")

print("SO PATH =", SO_FILE)
print("EXISTS =", os.path.exists(SO_FILE))

try:
    lib = ctypes.CDLL(SO_FILE)
    print("LIBRARY LOADED OK")
except Exception as e:
    print("LOAD ERROR =", e)

@app.route("/")
def home():
    return "Township Decoder Online"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
