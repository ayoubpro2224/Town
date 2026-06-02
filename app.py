from flask import Flask, request, send_file
import ctypes
import tempfile
import os

app = Flask(__name__)

lib = ctypes.CDLL("./libdecodexmldyluc1.so")

decode = getattr(lib, "_Z6decodePKcS0_")
decode.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
decode.restype = ctypes.c_bool

@app.route("/")
def home():
    return """
    <h2>Township Decoder Online</h2>

    <form action="/decode" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">Decode</button>
    </form>
    """

@app.route("/decode", methods=["POST"])
def decode_file():

    if "file" not in request.files:
        return "No file"

    uploaded = request.files["file"]

    fd1, input_path = tempfile.mkstemp()
    os.close(fd1)

    uploaded.save(input_path)

    output_path = input_path + "_dec.xml"

    ok = decode(
        input_path.encode(),
        output_path.encode()
    )

    if not ok:
        return "Decode failed"

    if not os.path.exists(output_path):
        return "Output file not found"

    return send_file(
        output_path,
        as_attachment=True,
        download_name="mGameInfo-dec.xml"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
