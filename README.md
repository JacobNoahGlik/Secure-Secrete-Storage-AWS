# Secure-Secrete-Storage-AWS
Securely store any secretes or tokens in your code (thats running on AWS) using AWS's KMS system **Python**

<br>

## secrete.py
Using the 7 steps and x functions in the `secrete.py` file you should be able to securely store and access secretes and tokens directly in your code
1. Generate `Fernet key`
2. Encrypt `api token / secrete`
3. Write encrypted `api token / secrete` to file
4. Save the `Fernet key` to `KMS` (AWS's Key Management Service)
5. Get the `Fernet key` from `KMS`
6. Get the encrypted `api token / secrete` from the file
7. Decrypt the `api token / secrete` for use in code
