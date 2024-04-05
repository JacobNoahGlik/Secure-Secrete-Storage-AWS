import boto3
from cryptography.fernet import Fernet

# Encrypt GitHub API token
def encrypt_token(token: str, fernet_key: bytes) -> bytes:
    fernet: Fernet = Fernet(fernet_key)
    encrypted_token: bytes = fernet.encrypt(token.encode())
    return encrypted_token

# Save encrypted token bytes to a file
def save_to_file(data: bytes, filename: str) -> None:
    with open(filename, 'wb') as file:
        file.write(data)

# Generate Fernet key
def generate_fernet_key() -> bytes:
    return Fernet.generate_key()

# Store Fernet key securely in AWS KMS
def store_key_in_kms(key_bytes: bytes) -> str:
    kms_client: boto3.client = boto3.client('kms')
    response: dict[str, str] = kms_client.import_key_material(
        KeyId='alias/your-key-alias',  # Replace with your KMS key alias
        ImportToken=key_bytes,
        # Specify KeySpec if you want to specify a specific key specification, default is AES_256
    )
    return response

# Retrieve Fernet key from AWS KMS
def retrieve_key_from_kms() -> bytes:
    kms_client: boto3.client = boto3.client('kms')
    response: dict[str, str] = kms_client.get_parameters(
        Names=['alias/your-key-alias'],  # Replace with your KMS key alias
        WithDecryption=True
    )
    key_bytes: bytes = response['Parameters'][0]['Value']
    return key_bytes

# Decrypt GitHub API token
def decrypt_token(encrypted_token: bytes, fernet_key: bytes) -> str:
    fernet: Fernet = Fernet(fernet_key)
    decrypted_token: str = fernet.decrypt(encrypted_token)
    return decrypted_token.decode()

# 1. Generate Fernet key
fernet_key: bytes = generate_fernet_key()

# 2. Encrypt GitHub API token
github_api_token: str = 'YOUR_GITHUB_API_TOKEN'
encrypted_token: bytes = encrypt_token(github_api_token, fernet_key)

# 3. Save encrypted token bytes to a file
save_to_file(encrypted_token, 'encrypted_token.bin') # returns None

# 4. Store Fernet key securely in AWS KMS
store_key_in_kms(fernet_key) # returns response from kms

# 5. Retrieve Fernet key from AWS KMS
retrieved_key_bytes: bytes = retrieve_key_from_kms()
retrieved_fernet_key: bytes = Fernet(retrieved_key_bytes)

# 6. Get the encrypted GitHub token from the file
with open('encrypted_token.bin', 'rb') as file:
    encrypted_token_from_file: bytes = file.read()

# 7. Decrypt the GitHub token
decrypted_token: str = decrypt_token(encrypted_token_from_file, retrieved_fernet_key)
print("Decrypted GitHub API token:", decrypted_token)
