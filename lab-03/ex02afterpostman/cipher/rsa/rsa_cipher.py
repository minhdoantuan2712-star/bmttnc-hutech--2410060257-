import rsa
import base64

class RSACipher:
    def __init__(self):
        self.public_key = None
        self.private_key = None

    def generate_keys(self, key_size=1024):
        """Tạo cặp khóa RSA mới (mặc định 1024 bits)"""
        (self.public_key, self.private_key) = rsa.newkeys(key_size)
        pub_pem = self.public_key.save_pkcs1().decode('utf-8')
        priv_pem = self.private_key.save_pkcs1().decode('utf-8')
        return pub_pem, priv_pem

    def load_keys(self):
        """Trả về cặp khóa dạng đối tượng RSA hiện tại"""
        return self.private_key, self.public_key

    def load_keys_from_pem(self, pub_pem_str, priv_pem_str):
        """Nạp khóa Public và Private từ chuỗi hoặc bytes PEM"""
        if pub_pem_str:
            if isinstance(pub_pem_str, str):
                pub_pem_str = pub_pem_str.encode('utf-8')
            self.public_key = rsa.PublicKey.load_pkcs1(pub_pem_str)
            
        if priv_pem_str:
            if isinstance(priv_pem_str, str):
                priv_pem_str = priv_pem_str.encode('utf-8')
            self.private_key = rsa.PrivateKey.load_pkcs1(priv_pem_str)

    def encrypt(self, plain_text, pub_key_pem=None) -> str:
        """Mã hóa văn bản plain_text bằng Public Key, trả về chuỗi Base64"""
        if pub_key_pem:
            if isinstance(pub_key_pem, (str, bytes)):
                key_bytes = pub_key_pem.encode('utf-8') if isinstance(pub_key_pem, str) else pub_key_pem
                pub_key = rsa.PublicKey.load_pkcs1(key_bytes)
            else:
                pub_key = pub_key_pem
        elif self.public_key:
            pub_key = self.public_key
        else:
            raise ValueError("Chưa có Public Key để mã hóa.")

        # Đảm bảo plain_text là bytes trước khi encrypt
        data_bytes = plain_text.encode('utf-8') if isinstance(plain_text, str) else plain_text
        encrypted_bytes = rsa.encrypt(data_bytes, pub_key)
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decrypt(self, cipher_text_base64, priv_key_pem=None) -> str:
        """Giải mã chuỗi Base64 bằng Private Key, trả về bản rõ"""
        if priv_key_pem:
            if isinstance(priv_key_pem, (str, bytes)):
                key_bytes = priv_key_pem.encode('utf-8') if isinstance(priv_key_pem, str) else priv_key_pem
                priv_key = rsa.PrivateKey.load_pkcs1(key_bytes)
            else:
                priv_key = priv_key_pem
        elif self.private_key:
            priv_key = self.private_key
        else:
            raise ValueError("Chưa có Private Key để giải mã.")

        # Giải mã Base64 rồi giải mã RSA
        b64_bytes = cipher_text_base64.encode('utf-8') if isinstance(cipher_text_base64, str) else cipher_text_base64
        cipher_bytes = base64.b64decode(b64_bytes)
        decrypted_bytes = rsa.decrypt(cipher_bytes, priv_key)
        return decrypted_bytes.decode('utf-8')

    def sign(self, message, priv_key=None) -> str:
        """Ký thông điệp bằng Private Key, trả về chuỗi chữ ký Base64"""
        key = priv_key or self.private_key
        if not key:
            raise ValueError("Chưa có Private Key để ký.")
        if isinstance(key, (str, bytes)):
            key_bytes = key.encode('utf-8') if isinstance(key, str) else key
            key = rsa.PrivateKey.load_pkcs1(key_bytes)
            
        msg_bytes = message.encode('utf-8') if isinstance(message, str) else message
        signature_bytes = rsa.sign(msg_bytes, key, 'SHA-1')
        return base64.b64encode(signature_bytes).decode('utf-8')

    def verify(self, message, signature_base64, pub_key=None) -> bool:
        """Xác minh chữ ký Base64 bằng Public Key"""
        key = pub_key or self.public_key
        if not key:
            raise ValueError("Chưa có Public Key để xác minh.")
        if isinstance(key, (str, bytes)):
            key_bytes = key.encode('utf-8') if isinstance(key, str) else key
            key = rsa.PublicKey.load_pkcs1(key_bytes)
            
        msg_bytes = message.encode('utf-8') if isinstance(message, str) else message
        sig_b64_bytes = signature_base64.encode('utf-8') if isinstance(signature_base64, str) else signature_base64
        signature_bytes = base64.b64decode(sig_b64_bytes)
        
        try:
            rsa.verify(msg_bytes, signature_bytes, key)
            return True
        except rsa.VerificationError:
            return False