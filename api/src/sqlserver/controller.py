from fastapi import APIRouter, Depends
from typing import List

from .database import SessionLocal, get_db

from .service import SqlServerService
from .schemas.track import TrackCreate, TrackUpdate, TrackInDB

router = APIRouter()

@router.get("/v1/service_check")
def server_check(db: SessionLocal = Depends(get_db)):
    sqlserver_service = SqlServerService(db)
    return sqlserver_service.service_check()

# Load data from /tracks.json
@router.post("/v1/track/load_from_json")
def load_from_json(db: SessionLocal = Depends(get_db)):
    sqlserver_service = SqlServerService(db)
    return sqlserver_service.load_from_json()


@router.post("/v1/track", response_model=TrackInDB)
def create_track(track: TrackCreate, db: SessionLocal = Depends(get_db)):
    sqlserver_service = SqlServerService(db)
    return sqlserver_service.create_track(track)


@router.get("/v1/track", response_model=List[TrackInDB])
def get_tracks(db: SessionLocal = Depends(get_db)):
    sqlserver_service = SqlServerService(db)
    return sqlserver_service.get_tracks()


@router.get("/v1/track/{track_id}", response_model=TrackInDB)
def get_track(track_id: int, db: SessionLocal = Depends(get_db)):
    sqlserver_service = SqlServerService(db)
    return sqlserver_service.get_track(track_id)


@router.put("/v1/track/{track_id}", response_model=TrackInDB)
def update_track(track_id: int, track: TrackUpdate, db: SessionLocal = Depends(get_db)):
    sqlserver_service = SqlServerService(db)
    return sqlserver_service.update_track(track_id, track)


@router.delete("/v1/track/{track_id}")
def delete_track(track_id: int, db: SessionLocal = Depends(get_db)):
    sqlserver_service = SqlServerService(db)
    return sqlserver_service.delete_track(track_id)
