# About
This tool let people save their passwords in a local encrypted database. The passwords are easily accessible by any device that can open and read .db files.

# Encryption tecnhiques
The tool uses the following encryption tecnhiques to safely encrypt the passwords based on a user-provided master password.

## PBKDF2 (Password-Based Key Derivation Function 2)
Used to derive a strong 256-bit encryption key from the user's password and a random salt, with 1,000,000 iterations for enhanced brute-force resistance.

## Salted Key Derivation
A securely generated random salt ensures that identical passwords produce different keys, protecting against rainbow table attacks.

## AES (Advanced Encryption Standard) in CBC Mode
Data is encrypted using AES-256 in CBC (Cipher Block Chaining) mode. Each encryption uses a new, random initialization vector (IV) for security.

## PKCS7 Padding
Applied to plaintext before encryption to align it with AES's 16-byte block size requirement.

# Usage
The tool offers following 4 functions (+ exit):

<img width="784" height="273" alt="OPTIONS MENU" src="https://github.com/user-attachments/assets/3bbce19d-7d16-4172-81f7-a96774cca139" />

Every function requires a master password the user must provide, without it it's impossible to decrypt the database's data. The master password is not stored at any time.
