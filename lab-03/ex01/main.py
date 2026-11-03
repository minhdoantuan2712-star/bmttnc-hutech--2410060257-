import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import uic
from caesar_cipher import CaesarCipher

class CaesarApp(QDialog):
    def __init__(self):
        super().__init__()
        
        # 1. Nạp trực tiếp file caesar.ui
        ui_path = os.path.join(os.path.dirname(__file__), "ui", "caesar.ui")
        if not os.path.exists(ui_path):
            ui_path = os.path.join(os.path.dirname(__file__), "caesar.ui")

        uic.loadUi(ui_path, self)

        # 2. Khởi tạo thuật toán
        self.cipher = CaesarCipher()

        # 3. Kết nối nút bấm theo objectName đã chuẩn hóa ở Bước 1
        self.btnEncrypt.clicked.connect(self.handle_encrypt)
        self.btnDecrypt.clicked.connect(self.handle_decrypt)

    def get_key(self):
        """Lấy khóa từ ô txtKey"""
        key_str = self.txtKey.text().strip()
        if not key_str:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập khóa (Key)!")
            return None
        try:
            return int(key_str)
        except ValueError:
            QMessageBox.critical(self, "Lỗi", "Khóa (Key) phải là một số nguyên!")
            return None

    def handle_encrypt(self):
        key = self.get_key()
        if key is not None:
            plain_text = self.txtPlainText.toPlainText()
            if not plain_text.strip():
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập văn bản cần mã hóa!")
                return
            
            result = self.cipher.encrypt_text(plain_text, key)
            self.txtResult.setPlainText(result)

    def handle_decrypt(self):
        key = self.get_key()
        if key is not None:
            # Lấy văn bản mã hóa từ ô PlainText (hoặc ô CipherText)
            cipher_text = self.txtPlainText.toPlainText()
            if not cipher_text.strip():
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập văn bản cần giải mã!")
                return
                
            result = self.cipher.decrypt_text(cipher_text, key)
            self.txtResult.setPlainText(result)

if __name__ == "__main__":
    # Tự động điều chỉnh tỉ lệ hiển thị theo màn hình Windows (Fix lỗi bị bé/méo)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    window = CaesarApp()
    window.show()
    sys.exit(app.exec_())