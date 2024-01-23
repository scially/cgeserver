from typing import Annotated, Generator
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from app.db.engine import engine

def get_db() -> Generator:
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_db)]