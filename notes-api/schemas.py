from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None 

    model_config = ConfigDict(from_attributes=True) #enables object read for pydantic, it converts note object into json/dict automatically and read from it