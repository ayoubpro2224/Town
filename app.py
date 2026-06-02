from flask import Flask, request, send_file
import os
import ctypes
import tempfile

app = Flask(__name__)

@app.route("/")
def home():
    return "Township Decoder Online"

@app.route("/decode", methods=["POST"])
def decode_file():

    if "file" not in request.files:
        return {"error": "No file uploaded"}

    uploaded = request.files["file"]

    input_file = tempfile.NamedTemporaryFile(delete=False)
    uploaded.save(input_file.name)

    output_file = input_file.name + "_dec.xml"

    try:
        lib = ctypes.CDLL("./libdecodexmldyluc1.so")

        # سنحدد اسم الدالة لاحقاً
        return {"status": "library loaded"}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)