from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_password_hashing():
    password = "admincti123"
    hashed = pwd_context.hash(password)
    print(f"Hashed password: {hashed}")

    # Verify correct password
    is_correct = pwd_context.verify(password, hashed)
    print(f"Verification of correct password: {is_correct}")

    # Verify incorrect password
    is_incorrect = pwd_context.verify("wrongpassword", hashed)
    print(f"Verification of incorrect password: {is_incorrect}")

if __name__ == "__main__":
    test_password_hashing()
