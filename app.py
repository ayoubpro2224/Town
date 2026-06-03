from flask import Flask, request, send_file
import lz4.frame
import io

app = Flask(__name__)

def generate_table(param2, param3):
    table = bytearray(727)
    iVar3 = 0
    while iVar3 < 727:
        uVar2 = 726 - iVar3
        uVar1 = ((param3 * 0x5bd1e995 ^ (param3 * 0x5bd1e995 >> 24)) * 0x5bd1e995 ^ ((param2 ^ 4) * 0x5bd1e995)) & 0xFFFFFFFF
        uVar1 = ((uVar1 ^ (uVar1 >> 13)) * 0x5bd1e995) & 0xFFFFFFFF
        param3 = (uVar1 ^ (uVar1 >> 15)) & 0xFFFFFFFF
        if uVar2 > 2: uVar2 = 3
        
        chunk = param3.to_bytes(4, 'little')
        for k in range(uVar2 + 1):
            table[iVar3 + k] = chunk[k]
        iVar3 += uVar2 + 1
    return table

@app.route('/', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        file = request.files['file']
        data = file.read()
        
        # فك التشفير
        table = generate_table(0x1, 0x2)
        decrypted = bytearray(len(data))
        for i in range(len(data)):
            decrypted[i] = data[i] ^ table[i % 727] ^ 0x79
            
        # فك الضغط (LZ4)
        try:
            decompressed = lz4.frame.decompress(decrypted)
            return send_file(io.BytesIO(decompressed), download_name="decrypted.xml", mimetype="application/xml")
        except:
            return "خطأ في فك الضغط، ربما الترويسة تحتاج حذف!"
            
    return '''<form method="post" enctype="multipart/form-data"><input type="file" name="file"><input type="submit"></form>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
