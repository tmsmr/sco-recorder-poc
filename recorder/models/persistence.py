import os

from pydantic import BaseModel
from .api import SnapshotReq, SnapshotResp


class SnapshotMeta(BaseModel):
    values: SnapshotReq
    meta: SnapshotResp

    def save(self, folder):
        with open(os.path.join(folder, 'meta.json'), 'w') as f:
            f.write(str(self.model_dump_json()))
