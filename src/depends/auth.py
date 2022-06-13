from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

auth_username = 'user'
auth_password = 'pass'

def set_valid_credentials(user, pw):
    global auth_username, auth_password
    auth_username = user
    auth_password = pw

def verify_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if not auth_username:
        return 'anonymous'
    if auth_username != credentials.username or auth_password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
