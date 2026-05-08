import bcrypt

def hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    # bcrypt limits passwords to 72 bytes; truncate to avoid ValueError
    if len(pwd_bytes) > 72:
        pwd_bytes = pwd_bytes[:72]
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

def verify(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    if len(password_byte_enc) > 72:
        password_byte_enc = password_byte_enc[:72]
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)
