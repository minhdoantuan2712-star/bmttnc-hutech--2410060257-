from flask import Flask, request, jsonify
from cipher.rsa import RSACipher

app = Flask(__name__)

# RSA CIPHER ALGORITHM
rsa_cipher = RSACipher()

@app.route('/api/rsa/generate_keys', methods=['GET'])
def rsa_generate_keys():
    pub_pem, priv_pem = rsa_cipher.generate_keys()
    return jsonify({
        'message': 'Keys generated successfully',
        'public_key': pub_pem,
        'private_key': priv_pem
    })

@app.route('/api/rsa/encrypt', methods=['POST'])
def rsa_encrypt():
    data = request.json
    message = data['message']
    key_type = data.get('key_type', 'public')
    
    private_key, public_key = rsa_cipher.load_keys()
    key = public_key if key_type == 'public' else private_key
    
    # encrypt() trả về chuỗi str (Base64) -> Không dùng .hex()
    encrypted_message = rsa_cipher.encrypt(message, key)
    return jsonify({'encrypted_message': encrypted_message})

@app.route('/api/rsa/decrypt', methods=['POST'])
def rsa_decrypt():
    data = request.json
    ciphertext_base64 = data['ciphertext']
    key_type = data.get('key_type', 'private')
    
    private_key, public_key = rsa_cipher.load_keys()
    key = private_key if key_type == 'private' else public_key
    
    decrypted_message = rsa_cipher.decrypt(ciphertext_base64, key)
    return jsonify({'decrypted_message': decrypted_message})

@app.route('/api/rsa/sign', methods=['POST'])
def rsa_sign_message():
    data = request.json
    message = data['message']
    private_key, _ = rsa_cipher.load_keys()
    
    # sign() trả về chuỗi str (Base64) -> Không dùng .hex()
    signature = rsa_cipher.sign(message, private_key)
    return jsonify({'signature': signature})

@app.route('/api/rsa/verify', methods=['POST'])
def rsa_verify_signature():
    data = request.json
    message = data['message']
    signature = data['signature']
    _, public_key = rsa_cipher.load_keys()
    
    is_verified = rsa_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)