from passlib.context import CryptContext
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
hash_password=pwd_context.hash
verify_password=lambda p,h: pwd_context.verify(p,h)
