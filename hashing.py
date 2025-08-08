from passlib.context import CryptContext

# Password hashing context using bcrypt
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    """
    Utility class for hashing and verifying passwords using bcrypt.
    """

    @staticmethod
    def bcrypt(password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.

        Args:
            plain_password (str): The plain password to verify.
            hashed_password (str): The hashed password.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return pwd_cxt.verify(plain_password, hashed_password)