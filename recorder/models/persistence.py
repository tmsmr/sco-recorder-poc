import os

from pydantic import BaseModel
from .api import RecordReq, RecordResp


class Record(BaseModel):
    values: RecordReq
    meta: RecordResp

    def save(self, folder):
        with open(os.path.join(folder, 'meta.json'), 'w') as f:
            f.write(str(self.model_dump_json()))
