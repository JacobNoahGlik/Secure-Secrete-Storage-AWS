import boto3
from cryptography.fernet import Fernet

# Encrypt GitHub API token
def encrypt_token(token, fernet_key):
    fernet = Fernet(fernet_key)
    encrypted_token = fernet.encrypt(token.encode())
    return encrypted_token

# Save encrypted token bytes to a file
def save_to_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

# Generate Fernet key
def generate_fernet_key():
    return Fernet.generate_key()

# Store Fernet key securely in AWS KMS
def store_key_in_kms(key_bytes):
    kms_client = boto3.client('kms')
    response = kms_client.import_key_material(
        KeyId='alias/your-key-alias',  # Replace with your KMS key alias
        ImportToken=key_bytes,
        # Specify KeySpec if you want to specify a specific key specification, default is AES_256
    )
    return response

# Retrieve Fernet key from AWS KMS
def retrieve_key_from_kms():
    kms_client = boto3.client('kms')
    response = kms_client.get_parameters(
        Names=['alias/your-key-alias'],  # Replace with your KMS key alias
        WithDecryption=True
    )
    key_bytes = response['Parameters'][0]['Value']
    return key_bytes

# Decrypt GitHub API token
def decrypt_token(encrypted_token, fernet_key):
    fernet = Fernet(fernet_key)
    decrypted_token = fernet.decrypt(encrypted_token)
    return decrypted_token.decode()

# 1. Generate Fernet key
fernet_key = generate_fernet_key()

# 2. Encrypt GitHub API token
github_api_token = 'YOUR_GITHUB_API_TOKEN'
encrypted_token = encrypt_token(github_api_token, fernet_key)

# 3. Save encrypted token bytes to a file
save_to_file(encrypted_token, 'encrypted_token.bin')

# 4. Store Fernet key securely in AWS KMS
store_key_in_kms(fernet_key)

# 5. Retrieve Fernet key from AWS KMS
retrieved_key_bytes = retrieve_key_from_kms()
retrieved_fernet_key = Fernet(retrieved_key_bytes)

# 6. Get the encrypted GitHub token from the file
with open('encrypted_token.bin', 'rb') as file:
    encrypted_token_from_file = file.read()

# 7. Decrypt the GitHub token
decrypted_token = decrypt_token(encrypted_token_from_file, retrieved_fernet_key)
print("Decrypted GitHub API token:", decrypted_token)
