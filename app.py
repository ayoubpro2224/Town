from flask import Flask, request, send_file
import io
import struct

app = Flask(__name__)

# دالة توليد الجدول كما في hash.cpp
def generate_hash_table(length, seed):
    table = bytearray(727)
    i = 0
    hash_val = seed
    # محاكاة منطق MurmurHash2 للقيم (كما في كود C)
    m = 0x5bd1e995
    while i < 727:
        # هذه محاكاة منطقية للحلقة الموجودة في الكود الأصلي
        h = hash_val
        k = (h * m) & 0xFFFFFFFF
        k = (k ^ (k >> 24)) * m
        hash_val = (k ^ (k >> 13)) * m
        hash_val = (hash_val ^ (hash_val >> 15)) & 0xFFFFFFFF
        
        # محاكاة memcpy
        chunk = hash_val.to_bytes(4, 'little')
        for j in range(4):
            if i + j < 727:
                table[i + j] = chunk[j]
        i += 4
    return table

@app.route('/', methods=['POST'])
def decrypt():
    if 'file' not in request.files:
        return "لا يوجد ملف مرفوع"
    
    file = request.files['file']
    raw_data = bytearray(file.read())
    
    # 1. استخراج الـ Header (8 بايت كما في data.h)
    # TOWNSHIP_XML_HEADER
    header = raw_data[:8]
    # قراءة hash_seed (البايتات 4 إلى 8)
    _, _, hash_seed = struct.unpack('<BI I', header) 
    
    # 2. البيانات الفعلية (بعد 8 بايت)
    body_data = raw_data[8:]
    
    # 3. توليد الجدول (بناءً على البذرة)
    table = generate_hash_table(727, hash_seed + 4)
    
    # 4. فك التشفير التراكمي (Delta Decoding + XOR)
    size = len(body_data)
    for i in range(size):
        j = i % 727
        # عكس عملية التراكم (C: -= تصبح في الفك +=)
        if i > 0:
            body_data[i] = (body_data[i] + body_data[i-1]) & 0xFF
        # عكس الـ XOR (هو نفسه)
        body_data[i] = (body_data[i] ^ table[j]) & 0xFF
        
    return send_file(io.BytesIO(body_data), download_name="decoded.xml", mimetype="application/xml")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
