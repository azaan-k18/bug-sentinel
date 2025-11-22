from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.security import create_access_token

router = APIRouter()

class TokenResp(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginReq(BaseModel):
    username: str
    password: str

# NOTE: This is a placeholder. Integrate with real user store / SSO in prod.
@router.post("/login", response_model=TokenResp)
def login(req: LoginReq):
    if req.username == "admin" and req.password == "admin":
        token = create_access_token(subject=req.username)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="invalid credentials")
