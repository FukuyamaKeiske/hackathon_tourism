# app/dependencies.py
from fastapi import Depends, HTTPException, Request


async def get_current_user(request: Request):
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=401, detail="Not authenticated")
    return request.state.user
