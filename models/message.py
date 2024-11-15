from pydantic import BaseModel
from typing import Optional

class Message(BaseModel):
    msg: str
    topic_name: str
    key: Optional[str] = None