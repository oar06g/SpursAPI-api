from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA512
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os
import hmac
import hashlib

class Encryption:  # Shizuko Platform Encryption
  def __init__(self, password: str):
    self.password = password.encode()
    self.salt = self.generate_salt_from_password(self.password)
    self.key = self.derive_key(self.password, self.salt)
    self.hmac_key = self.key[:16]
    self.encryption_key = self.key[16:]

  def generate_salt_from_password(self, password: bytes) -> bytes:
    return hashlib.sha256(password).digest()

  def derive_key(self, password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
      algorithm=SHA512(),
      length=32,
      salt=salt,
      iterations=200000,
      backend=default_backend(),
    )
    return kdf.derive(password)

  def encrypt(self, message: str) -> str:
    iv = os.urandom(16)
    cipher = Cipher(
      algorithms.AES(self.encryption_key),
      modes.CFB(iv),
      backend=default_backend(),
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()

    signature = hmac.new(self.hmac_key, ciphertext, digestmod="sha256").digest()

    encrypted_message = base64.b64encode(iv + signature + ciphertext).decode()
    return encrypted_message

  def decrypt(self, encrypted_base64: str) -> str:
    encrypted_data = base64.b64decode(encrypted_base64.encode())

    iv = encrypted_data[:16]
    signature = encrypted_data[16:48]
    ciphertext = encrypted_data[48:]

    expected_signature = hmac.new(
      self.hmac_key, ciphertext, digestmod="sha256"
    ).digest()
    if not hmac.compare_digest(signature, expected_signature):
      raise ValueError("Signature mismatch! Message integrity compromised.")

    cipher = Cipher(
      algorithms.AES(self.encryption_key),
      modes.CFB(iv),
      backend=default_backend(),
    )
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext.decode()

# مثال على الاستخدام
# password = "_BIM8o0oRI4uttmSyp67VnQZQp7-megO7r48Uzi8Apo="  # كلمة المرور
# tpe = TPE(password)

# # تشفير رسالة
# encrypted = tpe.encrypt("Sensitive Data Here!")
# print("Encrypted:", encrypted)

# # فك تشفير الرسالة
# try:
#     decrypted = tpe.decrypt(encrypted)
#     print("Decrypted:", decrypted)
# except ValueError as e:
#     print("Decryption failed:", e)