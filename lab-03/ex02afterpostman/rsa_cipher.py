import rsa
import base64

class RSACipher:
    def __init__(self):
        self.public_key = None
        self.private_key = None

    def generate_keys(self, key_size=1024):
        """Sinh cặp khóa RSA"""
        (self.public_key, self.private_key) = rsa.newkeys(key_size)
        pub_pem = self.public_key.save_pkcs1().decode('utf-8')
        priv_pem = self.private_key.save_pkcs1().decode('utf-8')
        return pub_pem, priv_pem

    def encrypt(self, plain_text: str) -> str:
        """Mã hóa chuỗi văn bản bằng Public Key"""
        if not self.public_key:
            raise ValueError("Chưa có Public Key. Hãy tạo khóa trước!")
        encrypted_bytes = rsa.encrypt(plain_text.encode('utf-8'), self.public_key)
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decrypt(self, cipher_text_b64: str) -> str:
        """Giải mã chuỗi Base64 bằng Private Key"""
        if not self.private_key:
            raise ValueError("Chưa có Private Key. Hãy tạo khóa trước!")
        cipher_bytes = base64.b64decode(cipher_text_b64.encode('utf-8'))
        decrypted_bytes = rsa.decrypt(cipher_bytes, self.private_key)
        return decrypted_bytes.decode('utf-8')

    def sign(self, message: str) -> str:
        """Ký số thông điệp bằng Private Key (dùng thuật toán băm SHA-256)"""
        if not self.private_key:
            raise ValueError("Chưa có Private Key để ký số!")
        signature_bytes = rsa.sign(message.encode('utf-8'), self.private_key, 'SHA-256')
        return base64.b64encode(signature_bytes).decode('utf-8')

    def verify(self, message: str, signature_b64: str) -> bool:
        """Kiểm tra chữ ký số bằng Public Key"""
        if not self.public_key:
            raise ValueError("Chưa có Public Key để xác minh!")
        try:
            signature_bytes = base64.b64decode(signature_b64.encode('utf-8'))
            rsa.verify(message.encode('utf-8'), signature_bytes, self.public_key)
            return True
        except rsa.VerificationError:
            return False