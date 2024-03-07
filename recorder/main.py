import time
import uuid
import uvicorn
from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager

from config import RecorderConfig
from services import MockCapture
from models import *

conf = RecorderConfig.from_environ(os.environ)
capture = MockCapture(conf.source.path, int(conf.source.fps), int(conf.snapshots.histsize))


@asynccontextmanager
async def lifespan(_: FastAPI):
    capture.start()
    yield
    capture.stop()

api = FastAPI(lifespan=lifespan)


def create_snapshot_bg(path: str, meta: SnapshotMeta):
    os.mkdir(path)
    capture.save(path)
    meta.save(path)


@api.post("/api/snapshot")
async def action(req: SnapshotReq, bg: BackgroundTasks):
    resp = SnapshotResp(sid=uuid.uuid4(), ts=int(time.time() * 1000))
    meta = SnapshotMeta(values=req, meta=resp)
    path = os.path.join(conf.snapshots.basepath, str(resp.sid))
    bg.add_task(create_snapshot_bg, path, meta)
    return resp


if __name__ == "__main__":
    uvicorn.run(api, host=conf.listener.host, port=int(conf.listener.port))
