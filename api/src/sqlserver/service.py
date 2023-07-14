import json
import pathlib
from typing import List
from sqlalchemy.orm import Session
from .models.track import Track
from .schemas.track import TrackCreate, TrackUpdate, TrackInDB
from sqlalchemy import text
import os

class SqlServerService:
    def __init__(self, db: Session):
        self.db = db

    def service_check(self):
        return "SqlServer service is running OK"
        
    def create_track(self, track: TrackCreate) -> TrackInDB:
        db_track = Track(**track.dict())
        self.db.add(db_track)
        self.db.commit()
        self.db.refresh(db_track)
        return db_track

    def get_tracks(self) -> List[TrackInDB]:
        return self.db.query(Track).all()

    def get_track(self, track_id: int) -> TrackInDB:
        return self.db.query(Track).get(track_id)

    def update_track(self, track_id: int, track: TrackUpdate) -> TrackInDB:
        db_track = self.db.query(Track).get(track_id)
        for field, value in track.dict().items():
            setattr(db_track, field, value)
        self.db.commit()
        self.db.refresh(db_track)
        return db_track

    def delete_track(self, track_id: int):
        db_track = self.db.query(Track).get(track_id)
        self.db.delete(db_track)
        self.db.commit()
        return {"message": "Track deleted successfully"}

    def load_from_json(self):
        current_dir = os.getcwd()
        DATAFILE = f"{current_dir}/src/sqlserver/data/tracks.json"

        with open(DATAFILE, 'r') as f:
            tracks = json.load(f)
            track_objects = [Track(**TrackCreate(**track).dict()) for track in tracks]
            self.db.bulk_save_objects(track_objects)
            self.db.commit()

        return { "message": f"{len(track_objects)} tracks added." }

    def execute_query(self, query: str) -> List[dict]:
        result = self.db.execute(text(query))
        return [dict(row) for row in result]