import time
import uuid
import uvicorn
from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager

from config import RecorderConfig
from services import MockCapture
from models import *

conf = RecorderConfig.from_environ(os.environ)
capture = MockCapture(conf.source.path, int(conf.source.fps), int(conf.records.histsize))


@asynccontextmanager
async def lifespan(_: FastAPI):
    capture.start()
    yield
    capture.stop()

api = FastAPI(lifespan=lifespan)


def create_record_bg(path: str, meta: Record):
    os.mkdir(path)
    capture.save(path)
    meta.save(path)


@api.post("/api/record")
async def action(req: RecordReq, bg: BackgroundTasks):
    resp = RecordResp(rid=uuid.uuid4(), ts=int(time.time() * 1000), frames=conf.records.histsize)
    record = Record(values=req, meta=resp)
    path = os.path.join(conf.records.basepath, str(resp.rid))
    bg.add_task(create_record_bg, path, record)
    return resp


if __name__ == "__main__":
    uvicorn.run(api, host=conf.listener.host, port=int(conf.listener.port))
