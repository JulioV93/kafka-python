from pydantic import BaseModel
from typing import Optional

class Topic(BaseModel):
    name: str
    max_bytes: Optional[int] = 1048576
    partitions: Optional[int] = 6
    replication_factor: Optional[int] = 1
    cleanup_policy: Optional[str] = "delete"
    retention_ms: Optional[int] = 86400000
    max_message_bytes: Optional[int] = 1048576