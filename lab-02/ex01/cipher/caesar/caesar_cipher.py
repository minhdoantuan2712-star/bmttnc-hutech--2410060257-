from cipher.caesar.alphabet import ALPHABET

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET

    def encrypt_text(self, text: str, key: int) -> str:
        alphabet_len = len(self.alphabet)
        text = text.upper()
        encrypted_chars = []
        
        for letter in text:
            if letter in self.alphabet:
                letter_index = self.alphabet.index(letter)
                output_index = (letter_index + key) % alphabet_len
                output_letter = self.alphabet[output_index]
                encrypted_chars.append(output_letter)
            else:
                encrypted_chars.append(letter)
                
        return "".join(encrypted_chars)

    def decrypt_text(self, text: str, key: int) -> str:
        alphabet_len = len(self.alphabet)
        text = text.upper()
        decrypted_chars = []
        
        for letter in text:
            if letter in self.alphabet:
                letter_index = self.alphabet.index(letter)
                output_index = (letter_index - key) % alphabet_len
                output_letter = self.alphabet[output_index]
                decrypted_chars.append(output_letter)
            else:
                decrypted_chars.append(letter)
                
        return "".join(decrypted_chars)