import bcrypt

# function to hash password
def hash_password(password: str):
    # generate a salt
    salt = bcrypt.gensalt()

    # hash the password
    hashed_password = bcrypt.hashpw(password, salt)

    return hashed_password

# verify password match
def verify_password(provided_password, hashed_password):
    return  bcrypt.checkpw(provided_password, hashed_password):


# refresh token after 7 days
