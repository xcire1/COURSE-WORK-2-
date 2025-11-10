import bcrypt
USER_DATA_FILE = "users.txt"
def hash_password(plain_text_password):
    def verify_password():
        test_password = "SecurePassword123"
        hashed = hash_password(test_password)
        print(f"Original Password: {test_password}")
        print(f"Hashed password: {hashed}")
        print(f"Hash length: {len(hashed)} characters")

        is_valid = verify_password(test_password, hashed)
        print(f"Password verification result: {is_valid}")
        is_valid_wrong = verify_password("WrongPassword", hashed)
        print(f"Wrong password verification result: {is_valid_wrong}")
    # Generate a salt and hash the password