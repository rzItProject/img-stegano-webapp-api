import secrets

def generate_secret_key():
    return secrets.token_hex(32)  # Generate a 256-bit key, 32 bytes = 256 bits

# Usage
key = generate_secret_key()
print(key)
