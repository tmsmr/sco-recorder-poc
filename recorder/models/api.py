from uuid import UUID

from pydantic import BaseModel


class RecordReq(BaseModel):
    weight: float


class RecordResp(BaseModel):
    rid: UUID
    ts: int
    frames: int
