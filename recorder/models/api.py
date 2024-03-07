from uuid import UUID

from pydantic import BaseModel


class SnapshotReq(BaseModel):
    weight: float


class SnapshotResp(BaseModel):
    sid: UUID
    ts: int
