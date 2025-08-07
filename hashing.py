from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password: str) -> str:
        """
        Hash a password using bcrypt.
        :param password: The password to hash.
        :return: The hashed password.
        """
        return pwd_cxt.hash(password)

    def verify(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a hashed password against a plain password.
        :param hashed_password: The hashed password.
        :param plain_password: The plain password to verify.
        :return: True if the passwords match, False otherwise.
        """
        return pwd_cxt.verify(plain_password, hashed_password)