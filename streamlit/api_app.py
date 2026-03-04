from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import json
from pathlib import Path
from datetime import datetime

app = FastAPI()

JOBS_FILE = Path("active_jobs.json")
COMPLETED_FILE = Path("completed_jobs.json")

def _read_json_list(path: Path):
    if not path.exists():
        return []
    raw = path.read_bytes()
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            txt = raw.decode(enc)
            if not txt.strip():
                return []
            data = json.loads(txt)
            if not isinstance(data, list):
                return []
            # korjaa utf-8:ksi jos oli väärä enkoodaus
            if enc != "utf-8":
                _write_json_list(path, data)
            return data
        except Exception:
            continue
    return []

def _write_json_list(path: Path, data: list):
    path.write_text(
        json.dumps(data, indent=4, ensure_ascii=False),
        encoding="utf-8",
        newline="\n"
    )

def load_active_jobs():
    return _read_json_list(JOBS_FILE)

def save_active_jobs(jobs):
    _write_json_list(JOBS_FILE, jobs)

def load_completed_jobs():
    return _read_json_list(COMPLETED_FILE)

def save_completed_jobs(jobs):
    _write_json_list(COMPLETED_FILE, jobs)

@app.post("/jobs")
async def receive_job(request: Request):
    job = await request.json()

    # ignoraa ping-testit
    if job.get("ping") is True:
        return {"status": "ok", "ignored": True}

    jobs = load_active_jobs()
    jobs.append(job)
    save_active_jobs(jobs)
    return {"status": "ok", "count": len(jobs)}

class CompletePayload(BaseModel):
    id: str
    notes: str | None = ""
    completed_by: str | None = None  # mekaanikon nimi (valinnainen)

@app.post("/jobs/complete")
def complete_job(payload: CompletePayload):
    jobs = load_active_jobs()
    completed = load_completed_jobs()

    # etsi työ id:llä
    idx = next((i for i, j in enumerate(jobs) if str(j.get("id")) == str(payload.id)), None)
    if idx is None:
        return {"status": "not_found", "id": payload.id}

    job = jobs.pop(idx)

    # lisää kuittausmetat
    job["status"] = "completed"
    job["completed_at"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    job["notes"] = payload.notes or ""
    if payload.completed_by:
        job["completed_by"] = payload.completed_by

    completed.append(job)

    save_active_jobs(jobs)
    save_completed_jobs(completed)

    return {"status": "ok", "active_count": len(jobs), "completed_count": len(completed)}
