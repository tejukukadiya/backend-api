import secrets
import base64

# JWT SECRET KEY
SECRET_KEY = secrets.token_urlsafe(32)  # 32 characters, safe for URLs

# JWT ALGORITHM
ALGORITHM = 'HS256'

# AES KEY (256-bit = 32 bytes, encoded safely)
raw_aes_key = secrets.token_bytes(32)  # 32 bytes
AES_KEY = base64.b64encode(raw_aes_key).decode('utf-8')  # Encode for safe storage

# IV KEY (AES block size = 16 bytes)
raw_iv = secrets.token_bytes(16)  # 16 bytes
IV_KEY = base64.b64encode(raw_iv).decode('utf-8')

# Token Expiry Time
ACCESS_TOKEN_EXPIRE_TIME = 30  # in minutes

# Print out values (optional)
print("SECRET_KEY =", SECRET_KEY)
print("ALGORITHM =", ALGORITHM)
print("AES_KEY =", AES_KEY)
print("IV_KEY =", IV_KEY)
print("ACCESS_TOKEN_EXPIRE_TIME =", ACCESS_TOKEN_EXPIRE_TIME)
