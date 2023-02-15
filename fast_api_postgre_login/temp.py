import string
import secrets
import hashlib

alphabet = string.ascii_letters + string.digits
token = ''.join(secrets.choice(alphabet) for i in range(32))
username = 'batuhanygt'


hashed_token = hashlib.sha256((token+username).encode()).hexdigest()
hashed_username = hashlib.sha256(username.encode()).hexdigest()

hasher_username2 = hashlib.sha256(username.encode()).hexdigest()

print("token : ",hashed_token)

print("username : ",hashed_username)

print("username 2 : ",hasher_username2)