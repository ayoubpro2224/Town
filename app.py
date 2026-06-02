from flask import Flask, request, send_file
import ctypes
import tempfile
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("Current directory:", BASE_DIR)
print("Files:", os.listdir(BASE_DIR))

SO_FILE = os.path.join(BASE_DIR, "libdecodexmldyluc1.so")

lib = ctypes.CDLL(SO_FILE)

decode = getattr(lib, "_Z6decodePKcS0_")
decode.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
decode.restype = ctypes.c_bool


@app.route("/")
def home():
    return """
    <html>
    <body>
        <h2>Township Decoder Online</h2>

        <form action="/decode" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Decode</button>
        </form>

    </body>
    </html>
    """


@app.route("/decode", methods=["POST"])
def decode_file():

    if "file" not in request.files:
        return "No file uploaded"

    uploaded = request.files["file"]

    fd, input_path = tempfile.mkstemp()
    os.close(fd)

    uploaded.save(input_path)

    output_path = input_path + "_dec.xml"

    try:

        result = decode(
            input_path.encode("utf-8"),
            output_path.encode("utf-8")
        )

        if not result:
            return "Decode failed"

        if not os.path.exists(output_path):
            return "Output file was not generated"

        return send_file(
            output_path,
            as_attachment=True,
            download_name="mGameInfo-dec.xml"
        )

    except Exception as e:
        return f"ERROR: {str(e)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
