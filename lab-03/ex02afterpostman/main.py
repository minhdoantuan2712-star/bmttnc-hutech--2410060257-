import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import uic
from rsa_cipher import RSACipher

class RSAApp(QDialog):
    def __init__(self):
        super().__init__()
        
        # Đường dẫn tới file .ui trong thư mục ui/
        ui_path = os.path.join(os.path.dirname(__file__), 'ui', 'rsa.ui')
        uic.loadUi(ui_path, self)

        # Khởi tạo đối tượng thuật toán RSA
        self.rsa_cipher = RSACipher()

        # Kết nối các nút bấm với hàm xử lý
        self.btnGenerate.clicked.connect(self.handle_generate_keys)
        self.btnEncrypt.clicked.connect(self.handle_encrypt)
        self.btnDecrypt.clicked.connect(self.handle_decrypt)
        self.btnSign.clicked.connect(self.handle_sign)
        self.btnVerify.clicked.connect(self.handle_verify)

    # 1. Sự kiện nút Tạo Khóa (btnGenerate)
    def handle_generate_keys(self):
        try:
            pub_pem, priv_pem = self.rsa_cipher.generate_keys(1024)
            
            # Nếu trong UI của bạn có khung hiển thị khóa (txtPublicKey, txtPrivateKey)
            if hasattr(self, 'txtPublicKey'):
                self.txtPublicKey.setText(pub_pem)
            if hasattr(self, 'txtPrivateKey'):
                self.txtPrivateKey.setText(priv_pem)
                
            QMessageBox.information(self, "Thông báo", "Tạo cặp khóa RSA (1024 bits) thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tạo khóa: {str(e)}")

    # 2. Sự kiện nút Mã hóa (btnEncrypt)
    def handle_encrypt(self):
        plain_text = self.txtPlaintext.toPlainText().strip()
        if not plain_text:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập nội dung vào khung txtPlaintext!")
            return
        
        try:
            cipher_b64 = self.rsa_cipher.encrypt(plain_text)
            self.txtResult.setText(cipher_b64)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Mã hóa", str(e))

    # 3. Sự kiện nút Giải mã (btnDecrypt)
    def handle_decrypt(self):
        cipher_text = self.txtResult.toPlainText().strip()
        if not cipher_text:
            # Nếu txtResult trống, thử lấy từ txtPlaintext
            cipher_text = self.txtPlaintext.toPlainText().strip()
            
        if not cipher_text:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập bản mã để giải mã!")
            return

        try:
            decrypted_text = self.rsa_cipher.decrypt(cipher_text)
            self.txtResult.setText(decrypted_text)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Giải mã", f"Giải mã thất bại: {str(e)}")

    # 4. Sự kiện nút Ký số (btnSign)
    def handle_sign(self):
        info_text = self.txtInfo.toPlainText().strip()
        if not info_text:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập thông tin cần ký vào txtInfo!")
            return

        try:
            signature = self.rsa_cipher.sign(info_text)
            self.txtSignature.setText(signature)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Ký số", str(e))

    # 5. Sự kiện nút Kiểm tra chữ ký (btnVerify)
    def handle_verify(self):
        info_text = self.txtInfo.toPlainText().strip()
        signature_text = self.txtSignature.toPlainText().strip()

        if not info_text or not signature_text:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ thông tin (txtInfo) và chữ ký (txtSignature)!")
            return

        try:
            is_valid = self.rsa_cipher.verify(info_text, signature_text)
            if is_valid:
                QMessageBox.information(self, "Xác thực chữ ký", " Chữ ký HỢP LỆ! Thông tin chưa bị thay đổi.")
            else:
                QMessageBox.warning(self, "Xác thực chữ ký", " Chữ ký KHÔNG HỢP LỆ! Thông tin hoặc chữ ký đã bị thay đổi.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Xác thực", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSAApp()
    window.show()
    sys.exit(app.exec_())