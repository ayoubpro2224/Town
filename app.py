from flask import Flask, request, send_file
import io
import struct

app = Flask(__name__)

# دالة توليد الجدول بناءً على كود الـ C الأصلي
def generate_hash_table(length, seed):
    table = bytearray(727)
    i = 0
    hash_val = seed
    m = 0x5bd1e995
    # الحلقة الأساسية لتوليد الجدول
    while i < 727:
        k = (hash_val * m) & 0xFFFFFFFF
        k = (k ^ (k >> 24)) * m
        hash_val = (k ^ (k >> 13)) * m
        hash_val = (hash_val ^ (hash_val >> 15)) & 0xFFFFFFFF
        
        chunk = hash_val.to_bytes(4, 'little')
        for j in range(4):
            if i + j < 727:
                table[i + j] = chunk[j]
        i += 4
    return table

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "لم يتم رفع ملف"
        
        file = request.files['file']
        raw_data = bytearray(file.read())
        
        # 1. استخراج الـ Header (8 بايت كما في ملف data.h)
        # TOWNSHIP_XML_HEADER
        header = raw_data[:8]
        # قراءة hash_seed (البايتات 4 إلى 8)
        # هيكل الملف: type(1) + hash_length(3) + hash_seed(4)
        _, _, hash_seed = struct.unpack('<BI I', header)
        
        # 2. البيانات الفعلية (بعد 8 بايت)
        body_data = raw_data[8:]
        
        # 3. توليد الجدول باستخدام البذرة الموجودة في الـ Header
        table = generate_hash_table(727, hash_seed + 4)
        
        # 4. فك التشفير التراكمي (Delta Decoding + XOR)
        # هذا يطابق تماماً منطق decode.cpp
        size = len(body_data)
        for i in range(size):
            j = i % 727
            # عملية Delta Decoding (عكس التشفير)
            if i > 0:
                body_data[i] = (body_data[i] + body_data[i-1]) & 0xFF
            # فك الـ XOR
            body_data[i] = (body_data[i] ^ table[j]) & 0xFF
            
        return send_file(io.BytesIO(body_data), download_name="decoded.xml", mimetype="application/xml")
    
    # صفحة الرفع (HTML)
    return '''
    <!doctype html>
    <html dir="rtl">
    <head><meta charset="utf-8"><title>Ayoubtool Decoder</title></head>
    <body>
      <h1>أداة فك تشفير Township</h1>
      <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value="فك التشفير الآن">
      </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
